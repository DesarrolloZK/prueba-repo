from Conexion import *
from Archivos import *
import datetime
from pandas import DataFrame as df

class CtrlConexion():    
    def __init__(self) -> None:        
        self.cargar_Conexiones()
        self.cargar_Transac()
        self.cargar_ConJer()
        self.__db=Conexion()
        self.__consulta='SELECT dbo.CHECKS.CheckNumber, dbo.CHECK_DETAIL.DetailPostingTime, dbo.MAJOR_GROUP.ObjectNumber AS Expr1, dbo.CHECK_DETAIL.ObjectNumber AS PPD, dbo.MENU_ITEM_DETAIL.DefSequenceNum, dbo.CHECK_DETAIL.SalesCount, dbo.CHECK_DETAIL.Total, dbo.CHECK_DETAIL.DetailType, dbo.CHECKS.AutoGratuity, dbo.CHECKS.Other, dbo.CHECKS.SubTotal FROM dbo.CHECKS INNER JOIN dbo.CHECK_DETAIL INNER JOIN dbo.MENU_ITEM_DETAIL ON dbo.CHECK_DETAIL.CheckDetailID = dbo.MENU_ITEM_DETAIL.CheckDetailID ON dbo.CHECKS.CheckID = dbo.CHECK_DETAIL.CheckID INNER JOIN dbo.MENU_ITEM_DEFINITION ON dbo.MENU_ITEM_DETAIL.MenuItemDefID = dbo.MENU_ITEM_DEFINITION.MenuItemDefID INNER JOIN dbo.MAJOR_GROUP INNER JOIN dbo.MENU_ITEM_MASTER ON dbo.MAJOR_GROUP.ObjectNumber = dbo.MENU_ITEM_MASTER.MajGrpObjNum ON dbo.MENU_ITEM_DEFINITION.MenuItemMasterID = dbo.MENU_ITEM_MASTER.MenuItemMasterID ORDER BY PPD'
        #self.__consulta2='SELECT dbo.MENU_ITEM_MASTER.ObjectNumber, dbo.MENU_ITEM_PRICE.MenuItemPriceID, dbo.MENU_ITEM_PRICE.SequenceNum, dbo.MENU_ITEM_PRICE.Price, dbo.MENU_ITEM_DEFINITION.SubLvl, dbo.MENU_ITEM_DEFINITION.MainLvl, dbo.MENU_ITEM_DEFINITION.SequenceNum AS Expr1, dbo.HIERARCHY_STRUCTURE.HierStrucID AS Expr3, dbo.MENU_ITEM_PRICE.HierStrucID, dbo.HIERARCHY_UNIT.RevCtrID, dbo.HIERARCHY_UNIT.PropertyID, dbo.HIERARCHY_UNIT.HierUnitID, dbo.REVENUE_CENTER.ObjectNumber AS Expr2, dbo.MENU_ITEM_PRICE.MenuItemDefID FROM dbo.REVENUE_CENTER RIGHT OUTER JOIN                      dbo.HIERARCHY_UNIT ON dbo.REVENUE_CENTER.RevCtrID = dbo.HIERARCHY_UNIT.RevCtrID LEFT OUTER JOIN dbo.HIERARCHY_STRUCTURE INNER JOIN dbo.MENU_ITEM_MASTER INNER JOIN dbo.MENU_ITEM_DEFINITION ON dbo.MENU_ITEM_MASTER.MenuItemMasterID = dbo.MENU_ITEM_DEFINITION.MenuItemMasterID INNER JOIN dbo.MENU_ITEM_PRICE ON dbo.MENU_ITEM_DEFINITION.MenuItemDefID = dbo.MENU_ITEM_PRICE.MenuItemDefID ON dbo.HIERARCHY_STRUCTURE.HierStrucID = dbo.MENU_ITEM_PRICE.HierStrucID ON dbo.HIERARCHY_UNIT.HierUnitID = dbo.HIERARCHY_STRUCTURE.HierUnitID'
        self.__hoy=datetime.datetime.now()

    def cargar_Conexiones(self)->None:
        self.__conexiones=Archivos.traerConexiones()

    def cargar_Transac(self):
        self.__transacciones=Archivos.traerDefiniciones()

    def cargar_ConJer(self):
        self.__conceptJerar=Archivos.traerConcepJerar()

    def buscarConJer(self,jer)->list:
        self.cargar_ConJer()
        for i in self.__conceptJerar:
            if jer==i[1]: 
                return [i[0],i[2]]
        return []

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
            
    def buscarConexion(self,sName,prop,ofi)->list:
        self.cargar_Conexiones()
        for i in self.__conexiones:            
            if sName==i[0] or prop==i[1] or ofi==i[2]:                
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
        return self.__db.conectar(server,'test conect','test conect')           
    
    def consultar(self,sName,sentencia)->list:
        if self.probarConexion(sName):
            return self.__db.consulta(sentencia)
        return []
    
    def ordArchDia(self,sName,prop,ofi,repDia)->None:
        fFile=list()
        print(f'----------------------{prop}----------------------------')
        datos=p.consultar(sName,self.__consulta)                                       
        for i in range(len(datos)):
            if datos[i][7]==1 and datos[i][10]!=None:
                if (self.__hoy.day-datos[i][1].day==1 and datos[i][1].hour>=3) or (self.__hoy.day-datos[i][1].day==0 and datos[i][1].hour<3):  
                    fFile.append([datos[i][0],datos[i][1],datos[i][2],datos[i][3],datos[i][4],datos[i][5],datos[i][6],datos[i][7],datos[i][8],datos[i][9]])                
                    fecha=datos[i][1]
        fFile=self.sumaTotal(fFile)
        fFile=self.delCeros(fFile)
        self.ordenarArchivo(fFile,ofi)
        #self.ordenarArchivo(fFile,ofi)       
        #Archivos.escArchDia(self.sumaTotal(fFile),prop,ofi,fecha.strftime('%m%Y'))
        #if repDia:
        #    Archivos.reportes(self.sumaTotal(fFile),prop,ofi,fecha.strftime('%d%m%Y'))        
        # fFile.append(['concepto',10,'00','MST','JERARQUIA',ofi,'ofi prod',datos[i][3],datos[i][5],datos[i][6]])  
       
        
        
    def sumaTotal(self,datos)->list:
        totales=list()
        try:               
            while len(datos)>0:
                if datos[0][6] != None and datos[1][6] != None:                                                
                    if datos[0][2]==datos[1][2] and datos[0][3]==datos[1][3] and datos[0][4]==datos[1][4]:
                        datos[0][5]=datos[0][5]+datos[1][5]
                        datos[0][6]=datos[0][6]+datos[1][6]
                        datos.pop(1)
                    else:
                        datos[0][5]=round(datos[0][5])
                        datos[0][6]=round(datos[0][6])
                        totales.append(datos[0])
                        datos.pop(0)
                    if len(datos)==1:
                        datos[0][5]=round(datos[0][5])
                        datos[0][6]=round(datos[0][6])
                        totales.append(datos[0])
                elif datos[0][6] == None:
                    datos.pop(0)
                elif datos[1][6] == None:
                    datos.pop(1)           
        except IndexError as ie:
            datos[0][5]=round(datos[0][5])
            datos[0][6]=round(datos[0][6])
            totales.append(datos[0])
            return totales
    
    def delCeros(self,datos)->list:
        dat=list()
        for i in range(len(datos)):
            if datos[i][5]!=0:
                dat.append(datos[i])
        return dat
    
    def ordenarArchivo(self,datos,ofi)->list:
        dat=list()
        for i in datos:
            dat.append(['Concepto',10,'00','MST',i[2],ofi,'ofi prod',i[3],i[5],i[6]])
        dat=self.modNegativos(dat)
        for c in dat:
            print(c)

    def modNegativos(self,datos)->list:
        for i in range(len(datos)):
            if datos[i][7]<0 and datos[i][8]<0:
                aux=self.buscarConJer(datos[i][4])
                datos[i][0]=aux[0]
                datos[i][4]=aux[1]
                datos[i][7]=datos[i][7]*-1
                datos[i][8]=datos[i][8]*-1
        return datos

    def unoDiezReportes(self): 
        try:
            for i in os.listdir('Consultas/'):                                       
                datos=list()          
                for j in os.listdir(f'Consultas/{i}'):                                                
                    f=os.path.join(f'Consultas/{i}/',j)                               
                    if os.path.isfile(f) and j.endswith('.txt'):                    
                        with open(f,'r') as txtfile:
                            aux=txtfile.readlines()                                                                               
                            for k in aux:
                                datos.append(k.replace('\n','').split(';'))
                            txtfile.close()
                aux2=self.buscarConexion('',i.split('-')[0],'')
                fecha=datetime.datetime.strptime(datos[len(datos)-1][1],'%d%m%Y %H:%M')
                fecha=fecha.strftime('%d%m%Y')                
                Archivos.reportes(datos,aux2[1],aux2[2],fecha)
        except Exception as e:
            print(f'Error: {e}')

    def rutina(self):
        self.__hoy=datetime.datetime.now()
        for i in self.__conexiones:
            if self.__hoy.day<11:
                self.ordArchDia(i[0],i[1],i[2],False)
            elif self.__hoy.day==11:
                self.ordArchDia(i[0],i[1],i[2],False)
                self.unoDiezReportes()
            elif self.__hoy.day>11:
                self.ordArchDia(i[0],i[1],i[2],True)
            else:
                print('Error inesperado')

    def getConexiones(self)->list():
        self.cargar_Conexiones()
        return self.__conexiones

if __name__=='__main__':
    p=CtrlConexion()
    p.rutina()
    
    
   