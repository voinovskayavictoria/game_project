const { contextBridge } = require('electron');
const os = require('os');

contextBridge.exposeInMainWorld('system', {
  username: os.userInfo().username,
  platform: process.platform,
  hostname: os.hostname(),
});