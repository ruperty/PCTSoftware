import subprocess, psutil, logging

from os import sep, getpid

logger = logging.getLogger(__name__)


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
        pid = getpid()
        logger.info(f'Started PID {pid}')

 

        
        
    def start_webots(self):
        worldfilepath = self.webotspath +sep+'worlds' +sep+ self.worldfile
        subprocess.Popen([self.exe, f'--port={self.wport}', "--no-rendering", "--batch", "--mode=fast", "--stdout",  "--stderr", worldfilepath])
        logger.info(f'Started webots {worldfilepath} on port {self.wport}')


    def start_evolver(self):
        subprocess.Popen([self.bat])
        logger.info(f'Started evolver {self.bat}')

        
    def webots_ram(self):
        for p in psutil.process_iter():
            port_text = f'--port={self.wport}'
            if 'webots-bin' in p.name() and port_text in p.cmdline() :
                #print(p.memory_info().rss, p.cmdline(), p.name())   
                return p.memory_info().rss

    def get_process_info_webots(self):        
        for p in psutil.process_iter():
            port_text = f'--port={self.wport}'
            if 'webots-bin' in p.name() and port_text in p.cmdline() :
                rtn = f'RAM={p.memory_info().rss} PID={p.pid} webots-bin '
                return rtn


    def get_process_info_by_name(self, exe, text1, text2):
        for p in psutil.process_iter():
            if exe == p.name()  :
                for item in p.cmdline() :
                    if item.find(text1)>-1:
                        if text2 in p.cmdline() :
                            rtn = f'RAM={p.memory_info().rss} PID={p.pid} {exe} {text1} {text2}'
                            return rtn


    def get_process_info_by_pid(self, pid):
        for p in psutil.process_iter():
            if pid == p.pid :
                    rtn = f'RAM={p.memory_info().rss} PID={pid} {p.name()}'
                    return rtn



    def list_processes(self, name):
        for p in psutil.process_iter():
            if name in p.name()  :
                print(p.memory_info().rss, p.cmdline(), p.name())   

    def list_all_processes(self):
        for p in psutil.process_iter():
            print(p.memory_info().rss,  p.name())   
    

        
# ex = Executor(port=6666, wport=1234, sync=False)
#ex.start_webots()
#ex.start_evolver()
# ram = ex.webots_ram()
# print(ram)



