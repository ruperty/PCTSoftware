
def get_gdrive():
    import socket
    import os
    if socket.gethostname() == 'DESKTOP-5O07H5P':
        root_dir='/mnt/c/Users/ruper/Google Drive (not syncing)/'
        if os.name == 'nt' :
            root_dir='C:\\Users\\ruper\\Google Drive\\'
    else:
        root_dir='/mnt/c/Users/ryoung/Google Drive/'        
        if os.name == 'nt' :
            root_dir='C:\\Users\\ryoung\\Google Drive\\'
    return root_dir


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