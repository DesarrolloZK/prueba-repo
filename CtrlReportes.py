from CtrlConexion import CtrlConexion as ctcon
from Archivos import Archivos as file
from Archivos import Archivos as arc
from calendar import monthrange as mr
from tkinter import messagebox
from datetime import datetime
import decimal

class CtrlReportes():
    #Metodo constructor
    #Aqui traemos la informacion del archivo de configuracion
    def __init__(self)->None:
        #self.__db=con()
        self.cargarConfig()
        self.cargar_ConeptoJerarquia()
        self.cargar_ConceptoJerarquiaDev()
        self.cargar_Definiciones()

    def cargarConfig(self):
        self.__ico=None
        self.__ctcon=ctcon()
        self.__consulta=None
        self.__hoy=datetime.now()
        conf=file().configuraciones()
        if len(conf)!=0:
            for i in conf:
                if i[0].upper()=='CONSULTA':self.__consulta=i[1]
                if i[0].upper()=='IMPUESTO CONSUMO':self.__ico=float(i[1])/100
            if (self.__ico or self.__consulta)==None:messagebox.showerror(message='Error grave en las configuraciones, por favor verificar arhivo',title='Error')
            else:messagebox.showinfo(message='Configuraciones cargadas correctamente',title='Inicio')
        else:messagebox.showerror(message='Error grave en las configuraciones, por favor verificar arhivo',title='Error')

    def cargar_ConeptoJerarquia(self)->None:
        self.__conJer=file.traerConcepJerar()
    
    def cargar_ConceptoJerarquiaDev(self)->None:
        self.__conJerDev=file.traerConcepJerarDev()
    
    def cargar_Definiciones(self)->None:
        self.__definicionesM=file.traerDefM()
        self.__definicionesMST=file.traerDefMST()

    def buscar_ConceptoJerarquia(self,jer)->list:
        self.cargar_ConeptoJerarquia()        
        for i in self.__conJer:
            if str(jer)==i[1]:                
                return [i[0],i[2]]
        return []
    
    def buscar_ConceptoJerquiaDev(self,jer)->list:
        self.cargar_ConceptoJerarquiaDev()      
        for i in self.__conJerDev:
            if str(jer)==i[1]:
                return [i[0],i[2]]
        return []

    def buscar_Definiciones(self,ofi,defsq)->list:
        def buscarMST(ofi,defsq)->list:
            for c in self.__definicionesMST:                
                if ofi==c[0] and str(defsq)==c[2]:                    
                    return [c[3],c[4]]
            return ['M','']
        for c in self.__definicionesM:
            if ofi==c[0] and c[2]=='1':               
                return buscarMST(ofi,defsq)
            if ofi==c[0] and c[2]=='0':
                return ['M','']

    def verificar_DiaAnterior(self,fecha)->bool:
        diaAnterior=self.__hoy.day-fecha.day==1 and fecha.hour>=3
        diaActual=self.__hoy.day==fecha.day and fecha.hour<3
        return diaAnterior or diaActual

    def verificar_MesAnterior(self,fecha)->bool:
        mesAnterior=self.__hoy.month-fecha.month==1
        ultimoDiaMes=fecha.day==mr(fecha.year,fecha.month)[1] and fecha.hour>=3
        diaActual=self.__hoy.month==fecha.month and self.__hoy.day==fecha.day and fecha.hour<3
        return (mesAnterior and ultimoDiaMes) or diaActual

    def verificar_AñoAnterior(self,fecha)->bool:
        añoAnterior=self.__hoy.year-fecha.year==1
        ultimoMesAño=fecha.month==12
        ultimoDiaMes=fecha.day==mr(fecha.year,fecha.month)[1] and fecha.hour>=3
        diaActual=self.__hoy.year==fecha.year and self.__hoy.month==fecha.month and self.__hoy.day==fecha.day and fecha.hour<3
        return (añoAnterior and ultimoMesAño and ultimoDiaMes) or diaActual

    def analizarDb(self,sName,prop,ofi,reporte):
        vtas=[]
        descuentos=[]
        datos=self.__ctcon.consultar(sName,self.__consulta)        
        print(f'----------------------{prop}----------------------------')
        try:
            for i in datos:
                if i[10]!=None:
                    if i[7]==2:descuentos.append([i[5],i[6]])
                    if i[7]==1:                    
                        if self.verificar_DiaAnterior(i[1]): vtas.append([i[0],i[1].strftime('%d%m%Y %H:%M'),i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]])
                        elif self.verificar_MesAnterior(i[1]): vtas.append([i[0],i[1].strftime('%d%m%Y %H:%M'),i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]])
                        elif self.verificar_AñoAnterior(i[1]): vtas.append([i[0],i[1].strftime('%d%m%Y %H:%M'),i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]])  
            vtas=self.ordenar_Infomacion(vtas,descuentos,ofi)
            #arc.consultaBruta(datos,prop,ofi,i[1].strftime('%d%m%Y'))
            if reporte:print(arc.reportes(vtas,prop,ofi,i[1].strftime('%d%m%Y')))
        except Exception as e:
            print(e)

    def ordenar_Infomacion(self,vtas,descuentos,ofi)->list:
        vtasf=[]
        propinas=self.suma_Propinas(vtas,ofi)
        descuentos=self.calcular_Descuentos(descuentos,ofi)
        vtas=self.sumar_Productos(vtas)
        vtas=self.eliminar_Ceros(vtas)
        vtasf=self.orden_Final(vtas,ofi)
        vtasf=self.adicionar_ConceptoJerarquia(vtasf)
        vtasf=self.adicionar_ConceptoJerarquiaDev(vtasf)
        vtasf=self.adicionar_Definiciones(vtasf)
        if len(propinas)>0:vtasf.append(propinas)
        if len(descuentos)>0:vtasf.append(descuentos)
        vtasf.append(self.adicionar_IpoConsumo(vtasf,ofi))
        return vtasf

    def orden_Final(self,vtas,ofi)->list:
        datos=[]
        for x in vtas: datos.append(['Concepto','10','00','MST',x[2],ofi,str(x[4]),x[3],x[5],x[6]])
        return datos

    def suma_Propinas(self,vtas,ofi)->list:
        sum=0       
        check=[]
        dat=[]       
        for c in vtas:
            if c[0] not in check:                
                check.append(c[0])
                dat.append(c)
        for c in dat:
            if c[8]!=None: sum+=c[8]
            if c[9]!=None: sum+=c[9]
        if sum==0: return[]
        return ['0007',10,'00','','',ofi,'','','',round(sum)]

    def sumar_Productos(self,datos)->list:
        totales=[]
        while len(datos)!=0:
            try:                                     
                if datos[0][2]==datos[1][2] and datos[0][3]==datos[1][3] and datos[0][4]==datos[1][4]:
                    datos[0][5]=datos[0][5]+datos[1][5]
                    datos[0][6]=datos[0][6]+datos[1][6]
                    datos.pop(1)                    
                else:
                    datos[0][5]=datos[0][5]
                    datos[0][6]=round(datos[0][6]/decimal.Decimal('1.08'))
                    totales.append(datos[0])
                    datos.pop(0)                    
            except IndexError:
                datos[0][5]=datos[0][5]
                datos[0][6]=round(datos[0][6]/decimal.Decimal('1.08'))
                totales.append(datos[0])
                return totales
            except TypeError:           
                if datos[0][5]==None: datos.pop(0)
                elif datos[1][5]==None: datos.pop(1)
                elif datos[0][6]==None: datos.pop(0)
                elif datos[1][6]==None: datos.pop(1)      
        return totales  

    def eliminar_Ceros(self,vtas)->list:
        i=0
        while i<len(vtas):
            if vtas[i][5]==0:
                vtas.pop(i)
                i-=1            
            i+=1
        return vtas

    def adicionar_ConceptoJerarquia(self,vtasf)->list:
        datos=[]
        for x in vtasf:
            if x[4]!=4 and x[4]!=7 and x[4]!=None:
                if x[4]==6 or x[4]==8:
                    aux=self.buscar_ConceptoJerarquia(1)
                    x[0]=aux[0]
                    x[4]=aux[1]
                    datos.append(x)
                else:
                    aux=self.buscar_ConceptoJerarquia(x[4])
                    if len(aux)>0:
                        x[0]=aux[0]
                        x[4]=aux[1]
                        datos.append(x)
        return datos

    def adicionar_ConceptoJerarquiaDev(self,vtasf)->list:
        for x in vtasf:
            if x[7]<0 and x[8]<0:
                aux=self.buscar_ConceptoJerquiaDev(x[4])                
                x[0]=aux[0]
                x[4]=aux[1]
                x[7]=x[7]*-1
                x[8]=x[8]*-1
        return vtasf

    def adicionar_Definiciones(self,vtasf)->list:
        for x in vtasf:
            aux=self.buscar_Definiciones(x[5],x[6])
            x[3]=aux[0]
            x[6]=aux[1]
        return vtasf
    
    def calcular_Descuentos(self,descuentos,ofi)->list:
        aux=[0,0]
        for x in descuentos:
            if x[0]!=None:aux[0]+=x[0]
            if x[1]!=None:aux[1]+=x[1]
        if (aux[0] and aux[1])>0: return ['0014',10,'00','','',ofi,'',3,aux[0],round(aux[1]*-1)]
        return []

    def adicionar_IpoConsumo(self,vtasf,ofi)->list:
        sum=0
        for c in vtasf:
            sum+=c[9]
        sum=round(sum*self.__ico)
        return ['0005',10,'00','','',ofi,'','','',sum]

    def rutina(self):
        puntos=ctcon().getConexiones()
        for i in puntos:
            self.analizarDb(i[0],i[1],i[2],True)
        
if __name__=='__main__':
    prueba=CtrlReportes()
    prueba.rutina()