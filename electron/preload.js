const { contextBridge } = require('electron')

// Expose safe APIs to the renderer if needed in future
contextBridge.exposeInMainWorld('electronAPI', {
  platform: process.platform,
})
