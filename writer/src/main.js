const { app, BrowserWindow, Menu, dialog, ipcMain, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

// ─── State ───────────────────────────────────────────────────────────────────
let mainWindow = null;
let pythonBridge = null;
let currentFilePath = null;
let isDirty = false;
let autoSaveTimer = null;
let recentFiles = [];
let isDarkMode = false;
let zoomLevel = 1.0;

const RECENT_FILES_PATH = path.join(app.getPath('userData'), 'recent-files.json');
const AUTOSAVE_INTERVAL_MS = 60_000; // 1 minute

// ─── Recent Files ────────────────────────────────────────────────────────────
function loadRecentFiles() {
  try {
    if (fs.existsSync(RECENT_FILES_PATH)) {
      recentFiles = JSON.parse(fs.readFileSync(RECENT_FILES_PATH, 'utf-8'));
    }
  } catch {
    recentFiles = [];
  }
}

function saveRecentFiles() {
  try {
    fs.writeFileSync(RECENT_FILES_PATH, JSON.stringify(recentFiles.slice(0, 10)));
  } catch { /* ignore */ }
}

function addRecentFile(filePath) {
  recentFiles = [filePath, ...recentFiles.filter(f => f !== filePath)].slice(0, 10);
  saveRecentFiles();
  buildMenu();
}

// ─── Python Bridge ───────────────────────────────────────────────────────────
function startPythonBridge() {
  const bridgePath = path.join(__dirname, 'bridge.py');
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

  try {
    pythonBridge = spawn(pythonCmd, [bridgePath], {
      cwd: __dirname,
      env: { ...process.env, PYTHONUNBUFFERED: '1' },
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    pythonBridge.stdout.on('data', (data) => {
      console.log('[Python Bridge]', data.toString().trim());
    });

    pythonBridge.stderr.on('data', (data) => {
      console.error('[Python Bridge Error]', data.toString().trim());
    });

    pythonBridge.on('error', () => {
      pythonBridge = null;
    });

    pythonBridge.on('close', (code) => {
      console.log(`[Python Bridge] exited with code ${code}`);
      pythonBridge = null;
    });
  } catch {
    pythonBridge = null;
  }
}

function stopPythonBridge() {
  if (pythonBridge) {
    pythonBridge.kill();
    pythonBridge = null;
  }
}

// ─── Window ──────────────────────────────────────────────────────────────────
function updateTitle() {
  if (!mainWindow) return;
  const docName = currentFilePath ? path.basename(currentFilePath) : 'Untitled';
  const dirtyMark = isDirty ? ' •' : '';
  mainWindow.setTitle(`${docName}${dirtyMark} — Varnaakshara Writer`);
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: 'Untitled — Varnaakshara Writer',
    icon: path.join(__dirname, '..', 'assets', 'icon.png'),
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      spellcheck: false,
    },
    show: false,
  });

  // Load from webpack dev server in dev, or built file in production
  const isDev = !app.isPackaged;
  if (isDev) {
    mainWindow.loadURL('http://localhost:9000');
    // mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '..', 'build', 'index.html'));
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.maximize();
    mainWindow.show();
    mainWindow.focus();
  });

  mainWindow.on('close', async (e) => {
    if (isDirty) {
      e.preventDefault();
      const { response } = await dialog.showMessageBox(mainWindow, {
        type: 'warning',
        buttons: ['Save', "Don't Save", 'Cancel'],
        defaultId: 0,
        cancelId: 2,
        title: 'Unsaved Changes',
        message: 'Do you want to save changes before closing?',
      });
      if (response === 0) {
        mainWindow.webContents.send('menu-save');
        // Wait briefly for save to complete, then close
        setTimeout(() => {
          isDirty = false;
          mainWindow.close();
        }, 500);
      } else if (response === 1) {
        isDirty = false;
        mainWindow.close();
      }
      // response === 2 → Cancel, do nothing
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
    clearInterval(autoSaveTimer);
  });

  // Auto-save timer
  autoSaveTimer = setInterval(() => {
    if (isDirty && currentFilePath) {
      mainWindow?.webContents.send('auto-save');
    }
  }, AUTOSAVE_INTERVAL_MS);
}

// ─── Menu ────────────────────────────────────────────────────────────────────
function buildMenu() {
  const recentFilesMenu = recentFiles.length > 0
    ? recentFiles.map(filePath => ({
        label: path.basename(filePath),
        sublabel: filePath,
        click: () => {
          mainWindow?.webContents.send('open-file', filePath);
          addRecentFile(filePath);
        },
      }))
    : [{ label: 'No Recent Files', enabled: false }];

  const template = [
    // ── File ──
    {
      label: 'File',
      submenu: [
        {
          label: 'New',
          accelerator: 'CmdOrCtrl+N',
          click: () => mainWindow?.webContents.send('menu-new'),
        },
        {
          label: 'Open…',
          accelerator: 'CmdOrCtrl+O',
          click: async () => {
            const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
              filters: [
                { name: 'Varnaakshara Documents', extensions: ['vnk'] },
                { name: 'Word Documents', extensions: ['docx'] },
                { name: 'HTML Files', extensions: ['html', 'htm'] },
                { name: 'Text Files', extensions: ['txt'] },
                { name: 'All Files', extensions: ['*'] },
              ],
              properties: ['openFile'],
            });
            if (!canceled && filePaths[0]) {
              mainWindow?.webContents.send('open-file', filePaths[0]);
              addRecentFile(filePaths[0]);
            }
          },
        },
        {
          label: 'Import DOCX…',
          click: async () => {
            const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
              filters: [
                { name: 'Word Documents', extensions: ['docx'] },
                { name: 'All Files', extensions: ['*'] },
              ],
              properties: ['openFile'],
            });
            if (!canceled && filePaths[0]) {
              mainWindow?.webContents.send('menu-import-docx', filePaths[0]);
              addRecentFile(filePaths[0]);
            }
          },
        },
        { type: 'separator' },
        {
          label: 'Save',
          accelerator: 'CmdOrCtrl+S',
          click: () => mainWindow?.webContents.send('menu-save'),
        },
        {
          label: 'Save As…',
          accelerator: 'CmdOrCtrl+Shift+S',
          click: () => mainWindow?.webContents.send('menu-save-as'),
        },
        { type: 'separator' },
        {
          label: 'Export',
          submenu: [
            {
              label: 'Export as PDF…',
              click: () => mainWindow?.webContents.send('menu-export', 'pdf'),
            },
            {
              label: 'Export as DOCX…',
              click: () => mainWindow?.webContents.send('menu-export', 'docx'),
            },
            {
              label: 'Export as RTF…',
              click: () => mainWindow?.webContents.send('menu-export', 'rtf'),
            },
            {
              label: 'Export as HTML…',
              click: () => mainWindow?.webContents.send('menu-export', 'html'),
            },
          ],
        },
        { type: 'separator' },
        {
          label: 'Print…',
          accelerator: 'CmdOrCtrl+P',
          click: () => mainWindow?.webContents.send('menu-print'),
        },
        { type: 'separator' },
        {
          label: 'Recent Files',
          submenu: recentFilesMenu,
        },
        { type: 'separator' },
        {
          label: 'Exit',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Alt+F4',
          click: () => app.quit(),
        },
      ],
    },
    // ── Edit ──
    {
      label: 'Edit',
      submenu: [
        {
          label: 'Undo',
          accelerator: 'CmdOrCtrl+Z',
          click: () => mainWindow?.webContents.send('menu-undo'),
        },
        {
          label: 'Redo',
          accelerator: 'CmdOrCtrl+Y',
          click: () => mainWindow?.webContents.send('menu-redo'),
        },
        { type: 'separator' },
        { label: 'Cut', accelerator: 'CmdOrCtrl+X', role: 'cut' },
        { label: 'Copy', accelerator: 'CmdOrCtrl+C', role: 'copy' },
        { label: 'Paste', accelerator: 'CmdOrCtrl+V', role: 'paste' },
        {
          label: 'Paste Special…',
          accelerator: 'CmdOrCtrl+Shift+V',
          click: () => mainWindow?.webContents.send('menu-paste-special'),
        },
        { type: 'separator' },
        {
          label: 'Find & Replace…',
          accelerator: 'CmdOrCtrl+H',
          click: () => mainWindow?.webContents.send('menu-find-replace'),
        },
        { type: 'separator' },
        { label: 'Select All', accelerator: 'CmdOrCtrl+A', role: 'selectAll' },
      ],
    },
    // ── View ──
    {
      label: 'View',
      submenu: [
        {
          label: 'Zoom In',
          accelerator: 'CmdOrCtrl+=',
          click: () => {
            zoomLevel = Math.min(zoomLevel + 0.1, 3.0);
            mainWindow?.webContents.send('set-zoom', zoomLevel);
          },
        },
        {
          label: 'Zoom Out',
          accelerator: 'CmdOrCtrl+-',
          click: () => {
            zoomLevel = Math.max(zoomLevel - 0.1, 0.5);
            mainWindow?.webContents.send('set-zoom', zoomLevel);
          },
        },
        {
          label: 'Reset Zoom',
          accelerator: 'CmdOrCtrl+0',
          click: () => {
            zoomLevel = 1.0;
            mainWindow?.webContents.send('set-zoom', zoomLevel);
          },
        },
        { type: 'separator' },
        {
          label: 'Toggle Ruler',
          click: () => mainWindow?.webContents.send('toggle-ruler'),
        },
        {
          label: 'Full Screen',
          accelerator: 'F11',
          click: () => {
            mainWindow?.setFullScreen(!mainWindow.isFullScreen());
          },
        },
        { type: 'separator' },
        {
          label: 'Dark Mode',
          type: 'checkbox',
          checked: isDarkMode,
          click: (item) => {
            isDarkMode = item.checked;
            mainWindow?.webContents.send('set-dark-mode', isDarkMode);
          },
        },
        { type: 'separator' },
        {
          label: 'Toggle Developer Tools',
          accelerator: 'F12',
          click: () => mainWindow?.webContents.toggleDevTools(),
        },
      ],
    },
    // ── Insert ──
    {
      label: 'Insert',
      submenu: [
        {
          label: 'Image…',
          click: async () => {
            const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
              filters: [{ name: 'Images', extensions: ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp'] }],
              properties: ['openFile'],
            });
            if (!canceled && filePaths[0]) {
              mainWindow?.webContents.send('insert-image', filePaths[0]);
            }
          },
        },
        {
          label: 'Table…',
          click: () => mainWindow?.webContents.send('insert-table'),
        },
        {
          label: 'Link…',
          accelerator: 'CmdOrCtrl+K',
          click: () => mainWindow?.webContents.send('insert-link'),
        },
        { type: 'separator' },
        {
          label: 'Bookmark…',
          click: () => mainWindow?.webContents.send('insert-bookmark'),
        },
        {
          label: 'Page Break',
          accelerator: 'CmdOrCtrl+Enter',
          click: () => mainWindow?.webContents.send('insert-page-break'),
        },
        {
          label: 'Special Character…',
          click: () => mainWindow?.webContents.send('insert-special-char'),
        },
        { type: 'separator' },
        {
          label: 'Header & Footer…',
          click: () => mainWindow?.webContents.send('insert-header-footer'),
        },
      ],
    },
    // ── Format ──
    {
      label: 'Format',
      submenu: [
        {
          label: 'Bold',
          accelerator: 'CmdOrCtrl+B',
          click: () => mainWindow?.webContents.send('format-bold'),
        },
        {
          label: 'Italic',
          accelerator: 'CmdOrCtrl+I',
          click: () => mainWindow?.webContents.send('format-italic'),
        },
        {
          label: 'Underline',
          accelerator: 'CmdOrCtrl+U',
          click: () => mainWindow?.webContents.send('format-underline'),
        },
        {
          label: 'Strikethrough',
          accelerator: 'CmdOrCtrl+Shift+X',
          click: () => mainWindow?.webContents.send('format-strikethrough'),
        },
        { type: 'separator' },
        {
          label: 'Font…',
          click: () => mainWindow?.webContents.send('format-font'),
        },
        {
          label: 'Paragraph…',
          click: () => mainWindow?.webContents.send('format-paragraph'),
        },
        { type: 'separator' },
        {
          label: 'Bullets',
          click: () => mainWindow?.webContents.send('format-bullets'),
        },
        {
          label: 'Numbering',
          click: () => mainWindow?.webContents.send('format-numbering'),
        },
        { type: 'separator' },
        {
          label: 'Alignment',
          submenu: [
            { label: 'Left', accelerator: 'CmdOrCtrl+L', click: () => mainWindow?.webContents.send('format-align', 'left') },
            { label: 'Center', accelerator: 'CmdOrCtrl+E', click: () => mainWindow?.webContents.send('format-align', 'center') },
            { label: 'Right', accelerator: 'CmdOrCtrl+R', click: () => mainWindow?.webContents.send('format-align', 'right') },
            { label: 'Justify', accelerator: 'CmdOrCtrl+J', click: () => mainWindow?.webContents.send('format-align', 'justify') },
          ],
        },
        {
          label: 'Line Spacing',
          submenu: [
            { label: '1.0', click: () => mainWindow?.webContents.send('format-line-spacing', 1.0) },
            { label: '1.15', click: () => mainWindow?.webContents.send('format-line-spacing', 1.15) },
            { label: '1.5', click: () => mainWindow?.webContents.send('format-line-spacing', 1.5) },
            { label: '2.0', click: () => mainWindow?.webContents.send('format-line-spacing', 2.0) },
            { label: '2.5', click: () => mainWindow?.webContents.send('format-line-spacing', 2.5) },
            { label: '3.0', click: () => mainWindow?.webContents.send('format-line-spacing', 3.0) },
          ],
        },
        {
          label: 'Columns',
          submenu: [
            { label: 'One', click: () => mainWindow?.webContents.send('format-columns', 1) },
            { label: 'Two', click: () => mainWindow?.webContents.send('format-columns', 2) },
            { label: 'Three', click: () => mainWindow?.webContents.send('format-columns', 3) },
          ],
        },
      ],
    },
    // ── Tools ──
    {
      label: 'Tools',
      submenu: [
        {
          label: 'Spell Check',
          accelerator: 'F7',
          click: () => mainWindow?.webContents.send('tools-spell-check'),
        },
        {
          label: 'Word Count',
          click: () => mainWindow?.webContents.send('tools-word-count'),
        },
        { type: 'separator' },
        {
          label: 'Transliterate Selection…',
          click: () => mainWindow?.webContents.send('tools-transliterate'),
        },
        {
          label: 'Convert Script…',
          click: () => mainWindow?.webContents.send('tools-convert-script'),
        },
        {
          label: 'Convert Unicode ↔ ANSI…',
          click: () => mainWindow?.webContents.send('tools-unicode-ansi'),
        },
        {
          label: 'Panchama Varga Conversion…',
          click: () => mainWindow?.webContents.send('tools-panchama-varga'),
        },
        { type: 'separator' },
        {
          label: 'OCR — Scan Image…',
          click: () => mainWindow?.webContents.send('tools-ocr'),
        },
      ],
    },
    // ── Table ──
    {
      label: 'Table',
      submenu: [
        {
          label: 'Insert Table…',
          click: () => mainWindow?.webContents.send('insert-table'),
        },
        { type: 'separator' },
        {
          label: 'Insert Row Above',
          click: () => mainWindow?.webContents.send('table-insert-row', 'above'),
        },
        {
          label: 'Insert Row Below',
          click: () => mainWindow?.webContents.send('table-insert-row', 'below'),
        },
        {
          label: 'Insert Column Left',
          click: () => mainWindow?.webContents.send('table-insert-col', 'left'),
        },
        {
          label: 'Insert Column Right',
          click: () => mainWindow?.webContents.send('table-insert-col', 'right'),
        },
        { type: 'separator' },
        {
          label: 'Delete Row',
          click: () => mainWindow?.webContents.send('table-delete-row'),
        },
        {
          label: 'Delete Column',
          click: () => mainWindow?.webContents.send('table-delete-col'),
        },
        { type: 'separator' },
        {
          label: 'Merge Cells',
          click: () => mainWindow?.webContents.send('table-merge-cells'),
        },
        {
          label: 'Split Cells…',
          click: () => mainWindow?.webContents.send('table-split-cells'),
        },
        { type: 'separator' },
        {
          label: 'Table Properties…',
          click: () => mainWindow?.webContents.send('table-properties'),
        },
      ],
    },
    // ── Window ──
    {
      label: 'Window',
      submenu: [
        { label: 'Minimize', role: 'minimize' },
        { label: 'Maximize', click: () => mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize() },
        { type: 'separator' },
        { label: 'Close', role: 'close' },
      ],
    },
    // ── Help ──
    {
      label: 'Help',
      submenu: [
        {
          label: 'Documentation',
          click: () => shell.openExternal('https://github.com/varnaakshara/writer'),
        },
        {
          label: 'Report Issue',
          click: () => shell.openExternal('https://github.com/varnaakshara/writer/issues'),
        },
        { type: 'separator' },
        {
          label: 'About Varnaakshara Writer',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About Varnaakshara Writer',
              message: 'Varnaakshara Writer',
              detail: `Version ${require('../package.json').version}\n\nA free word processor for Indian languages.\nPart of the Varnaakshara IME suite.\n\n© 2026 Varnaakshara`,
            });
          },
        },
      ],
    },
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// ─── IPC Handlers ────────────────────────────────────────────────────────────
function setupIPC() {
  // Generic error dialog from renderer
  ipcMain.handle('show-error', async (_event, { title, message }) => {
    try {
      await dialog.showMessageBox(mainWindow, {
        type: 'error',
        title: title || 'Error',
        message: title || 'Error',
        detail: message || '',
      });
      return { success: true };
    } catch (err) {
      return { success: false, reason: err.message };
    }
  });
  // File: Save
  ipcMain.handle('save-file', async (_event, { filePath, content }) => {
    try {
      const targetPath = filePath || currentFilePath;
      if (!targetPath) {
        // Trigger Save As
        const { canceled, filePath: savePath } = await dialog.showSaveDialog(mainWindow, {
          defaultPath: 'Untitled.vnk',
          filters: [
            { name: 'Varnaakshara Documents', extensions: ['vnk'] },
            { name: 'HTML Files', extensions: ['html', 'htm'] },
            { name: 'All Files', extensions: ['*'] },
          ],
        });
        if (canceled || !savePath) return { success: false, reason: 'cancelled' };
        fs.writeFileSync(savePath, content, 'utf-8');
        currentFilePath = savePath;
        isDirty = false;
        addRecentFile(savePath);
        updateTitle();
        return { success: true, filePath: savePath };
      }
      fs.writeFileSync(targetPath, content, 'utf-8');
      currentFilePath = targetPath;
      isDirty = false;
      updateTitle();
      return { success: true, filePath: targetPath };
    } catch (err) {
      return { success: false, reason: err.message };
    }
  });

  // File: Save As
  ipcMain.handle('save-file-as', async (_event, { content, defaultName }) => {
    try {
      const { canceled, filePath } = await dialog.showSaveDialog(mainWindow, {
        defaultPath: defaultName || 'Untitled.vnk',
        filters: [
          { name: 'Varnaakshara Documents', extensions: ['vnk'] },
          { name: 'HTML Files', extensions: ['html', 'htm'] },
          { name: 'All Files', extensions: ['*'] },
        ],
      });
      if (canceled || !filePath) return { success: false, reason: 'cancelled' };
      fs.writeFileSync(filePath, content, 'utf-8');
      currentFilePath = filePath;
      isDirty = false;
      addRecentFile(filePath);
      updateTitle();
      return { success: true, filePath };
    } catch (err) {
      return { success: false, reason: err.message };
    }
  });

  // File: Open
  ipcMain.handle('open-file', async (_event, filePath) => {
    try {
      const targetPath = filePath || (await (async () => {
        const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
          filters: [
            { name: 'Varnaakshara Documents', extensions: ['vnk'] },
            { name: 'Word Documents', extensions: ['docx'] },
            { name: 'HTML Files', extensions: ['html', 'htm'] },
            { name: 'Text Files', extensions: ['txt'] },
            { name: 'All Files', extensions: ['*'] },
          ],
          properties: ['openFile'],
        });
        return canceled ? null : filePaths[0];
      })());
      if (!targetPath) return { success: false, reason: 'cancelled' };
      const content = fs.readFileSync(targetPath, 'utf-8');
      currentFilePath = targetPath;
      isDirty = false;
      addRecentFile(targetPath);
      updateTitle();
      return { success: true, filePath: targetPath, content };
    } catch (err) {
      return { success: false, reason: err.message };
    }
  });

  // DOCX: Open as binary
  ipcMain.handle('open-docx', async (_event, filePath) => {
    try {
      const targetPath = filePath || (await (async () => {
        const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
          filters: [
            { name: 'Word Documents', extensions: ['docx'] },
            { name: 'All Files', extensions: ['*'] },
          ],
          properties: ['openFile'],
        });
        return canceled ? null : filePaths[0];
      })());
      if (!targetPath) return { success: false, reason: 'cancelled' };
      const buffer = fs.readFileSync(targetPath);
      currentFilePath = null;
      isDirty = true;
      updateTitle();
      return { success: true, filePath: targetPath, buffer: buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength) };
    } catch (err) {
      return { success: false, reason: err.message };
    }
  });

  // Export
  ipcMain.handle('export-file', async (_event, { format, content }) => {
    try {
      const filters = {
        pdf: [{ name: 'PDF Files', extensions: ['pdf'] }],
        docx: [{ name: 'Word Documents', extensions: ['docx'] }],
        html: [{ name: 'HTML Files', extensions: ['html', 'htm'] }],
        rtf: [{ name: 'Rich Text Format', extensions: ['rtf'] }],
      };
      const { canceled, filePath } = await dialog.showSaveDialog(mainWindow, {
        defaultPath: `Untitled.${format}`,
        filters: filters[format] || [{ name: 'All Files', extensions: ['*'] }],
      });
      if (canceled || !filePath) return { success: false, reason: 'cancelled' };

      if (format === 'html') {
        fs.writeFileSync(filePath, content, 'utf-8');
        return { success: true, filePath };
      }

      if (format === 'pdf') {
        // Prefer main-process printToPDF for best fidelity.
        const pdfData = await mainWindow.webContents.printToPDF({
          printBackground: true,
          pageSize: 'A4',
          margins: { top: 0.5, bottom: 0.5, left: 0.5, right: 0.5 },
        });
        fs.writeFileSync(filePath, pdfData);
        return { success: true, filePath };
      }

      if (format === 'docx') {
        // Renderer generates binary (base64). Save bytes.
        const b64 = String(content || '');
        const bytes = Buffer.from(b64, 'base64');
        fs.writeFileSync(filePath, bytes);
        return { success: true, filePath };
      }

      if (format === 'rtf') {
        fs.writeFileSync(filePath, content, 'utf-8');
        return { success: true, filePath };
      }

      return { success: false, reason: 'Unknown format' };
    } catch (err) {
      return { success: false, reason: err.message };
    }
  });

  // Print
  ipcMain.handle('print', async () => {
    mainWindow?.webContents.print({ printBackground: true });
  });

  // Dirty flag
  ipcMain.on('set-dirty', (_event, dirty) => {
    isDirty = dirty;
    updateTitle();
  });

  // Set current file path from renderer
  ipcMain.on('set-current-file', (_event, filePath) => {
    currentFilePath = filePath;
    updateTitle();
  });

  // Transliteration bridge proxy — forward to Python HTTP server
  ipcMain.handle('bridge-request', async (_event, { endpoint, data }) => {
    try {
      const http = require('http');
      return await new Promise((resolve, reject) => {
        const postData = JSON.stringify(data);
        const req = http.request(
          {
            hostname: '127.0.0.1',
            port: 5111,
            path: endpoint,
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Content-Length': Buffer.byteLength(postData),
            },
            timeout: 10000,
          },
          (res) => {
            let body = '';
            res.on('data', chunk => (body += chunk));
            res.on('end', () => {
              try {
                resolve({ success: true, data: JSON.parse(body) });
              } catch {
                resolve({ success: true, data: body });
              }
            });
          }
        );
        req.on('error', (err) => resolve({ success: false, error: err.message }));
        req.on('timeout', () => {
          req.destroy();
          resolve({ success: false, error: 'Request timed out' });
        });
        req.write(postData);
        req.end();
      });
    } catch (err) {
      return { success: false, error: err.message };
    }
  });
}

// ─── App Lifecycle ───────────────────────────────────────────────────────────
// Silence console in Wine (stdout/stderr EBADF)
try { console.log('test'); } catch {
  const noop = () => {};
  console.log = noop; console.warn = noop;
  console.error = noop; console.info = noop;
}

app.whenReady().then(() => {
  loadRecentFiles();
  buildMenu();
  createWindow();
  try { startPythonBridge(); } catch { /* bridge optional */ }
  setupIPC();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  stopPythonBridge();
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  stopPythonBridge();
});
