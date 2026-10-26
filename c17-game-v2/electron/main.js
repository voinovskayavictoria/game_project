const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

let flaskProcess = null;
let mainWindow = null;

const FLASK_PORT = 5009;
const FLASK_HOST = '127.0.0.1';


// ------------------------------------------------------------------
// Запуск Flask в фоне
// ------------------------------------------------------------------
function startFlask() {
  return new Promise((resolve, reject) => {
        const backendPath = app.isPackaged
      ? path.join(process.resourcesPath, 'connect-backend.exe')
      : path.join(__dirname, 'connect-backend.exe');

    flaskProcess = spawn(backendPath, [], {
      cwd: path.dirname(backendPath),
      env: { ...process.env, PORT: String(FLASK_PORT), ELECTRON: '1' },
      stdio: ['ignore', 'pipe', 'pipe'],
      windowsHide: true,
    });

    flaskProcess.stdout.on('data', (d) => console.log('[flask]', d.toString().trim()));
    flaskProcess.stderr.on('data', (d) => console.error('[flask]', d.toString().trim()));
    flaskProcess.on('error', reject);

    waitForServer(resolve, reject);
  });
}

function waitForServer(resolve, reject) {
  const start = Date.now();
  const tryConnect = () => {
    const req = http.get(`http://${FLASK_HOST}:${FLASK_PORT}/`, (res) => {
      res.resume();
      resolve();
    });
    req.on('error', () => {
      if (Date.now() - start > 20000) {
        reject(new Error('Flask не запустился за 20 секунд'));
      } else {
        setTimeout(tryConnect, 300);
      }
    });
    req.setTimeout(1000, () => { req.destroy(); });
  };
  tryConnect();
}


// ------------------------------------------------------------------
// Окно
// ------------------------------------------------------------------
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    title: 'CONNECT',
    backgroundColor: '#0e1621',
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });

  mainWindow.loadURL(`http://${FLASK_HOST}:${FLASK_PORT}/`);
  mainWindow.on('closed', () => { mainWindow = null; });
}


// ------------------------------------------------------------------
// Жизненный цикл
// ------------------------------------------------------------------
app.whenReady().then(async () => {
  try {
    await startFlask();
    console.log('Flask поднялся на порту', FLASK_PORT);
  } catch (e) {
    console.error('Не удалось запустить Flask:', e.message);
  }
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

function killFlask() {
  if (!flaskProcess) return;
  try {
    if (process.platform === 'win32') {
      // На Windows убиваем дерево процессов
      spawn('taskkill', ['/pid', flaskProcess.pid, '/f', '/t']);
    } else {
      flaskProcess.kill();
    }
  } catch (e) { /* ignore */ }
  flaskProcess = null;
}

app.on('window-all-closed', () => {
  killFlask();
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  killFlask();
});