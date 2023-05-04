from os import sep


def get_root_path():
    import socket
    import os
    if socket.gethostname() == 'DESKTOP-5O07H5P':
        root_dir='/mnt/c/Users/ruper/'
        if os.name == 'nt' :
            root_dir='C:\\Users\\ruper\\'
    else:
        root_dir='/mnt/c/Users/ryoung/'        
        if os.name == 'nt' :
            root_dir='C:\\Users\\ryoung\\'
    return root_dir


class Executor():

    def __init__(self, port=None, wport=None, sync=None):
        self.port = port
        self.wport = wport
        self.webotspath = get_root_path() + 'Versioning'+sep+'PCTSoftware'+sep+'Libraries'+sep+'python'+sep+'webots'
        self.exe = "C:\\Program Files\\Webots\\msys64\\mingw64\\bin\\webotsw.exe"
        if sync:
            self.worldfile = "wrestling.wbt"
        else:
            self.worldfile = "wrestling-nosync.wbt"
        
        
    def start_webots(self):
        import subprocess
        worldfilepath = self.webotspath +sep+'worlds' +sep+ self.worldfile
        subprocess.Popen([self.exe, f'--port={self.wport}', "--no-rendering", "--batch", "--mode=fast", "--stdout",  "--stderr", worldfilepath])


ex = Executor(port=9999, wport=1235, sync=False)

ex.start_webots()

print("h")


