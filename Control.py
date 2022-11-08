import pyodbc
from Conexion import *
from Archivos import *
#Clase encargada de la conexion a la base de datos
class CtrlConexion():
    
    def __init__(self) -> None:        
        self.cargar_Conexiones()
        self.listaPrueba=list()
        self.__db=Conexion()        
        
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

    def nuevaConexion(self,server,propiedad,ofiVent)->str:        
        if(self.duplicados(server)):
            if self.__db.conectar(server,propiedad,ofiVent):
                self.cargar_Conexiones()
                self.__conexiones.append([server,propiedad,ofiVent])
                self.actualizar_Conexiones()
                self.__db.cerrarConexion()         
                return f"Conexion exitosa con: {server} en {propiedad}"           
            else:
                return f"Fallo conexion con: {server} en {propiedad}"
        return f"({server}) Esta conexion ya existe"



