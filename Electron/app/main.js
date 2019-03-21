const {app, BrowserWindow, Menu} = require('electron')

let win = null;


var executablePath = "model/run-dev/run-dev";
var child = require('child_process').spawn(executablePath, { cwd: undefined, env: process.env, shell:true });




app.on('ready', function () {
    // Initialize the window to our specified dimensions
    win = new BrowserWindow({width: 1000, height: 600});
    win.maximize();

    // Specify entry point to default entry point of vue.js
    // win.loadURL('http://localhost:8080'); //this one for the hot-loading dev server run via npm run serve in the vue directory
    win.loadURL('http://localhost:5000'); //this one for production, post-build, from the python directory.
    
    // Remove window once app is closed
    win.on('closed', function () {
        win = null;
    });



    //Set up menus
    const template = [
        {
          label: 'View',
          submenu: [
            { role: 'reload' },
            { role: 'forcereload' },
            { role: 'toggledevtools' },
            { type: 'separator' },
            { role: 'resetzoom' },
            { role: 'zoomin' },
            { role: 'zoomout' },
            { type: 'separator' },
            { role: 'togglefullscreen' }
          ]
        },
        {
          role: 'window',
          submenu: [
            { role: 'minimize' },
            { role: 'close' }
          ]
        },
        {
          role: 'help',
          submenu: [
            {
              label: 'Learn More',
              click () { require('electron').shell.openExternal('https://electronjs.org') }
            },
            {
                label: 'Dev Tools',
                click () { win.webContents.openDevTools(); }
              }
          ]
        }
    ]

    if (process.platform === 'darwin') {
        template.unshift({
          label: app.getName(),
          submenu: [
            { role: 'about' },
            { role: 'quit' }
          ]
        })
      
        // Edit menu
        template[1].submenu.push(
          { type: 'separator' },
          {
            label: 'Speech',
            submenu: [
              { role: 'startspeaking' },
              { role: 'stopspeaking' }
            ]
          }
        )
      
        // Window menu
        template[3].submenu = [
          { role: 'close' },
          { role: 'minimize' },
          { role: 'zoom' },
          { type: 'separator' },
          { role: 'front' },
          { role: 'toggledevtools' },
        ]
      }

    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)

});

//create the application window if the window variable is null
app.on('activate', () => {
    if (win === null) {
        createWindow()
        
    }
})

//quit the app once closed
app.on('window-all-closed', function () {
    child.kill('SIGINT');
    if (process.platform !== 'darwin') {
        
        app.quit();
    }
});
