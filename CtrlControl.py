from Conexion import *
from Archivos import *

#Clase encargada de la conexion a la base de datos
class CtrlConexion():    
    def __init__(self) -> None:        
        self.cargar_Conexiones()        
        self.__db=Conexion()        
        
    def cargar_Conexiones(self)->None:
        self.__conexiones=Archivos.leerArchivo()
        

    def actualizar_Conexiones(self,)->None:
        Archivos.guardarArchivo(self.__conexiones)
    
    def borrarConexion(self,ofiVent)->str:
        self.cargar_Conexiones()
        dat=self.buscarConexion(ofiVent)
        if dat!=None:
            for i in range(len(self.__conexiones)):
                if dat[0]==self.__conexiones[i][0]:
                    self.__conexiones.pop(i)
                    self.actualizar_Conexiones()
                    return f"Conexion '{dat[0]} de {dat[1]} Borrada' "
            return 'No se pudo borrar'
        return 'Esta conexion no existe'

    def modificarConexion(self,ofiVent,nuevoSName,nuevaPropiedad)->str:
        self.cargar_Conexiones()
        dat=self.buscarConexion(ofiVent)
        if dat!=None:
            if self.probarConexion(nuevoSName):
                for i in range(len(self.__conexiones)):
                    if dat[2]==self.__conexiones[i][2]:
                        self.__conexiones[i]=[nuevoSName,nuevaPropiedad,ofiVent]
                        self.actualizar_Conexiones()
                        return f"Modificado"            
                return "No se pudo modificar"
            return "Esta nueva conexion no funciona"
        return "Esta conexion no existe"
        
    
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

    def probarConexion(self,server)->bool:        
        if self.__db.conectar(server,'test conect','test conect'):
                return True
        return False
    
    def consultar(self,sName,sentencia)->list:
        self.__db.conectar(sName,"","")
        dat=self.__db.consulta(sentencia)
        return dat

if __name__=='__main__':
    p=CtrlConexion()
    datos=p.consultar('172.19.101.139\sqlexpress','select * from dbo.SAP_int')
    print(datos)