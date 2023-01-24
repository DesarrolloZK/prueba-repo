import time
import threading
import datetime
from ftplib import FTP


with FTP('181.48.67.100', 'Administrador', '!MiCros2022%') as ftp:
    # genera una lista de archivos
    with open('test/prueb2.txt','rb') as file:
        ftp.storlines('STOR prueb2.txt',file)



