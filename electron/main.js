const { app, BrowserWindow, shell } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

const isDev = !app.isPackaged

let mainWindow
let backendProcess

function startBackend() {
  const venvPython = process.platform === 'win32'
    ? path.join(__dirname, '..', 'backend', '.venv', 'Scripts', 'python.exe')
    : path.join(__dirname, '..', 'backend', '.venv', 'bin', 'python')
  const backendPath = path.join(__dirname, '..', 'backend', 'main.py')

  backendProcess = spawn(venvPython, [backendPath], {
    cwd: path.join(__dirname, '..', 'backend'),
    stdio: 'pipe',
  })

  backendProcess.stdout.on('data', (d) => console.log('[backend]', d.toString()))
  backendProcess.stderr.on('data', (d) => console.error('[backend]', d.toString()))
  backendProcess.on('exit', (code) => console.log('[backend] exited', code))
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1100,
    minHeight: 700,
    backgroundColor: '#1a1a2e',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    titleBarStyle: 'hiddenInset',
    show: false,
  })

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '..', 'dist', 'index.html'))
  }

  mainWindow.once('ready-to-show', () => mainWindow.show())

  // Open external links in default browser, not inside the app
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })
}

app.whenReady().then(() => {
  startBackend()
  // Small delay so backend socket is ready before frontend connects
  setTimeout(createWindow, 1500)

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (backendProcess) backendProcess.kill()
  if (process.platform !== 'darwin') app.quit()
})
