from Conexion import *
from Archivos import *

class Control():
    
    def __init__(self) -> None:
        
        self.__conexiones=list()
        

    def nuevaConexion(self,server,propiedad,ofiVent)->bool:
        conect=ControlConexion(server,propiedad,ofiVent)
        if conect.conectar():
            self.__conexiones.append(conect)
            
            print(f"Conexion exitosa con: {conect.getPropiedad()}")
            Archivos.guardarArchivo(self.__conexiones)
            
        else:
            print(f"Fallo conexion con: {conect.getPropiedad()}")
    
    
        
        
    '''
    def getConexiones(self)->list:
        return self.__conexiones
        
    '''
prueba=Control()

prueba.nuevaConexion("172.19.101.121\sqlexpress","Luna","99")
'''
prueba.nuevaConexion("172.19.25.121\sqlexpress","prueba","779")
prueba.nuevaConexion("172.19.101.139\sqlexpress","Dapo82","1305")
'''

