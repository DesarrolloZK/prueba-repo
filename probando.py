import time
import threading



def contar():
    for i in range(1,11):
        print(i)
        if i==7:
            descontar()
        time.sleep(1)
    contar()

def descontar():
    for i in range(1,5):
        print(f'Reportes {i}')
        time.sleep(0.5)

hilo1=threading.Thread(target=contar)
hilo1.start()


