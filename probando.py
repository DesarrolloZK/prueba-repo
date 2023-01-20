import time
from datetime import datetime as dt
def reloj():
    tiempo=dt.now().hour
    if 8<tiempo<17:
        time.sleep(1800)
    reloj()
reloj()