import pyodbc
from Conexion import *
from Archivos import *
#Clase encargada de la conexion a la base de datos
class CtrlConexion():
    
    def __init__(self) -> None:        
        self.cargar_Conexiones()        
        self.__db=Conexion()        
        
    def cargar_Conexiones(self)->None:
        self.__conexiones=Archivos.leerArchivo()

    def actualizar_Conexiones(self)->None:
        Archivos.guardarArchivo(self.__conexiones)
    
    def borrarConexion(self,sName)->bool:
        self.cargar_Conexiones()
        for i in self.__conexiones:
            if sName==i[0]:
                self.__conexiones.pop(i[0])
                self.actualizar_Conexiones()
                return True
        return False
    
    def actualizarConexion(self,ofiVent,nuevoSName,nuevaPropiedad)->str:
        self.cargar_Conexiones()        
        pass
    
    def buscarConexion(self,ofiVent)->list:
        self.cargar_Conexiones()
        for i in self.__conexiones:
            if ofiVent==i[2]:
                return i
        return None

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

    def probarConexion(self,ofiVent)->str:
        con=self.buscarConexion(ofiVent)
        if con!=None:
            if self.__db.conectar(con[0],con[1],con[2]):
                return 'conectado'
        else:
            return 'Esta conexion no existe'

p=CtrlConexion()
print(p.probarConexion('1305'))