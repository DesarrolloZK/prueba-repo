from Conexion import *
from Archivos import *
import datetime
from pandas import DataFrame as df
#Clase encargada de la conexion a la base de datos
class CtrlConexion():    
    def __init__(self) -> None:        
        self.cargar_Conexiones()
        self.cargar_Transac()       
        self.__db=Conexion()
        self.__consulta='SELECT dbo.CHECKS.CheckNumber, dbo.CHECK_DETAIL.DetailPostingTime,dbo.MAJOR_GROUP.ObjectNumber AS Expr1, dbo.CHECK_DETAIL.ObjectNumber AS PPD,dbo.MENU_ITEM_DETAIL.DefSequenceNum,dbo.CHECK_DETAIL.SalesCount, dbo.CHECK_DETAIL.Total,dbo.CHECK_DETAIL.DetailType FROM dbo.MENU_ITEM_DETAIL RIGHT OUTER JOIN dbo.CHECK_DETAIL LEFT OUTER JOIN dbo.CHECKS ON dbo.CHECK_DETAIL.CheckID = dbo.CHECKS.CheckID ON dbo.MENU_ITEM_DETAIL.CheckDetailID = dbo.CHECK_DETAIL.CheckDetailID LEFT OUTER JOIN dbo.MENU_ITEM_DEFINITION ON dbo.MENU_ITEM_DETAIL.MenuItemDefID = dbo.MENU_ITEM_DEFINITION.MenuItemDefID LEFT OUTER JOIN dbo.MAJOR_GROUP INNER JOIN dbo.MENU_ITEM_MASTER ON dbo.MAJOR_GROUP.ObjectNumber = dbo.MENU_ITEM_MASTER.MajGrpObjNum ON dbo.MENU_ITEM_DEFINITION.MenuItemMasterID = dbo.MENU_ITEM_MASTER.MenuItemMasterID'


    def cargar_Conexiones(self)->None:
        self.__conexiones=Archivos.traerConexiones()

    def cargar_Transac(self):
        self.__transacciones=Archivos.traerTransacciones()

    def buscarTransac(self,ofiVentas,fuente)->str:
        for i in self.__transacciones:
            if i[0]==ofiVentas and i[2]==fuente:
                return i[3]

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
            
    def buscarConexion(self,sName)->list:
        self.cargar_Conexiones()
        for i in self.__conexiones:
            if sName==i[0]:
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
        if self.probarConexion(sName):
            return self.__db.consulta(sentencia)
        return []
    
    def make_Final_File(self)->list:
        try:            
            datos=p.consultar('172.19.71.21\\sqlexpress',self.__consulta)
            rest=self.buscarConexion('172.19.71.21\\sqlexpress')
            fFile=list()
            for i in datos:
                if i[7]==1:
                    hoy=datetime.datetime.now()
                    date=i[1]        
                    if (hoy.day-i[1].day==1 and i[1].hour>=3) or (hoy.day-i[1].day==0 and i[1].hour<3):
                        fFile.append([f'000{i[2]}',10,00,i[2],self.buscarTransac(rest[1],i[4]),f'000{i[2]}','Prueba',i[3],i[5]])

            
            print(Archivos.finalFile(fFile,rest[1],rest[2],date))

        except IndexError as ie:
            print(str(ie))

if __name__=='__main__':
    p=CtrlConexion()
    p.make_Final_File()
   