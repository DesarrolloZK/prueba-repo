import pyodbc
from Conexion import *
from Archivos import *
#Clase encargada de la conexion a la base de datos
class CtrlConexion():
    
    def __init__(self) -> None:        
        self.cargar_Conexiones()
        self.listaPrueba=list()
        
        
    def cargar_Conexiones(self)->None:
        self.__conexiones=Archivos.leerArchivo()

    def actualizar_Conexiones(self)->None:
        Archivos.guardarArchivo(self.__conexiones)

    def duplicados(self,server)->bool:
        self.cargar_Conexiones()
        for i in self.__conexiones:
            if server==i[0]:
                return False
        return True       

    def conectar(self,server)->bool:
        try:            
            pyodbc.connect('DRIVER={ODBC Driver 18 for SQL server};'+
            'SERVER='+server+';DATABASE=CheckPostingDB;UID=ivkdb;PWD=Grup0IVK1*;ENCRYPT=No').close()                      
            return True
        except:
            return False

    

    def nuevaConexion(self,server,propiedad,ofiVent)->str:        
        if(self.duplicados(server)):
            if self.conectar(server):
                self.cargar_Conexiones()
                self.__conexiones.append([server,propiedad,ofiVent])
                self.actualizar_Conexiones()         
                return f"Conexion exitosa con: {server} en {propiedad}"           
            else:
                return f"Fallo conexion con: {server} en {propiedad}"
        return f"({server}) Esta conexion ya existe"
    
    

    

prueba=CtrlConexion()

print(prueba.nuevaConexion("172.19.101.121\sqlexpress","Luna","99"))
'''
print(prueba.nuevaConexion("172.19.101.121\sqlexpress","Luna","99"))
print(prueba.nuevaConexion("172.19.101.139\sqlexpress","Dapo82","98"))
print(prueba.nuevaConexion("172.19.101.140\sqlexpress","Michelle82","97"))
'''


