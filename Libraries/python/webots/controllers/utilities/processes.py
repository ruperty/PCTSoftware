import subprocess
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
        self.bat = get_root_path() + f'Versioning\\PCTSoftware\\Libraries\\python\\pctlocal\\tests\\ga\\pctobject\\evolve-{port}.bat'
        
        
    def start_webots(self):
        worldfilepath = self.webotspath +sep+'worlds' +sep+ self.worldfile
        subprocess.Popen([self.exe, f'--port={self.wport}', "--no-rendering", "--batch", "--mode=fast", "--stdout",  "--stderr", worldfilepath])

    def start_evolver(self):
        subprocess.Popen([self.bat])

        
        
ex = Executor(port=6666, wport=1235, sync=False)

#ex.start_webots()
ex.start_evolver()


print("h")

