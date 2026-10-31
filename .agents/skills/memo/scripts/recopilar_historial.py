#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de recopilación y transcripción de conversaciones para el agente Memo.
Proyecto: La Canción del Silencio
Genera y actualiza: historial/historial.md
"""

import os
import json
import re
from datetime import datetime, timezone

# Directorio raíz del proyecto (4 niveles arriba desde .agents/skills/memo/scripts)
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
HISTORIAL_DIR = os.path.join(WORKSPACE_DIR, "historial")
HISTORIAL_FILE = os.path.join(HISTORIAL_DIR, "historial.md")
BRAIN_DIR = os.path.expanduser(r"~\.gemini\antigravity-ide\brain")

def clean_user_prompt(raw_text):
    if not raw_text:
        return ""
    # Extract <USER_REQUEST> if present
    match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", raw_text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    else:
        text = raw_text.strip()
    return text

def parse_transcript_file(file_path):
    turns = []
    if not os.path.exists(file_path):
        return turns
        
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
                
            step_type = obj.get("type")
            created_at = obj.get("created_at")
            
            if step_type == "USER_INPUT":
                raw_c = obj.get("content", "")
                prompt = clean_user_prompt(raw_c)
                if prompt:
                    turns.append({
                        "role": "user",
                        "time": created_at,
                        "text": prompt
                    })
            elif step_type == "PLANNER_RESPONSE" and obj.get("status") == "DONE":
                c = obj.get("content")
                tool_calls = obj.get("tool_calls")
                # We record if it has user-facing message content and no tool calls (or final answer)
                if c and not tool_calls:
                    turns.append({
                        "role": "assistant",
                        "time": created_at,
                        "text": c.strip()
                    })
            elif step_type == "CALL_TOOL" or "tool_calls" in obj and obj.get("tool_calls"):
                # Track tool usage if relevant
                pass
    return turns

def find_novela_conversations():
    if not os.path.exists(BRAIN_DIR):
        print(f"Directorio de brain no encontrado: {BRAIN_DIR}")
        return []

    dirs = [
        os.path.join(BRAIN_DIR, d)
        for d in os.listdir(BRAIN_DIR)
        if os.path.isdir(os.path.join(BRAIN_DIR, d)) and d != "tempmediaStorage"
    ]

    novela_convs = []
    for d in dirs:
        log_file = os.path.join(d, ".system_generated", "logs", "transcript.jsonl")
        log_full = os.path.join(d, ".system_generated", "logs", "transcript_full.jsonl")
        target_log = log_full if os.path.exists(log_full) else log_file
        
        if not os.path.exists(target_log):
            continue

        is_novela = False
        try:
            with open(target_log, "r", encoding="utf-8", errors="ignore") as f:
                for idx, line in enumerate(f):
                    if idx > 30:
                        break
                    if any(k in line for k in ["NOVELA_3", "cancion-del-silencio", "La Canción del Silencio", "novela/"]):
                        is_novela = True
                        break
        except Exception:
            continue

        if is_novela:
            mtime = os.path.getmtime(d)
            novela_convs.append((d, target_log, mtime))

    # Sort chronologically by directory modification time
    novela_convs.sort(key=lambda x: x[2])
    return novela_convs

def format_iso_time(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return iso_str

def generate_historial_markdown(conv_data_list):
    os.makedirs(HISTORIAL_DIR, exist_ok=True)
    
    lines = [
        "# 📚 Historial y Bitácora de Conversaciones",
        "## *La Canción del Silencio / Antigravity*",
        "",
        "> **Agente Responsable:** **Memo** (Cronista y Archivero Mayor)",
        f"> **Última actualización:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"> **Total de sesiones recopiladas:** {len(conv_data_list)}",
        "",
        "Este documento recopila la transcripción íntegra y ordenada de las conversaciones, instrucciones, acuerdos técnicos, debates de trama y decisiones editoriales entre el Autor y Antigravity.",
        "",
        "---",
        "",
        "## 📑 Índice Cronológico de Sesiones",
        ""
    ]

    # Index
    for i, item in enumerate(conv_data_list, 1):
        conv_id = item["id"]
        first_time = item["start_time"]
        topic = item["first_prompt"][:80].replace("\n", " ")
        lines.append(f"- **[Sesión {i:02d} — {first_time}](#sesión-{i:02d}---{conv_id[:8]})**: {topic}...")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed sessions
    for i, item in enumerate(conv_data_list, 1):
        conv_id = item["id"]
        start_time = item["start_time"]
        turns = item["turns"]

        lines.append(f"## Sesión {i:02d} - {conv_id[:8]}")
        lines.append(f"**Identificador completo:** `{conv_id}`  ")
        lines.append(f"**Fecha y Hora de inicio:** `{start_time}`  ")
        lines.append(f"**Intercambios registrados:** {len(turns)}")
        lines.append("")

        if not turns:
            lines.append("*Sin mensajes de chat directos registrados en esta sesión.*")
            lines.append("")
            lines.append("---")
            lines.append("")
            continue

        for turn in turns:
            role = turn["role"]
            t = turn.get("time", "")
            formatted_t = format_iso_time(t)
            time_badge = f" *({formatted_t})*" if formatted_t else ""
            
            if role == "user":
                lines.append(f"### 👤 Autor{time_badge}")
                lines.append("")
                # Indent or format prompt
                lines.append(turn["text"])
                lines.append("")
            else:
                lines.append(f"### 🤖 Antigravity / Asistente{time_badge}")
                lines.append("")
                lines.append(turn["text"])
                lines.append("")

        lines.append("---")
        lines.append("")

    content = "\n".join(lines)
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Historial escrito con éxito en: {HISTORIAL_FILE}")
    print(f"Total sesiones volcadas: {len(conv_data_list)}")

def main():
    print("Iniciando recopilación de conversaciones...")
    novela_convs = find_novela_conversations()
    print(f"Encontradas {len(novela_convs)} conversaciones vinculadas a NOVELA_3.")

    conv_data_list = []
    for d, target_log, mtime in novela_convs:
        conv_id = os.path.basename(d)
        turns = parse_transcript_file(target_log)
        
        # Determine start time
        start_time = ""
        first_prompt = "(Sin texto inicial)"
        for t in turns:
            if t["role"] == "user":
                first_prompt = t["text"]
                start_time = format_iso_time(t.get("time"))
                break
        if not start_time:
            start_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S UTC")

        conv_data_list.append({
            "id": conv_id,
            "start_time": start_time,
            "first_prompt": first_prompt,
            "turns": turns
        })

    generate_historial_markdown(conv_data_list)

if __name__ == "__main__":
    main()
