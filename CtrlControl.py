from calendar import monthrange
from tkinter import messagebox
from Conexion import *
from Archivos import *
import datetime


class CtrlConexion():    
    def __init__(self) -> None:        
        self.cargar_Conexiones()        
        self.cargar_ConJer()
        self.cargar_Definiciones()
        self.__db=Conexion()
        self.__consulta='SELECT dbo.CHECKS.CheckNumber, dbo.CHECK_DETAIL.DetailPostingTime, dbo.MAJOR_GROUP.ObjectNumber AS Expr1, dbo.CHECK_DETAIL.ObjectNumber AS PPD, dbo.MENU_ITEM_DETAIL.DefSequenceNum, dbo.CHECK_DETAIL.SalesCount, dbo.CHECK_DETAIL.Total, dbo.CHECK_DETAIL.DetailType, dbo.CHECKS.AutoGratuity, dbo.CHECKS.Other, dbo.CHECKS.SubTotal FROM dbo.MENU_ITEM_DETAIL INNER JOIN dbo.MENU_ITEM_DEFINITION ON dbo.MENU_ITEM_DETAIL.MenuItemDefID = dbo.MENU_ITEM_DEFINITION.MenuItemDefID INNER JOIN dbo.MAJOR_GROUP INNER JOIN dbo.MENU_ITEM_MASTER ON dbo.MAJOR_GROUP.ObjectNumber = dbo.MENU_ITEM_MASTER.MajGrpObjNum ON dbo.MENU_ITEM_DEFINITION.MenuItemMasterID = dbo.MENU_ITEM_MASTER.MenuItemMasterID RIGHT OUTER JOIN dbo.CHECK_DETAIL INNER JOIN dbo.CHECKS ON dbo.CHECK_DETAIL.CheckID = dbo.CHECKS.CheckID ON dbo.MENU_ITEM_DETAIL.CheckDetailID = dbo.CHECK_DETAIL.CheckDetailID ORDER BY PPD'
        #self.__consultaold='SELECT dbo.CHECKS.CheckNumber, dbo.CHECK_DETAIL.DetailPostingTime, dbo.MAJOR_GROUP.ObjectNumber AS Expr1, dbo.CHECK_DETAIL.ObjectNumber AS PPD, dbo.MENU_ITEM_DETAIL.DefSequenceNum, dbo.CHECK_DETAIL.SalesCount, dbo.CHECK_DETAIL.Total, dbo.CHECK_DETAIL.DetailType, dbo.CHECKS.AutoGratuity, dbo.CHECKS.Other, dbo.CHECKS.SubTotal FROM dbo.CHECKS INNER JOIN dbo.CHECK_DETAIL INNER JOIN dbo.MENU_ITEM_DETAIL ON dbo.CHECK_DETAIL.CheckDetailID = dbo.MENU_ITEM_DETAIL.CheckDetailID ON dbo.CHECKS.CheckID = dbo.CHECK_DETAIL.CheckID INNER JOIN dbo.MENU_ITEM_DEFINITION ON dbo.MENU_ITEM_DETAIL.MenuItemDefID = dbo.MENU_ITEM_DEFINITION.MenuItemDefID INNER JOIN dbo.MAJOR_GROUP INNER JOIN dbo.MENU_ITEM_MASTER ON dbo.MAJOR_GROUP.ObjectNumber = dbo.MENU_ITEM_MASTER.MajGrpObjNum ON dbo.MENU_ITEM_DEFINITION.MenuItemMasterID = dbo.MENU_ITEM_MASTER.MenuItemMasterID ORDER BY PPD'
        self.__hoy=datetime.datetime.now()

    def cargar_Conexiones(self)->None:
        self.__conexiones=Archivos.traerConexiones()

    def cargar_Definiciones(self)->None:
        self.__defM=Archivos.traerDefM()
        self.__defMST=Archivos.traerDefMST()

    def cargar_ConJer(self):
        self.__conceptJerar=Archivos.traerConcepJerar()

    def cargar_ConJerDev(self):
        self.__conceptJerarDev=Archivos.traerConcepJerarDev()

    def buscarConJer(self,jer)->list:
        self.cargar_ConJer()        
        for i in self.__conceptJerar:
            if str(jer)==i[1]:
                
                return [i[0],i[2]]
        return []
    
    def buscarConJerDev(self,jer)->list:
        self.cargar_ConJerDev()        
        for i in self.__conceptJerarDev:
            if str(jer)==i[1]:
                return [i[0],i[2]]
        return []

    def buscarDefM(self,ofi,defsq)->list:
        def buscarDefMST(ofi,defsq)->list:
            for c in self.__defMST:
                if ofi==c[0] and str(defsq)==c[2]:                    
                    return [c[3],c[4]]
            return ['M',ofi]

        for c in self.__defM:
            if ofi==c[0] and c[2]=='1':               
                return buscarDefMST(ofi,defsq)
            if ofi==c[0] and c[2]=='0':
                return ['M',ofi]

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
        disc=list()
        print(f'----------------------{prop}----------------------------')
        datos=p.consultar(sName,self.__consulta)                                       
        for i in range(len(datos)):            
            if datos[i][7]==1 and datos[i][10]!=None:
                if (self.__hoy.day-datos[i][1].day==1 and datos[i][1].hour>=3) or (self.__hoy.day-datos[i][1].day==0 and datos[i][1].hour<3):  
                    fFile.append([datos[i][0],datos[i][1],datos[i][2],datos[i][3],datos[i][4],datos[i][5],datos[i][6],datos[i][7],datos[i][8],datos[i][9]])                   
                elif self.__hoy.month>datos[i][1].month and datos[i][1].day==monthrange(self.__hoy.year,datos[i][1].month)[1]:
                    fFile.append([datos[i][0],datos[i][1],datos[i][2],datos[i][3],datos[i][4],datos[i][5],datos[i][6],datos[i][7],datos[i][8],datos[i][9]])
                elif self.__hoy.year>datos[i][1].year and datos[i][1].day==monthrange(datos[i][1].year,datos[i][1].month)[1]:
                    fFile.append([datos[i][0],datos[i][1],datos[i][2],datos[i][3],datos[i][4],datos[i][5],datos[i][6],datos[i][7],datos[i][8],datos[i][9]])
            if datos[i][7]==2:
                disc.append(datos[i][6])
        fFile=self.totales(fFile,list())
        fFile=self.delCeros(fFile)
        self.ordenarArchivo(fFile,ofi)        
        #Archivos.escArchDia(self.sumaTotal(fFile),prop,ofi,fecha.strftime('%m%Y'))
        #if repDia:
        #    Archivos.reportes(self.sumaTotal(fFile),prop,ofi,fecha.strftime('%d%m%Y'))        
        # fFile.append(['concepto',10,'00','MST','JERARQUIA',ofi,'ofi prod',datos[i][3],datos[i][5],datos[i][6]])  
   
    def totales(self,datos,totales)->list:
        while len(datos)!=0:
            try:                                     
                if datos[0][2]==datos[1][2] and datos[0][3]==datos[1][3] and datos[0][4]==datos[1][4]:
                    datos[0][5]=datos[0][5]+datos[1][5]
                    datos[0][6]=datos[0][6]+datos[1][6]
                    datos.pop(1)                    
                else:
                    #print('prueba')
                    datos[0][5]=datos[0][5]
                    datos[0][6]=round(round(datos[0][6])/1.08)
                    totales.append(datos[0])
                    datos.pop(0)                    
            except IndexError:
                #print('prueba')
                datos[0][5]=datos[0][5]
                datos[0][6]=round(round(datos[0][6])/1.08)
                totales.append(datos[0])
                return totales
            except TypeError:
                #print('Error')
                if datos[0][5]==None: datos.pop(0)
                elif datos[1][5]==None: datos.pop(1)
                elif datos[0][6]==None: datos.pop(0)
                elif datos[1][6]==None: datos.pop(1)                  
        return totales
    
    def delCeros(self,datos)->list:
        i=0
        while i <len(datos):
            if datos[i][5]==0:
                datos.pop(i)
                i-=1            
            i+=1
        return datos
    
    def ordenarArchivo(self,datos,ofi):
        dat=list()
        for i in datos:
            dat.append(['Concepto',10,'00','MST',i[2],ofi,str(i[4]),i[3],i[5],i[6]])
        dat=self.addConJer(dat)
        dat=self.addConJerDev(dat)
        dat=self.addDefM(dat)
        props=self.orgPropinas(datos,ofi)
        if len(props)>0:
            dat.append(props)
        for c in dat:
            print(c)

    def orgPropinas(self,datos,ofi)->list:
        sum=0       
        check=[]
        dat=[]       
        for c in range(len(datos)):
            if datos[c][0] not in check:                
                check.append(datos[c][0])
                dat.append(datos[c])
               
        for c in dat:
            if c[8]!=None: sum+=c[8]
            if c[9]!=None: sum+=c[9]
        if sum==0: return[]
        return ['0007',10,'00','','',ofi,'','','',round(sum)]

    def addConJer(self,datos):
        c=0
        while c!=len(datos):
            if datos[c][4]==4:
                datos.pop(c)
                c-=1
            elif datos[c][4]==6:
                aux=self.buscarConJer(1)
                datos[c][0]=aux[0]
                datos[c][4]=aux[1]
                c+=1        
            elif datos[c][4]==7:
                datos.pop(c)
                c-=1
            elif datos[c][4]==8:
                aux=self.buscarConJer(1)
                datos[c][0]=aux[0]
                datos[c][4]=aux[1]
                c+=1
            else:
                aux=self.buscarConJer(datos[c][4])
                if len(aux)!=0:
                    datos[c][0]=aux[0]
                    datos[c][4]=aux[1]
                c+=1
        return datos

    def addConJerDev(self,datos)->list:
        for i in range(len(datos)):
            if datos[i][7]<0 and datos[i][8]<0:
                aux=self.buscarConJerDev(datos[i][4])                
                datos[i][0]=aux[0]
                datos[i][4]=aux[1]
                datos[i][7]=datos[i][7]*-1
                datos[i][8]=datos[i][8]*-1
        return datos

    def addDefM(self,datos):
        for c in range(len(datos)):
            aux=self.buscarDefM(datos[c][5],datos[c][6])
            datos[c][3]=aux[0]
            datos[c][6]=aux[1]
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
    
    
    
   