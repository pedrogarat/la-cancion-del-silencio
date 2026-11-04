const fs = require('fs');
const path = require('path');
const cp = require('child_process');

const tempRepo = path.resolve('C:/Users/Usuario/.gemini/antigravity/git_temp_repo');
const workspaceDir = path.resolve('.');

if (!fs.existsSync(tempRepo)) fs.mkdirSync(tempRepo, { recursive: true });
try { cp.execSync(`robocopy "." "${tempRepo}" /E /XD .gemini node_modules /R:1 /W:1`, { stdio: 'pipe' }); } catch (e) {}

try {
  cp.execSync('git add .', { cwd: tempRepo, stdio: 'pipe' });
  const status = cp.execSync('git status --short', { cwd: tempRepo, encoding: 'utf8' });
  console.log('Status:\n', status);
  if (status.trim()) {
    cp.execSync('git commit -m "feat(editorial): incorporar Capitulo 24 La Conjuracion del Silencio con PDFs, visor web de 24 capitulos y sinopsis"', { cwd: tempRepo, stdio: 'pipe' });
    cp.execSync('git push origin main', { cwd: tempRepo, stdio: 'pipe' });
    console.log('Push complete');
  }
} catch (e) {
  console.error('Error:', e.message);
}

try { cp.execSync(`robocopy "${path.join(tempRepo, '.git')}" "${path.join(workspaceDir, '.git')}" /E /R:1 /W:1`, { stdio: 'pipe' }); } catch (e) {}
fs.rmSync(tempRepo, { recursive: true, force: true });
console.log('Sync finished');
