from CtrlConexion import CtrlConexion as ctcon
from calendar import monthrange as mr
from Archivos import Archivos as file
from Archivos import Archivos as arc
from datetime import datetime as dt
from tkinter import messagebox
from datetime import timedelta
import time
import decimal

class CtrlReportes():
    #Metodo constructor
    #Aqui traemos la informacion del archivo de configuracion
    def __init__(self)->None:
        self.reloj()

    def reloj(self):
        self.__hoy=dt.now()
        h=self.__hoy.hour
        if 3<=h<=17:print(self.rutina())
        time.sleep(3600)
        self.reloj()

    def comprobar_Reportes(self,prop,ofi)->bool:
        lista=file.traerNombreReportes(prop,ofi)
        for x in lista:
            if dt.strptime(x.split(f'VTAS{ofi}')[1].split('.txt')[0],'%d%M%Y').day==dt.now().day-1: return False
        return True

    def cargarConfig(self)->None:
        if len(self.__conf)!=0:
            self.__consulta=None
            self.__valIpoC=None
            self.__ipFtp=None
            self.__userFtp=None
            self.__passFtp=None
            self.__valConJer=[]
            self.__valConJerDev=[]
            self.__ctcon=ctcon()
            self.cargar_ConceptoJerarquia()
            self.cargar_ConceptoJerarquiaDev()
            self.cargar_Definiciones()
            for x in self.__conf:
                print(f'{x[0]}:{x[1]}')
                if x[0].upper()=='QUERY':self.__consulta=x[1]
                elif x[0].upper()=='IPOCONSUMO':self.__valIpoC=decimal.Decimal(x[1])/100
                elif x[0].upper()=='FTP':self.__ipFtp=x[1]
                elif x[0].upper()=='USUARIO':self.__userFtp=x[1]
                elif x[0].upper()=='PASSWORD':self.__passFtp=x[1]
                
            if (self.__consulta or self.__valIpoC or self.__ipFtp or self.__userFtp or self.__passFtp)==None: print('Es posible que el archivo de confifuraciones este incompleto')
        else:
            print('Sin configuraciones:D')

    def cargar_ConceptoJerarquia(self)->None:
        self.__conJer=file.traerConcepJerar()
        for x in self.__conJer:
            if x[4]!='0': self.__valConJer.append([x[0],x[4]])
    
    def cargar_ConceptoJerarquiaDev(self)->None:
        self.__conJerDev=file.traerConcepJerarDev()
        for y in self.__conJerDev:
            if y[4]!='0': self.__valConJerDev.append([y[0],y[4]])
    
    def cargar_Definiciones(self)->None:
        self.__definicionesM=file.traerDefM()
        self.__definicionesMST=file.traerDefMST()

    def buscar_ConceptoJerarquia(self,jer)->list:
        self.cargar_ConceptoJerarquia()        
        for i in self.__conJer:
            if str(jer)==i[1]:                
                return i
            if str(jer)=='None':
                return self.buscar_ConceptoJerarquia(1)
        return []
    
    def buscar_ConceptoJerquiaDev(self,jer)->list:
        self.cargar_ConceptoJerarquiaDev()      
        for i in self.__conJerDev:
            if str(jer)==i[1]:
                return i
        return []

    def buscar_ValConcepto(self,conc)->decimal.Decimal:
        conceptos=self.__valConJer+self.__valConJerDev
        for x in conceptos:
            if x[0]==conc:
                if x[1]=='-1':return decimal.Decimal(x[1].replace('-',''))
                elif x[1]!='0': return decimal.Decimal(x[1])/decimal.Decimal('100')
        return decimal.Decimal('0.08')

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

    def verificar_DiaActual(self,fecha)->bool:
        return self.__hoy.day==fecha.day and fecha.hour<=3

    def verificar_DiaAnterior(self,fecha)->bool:
        return self.__hoy.day-fecha.day==1 and fecha.hour>=3

    def verificar_MesAnterior(self,fecha)->bool:
        mesAnterior=self.__hoy.month-fecha.month==1
        ultimoDiaMes=fecha.day==mr(fecha.year,fecha.month)[1] and fecha.hour>=3
        cambio=self.__hoy.day<2
        return mesAnterior and ultimoDiaMes and cambio

    def verificar_AnioAnterior(self,fecha)->bool:
        anioAnterior=self.__hoy.year-fecha.year==1
        ultimoMesAnio=fecha.month==12
        ultimoDiaMes=fecha.day==mr(fecha.year,fecha.month)[1] and fecha.hour>=3
        cambio=self.__hoy.day<2
        return anioAnterior and ultimoMesAnio and ultimoDiaMes and cambio

    def del_Reportes(self)->None:
        pass

    def analizarDb(self,sName,prop,ofi,reporte,reportes)->None:
        try:
            vtas=[]
            consultaDia=[]
            datos=self.__ctcon.consultar(sName,self.__consulta)
            for i in datos:
                if i[10]!=None:
                    bandera=self.verificar_DiaActual(i[1]) or self.verificar_DiaAnterior(i[1]) or self.verificar_MesAnterior(i[1]) or self.verificar_AnioAnterior(i[1])
                    if (i[7]==1 or i[7]==2) and bandera:
                        consultaDia.append(i)
                        vtas.append([i[0],i[1].strftime('%d%m%Y %H:%M'),i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
            print(arc.escribirConsulta(datos,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d-%m-%Y'),'Bruta'))
            print(arc.escribirConsulta(consultaDia,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d-%m-%Y'),'Diaria'))
            if len(vtas)!=0:
                if reporte:
                    vtas=self.ordenar_Infomacion(vtas,ofi)
                    print(arc().reportes(vtas,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d%m%Y'),self.__ipFtp,self.__userFtp,self.__passFtp))
                if reportes:
                    del vtas
                    vtas=arc.traerConsultaDiaria(prop,ofi)
                    vtas=self.convertir_Datos(vtas)
                    vtas=self.ordenar_Infomacion(vtas,ofi)
                    print(arc().reportes(vtas,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d%m%Y'),self.__ipFtp,self.__userFtp,self.__passFtp))
            else: print('No hay datos para Crear el reporte')
        except Exception as e:
            print(f'Error en el analisis de la Db\n Descripcion: {e}')

    def convertir_Datos(self,vtas)->list:
        datos=[]
        for x in vtas:
            if x[0]!='None':x[0]=int(x[0])
            else:x[0]=None
            if x[1]=='None':x[1]=None
            if x[2]!='None':x[2]=int(x[2])
            else:x[2]=None
            if x[3]!='None':x[3]=int(x[3])
            else:x[3]=None
            if x[4]!='None':x[4]=int(x[4])
            else:x[4]=None
            if x[5]!='None':x[5]=int(x[5])
            else:x[5]=None
            if x[6]!='None':x[6]=int(decimal.Decimal(x[6]))
            else:x[6]=None
            if x[7]!='None':x[7]=int(x[7])
            else:x[7]=None
            if x[8]!='None':x[8]=int(decimal.Decimal(x[8]))
            else:x[8]=None
            if x[9]!='None':x[9]=int(decimal.Decimal(x[9]))
            else:x[9]=None
            if x[10]!='None':x[10]=int(decimal.Decimal(x[10]))
            else:x[10]=None
            datos.append(x)
        return datos

    def ordenar_Infomacion(self,vtas,ofi)->list:
        vtasf=[]
        self.__icoTotal=0
        vtas=self.filtrar_Ppds(vtas)
        propinas=self.suma_Propinas(vtas,ofi)
        descuentos=self.extraer_Descuentos(vtas)
        descuentos=self.calcular_Descuentos(descuentos,ofi)
        vtas=self.sumar_Productos(vtas)
        if ofi=='1320':vtas=self.arreglar_Sushis(vtas,False)
        elif ofi=='1355':
            propinas=[]
            descuentos=[]
            vtas=self.arreglar_Sushis(vtas,True)
        vtasf=self.orden_Final(vtas,ofi)
        vtasf=self.adicionar_ConceptoJerarquia(vtasf)
        vtasf=self.adicionar_ConceptoJerarquiaDev(vtasf)
        vtasf=self.calcular_Quitar_Ico(vtasf)
        vtasf=self.eliminar_Ceros(vtasf)
        vtasf=self.adicionar_Definiciones(vtasf)
        vtasf.append(self.adicionar_IpoConsumo(ofi))
        if len(propinas)>0:vtasf.append(propinas)
        if len(descuentos)>0:vtasf.append(descuentos)
        vtasf=self.arreglar_Domicilios(vtasf)
        return vtasf

    def filtrar_Ppds(self,vtas)->list:
        datos=[]
        for x in vtas:
            if x[7]==2 or x[3]>99999:
                datos.append(x)
        return datos

    def suma_Propinas(self,vtas,ofi)->list:
        sum=0       
        check=[]
        dat=[]
        aux=self.buscar_ConceptoJerarquia('prop')
        if len(aux)==0: aux=self.buscar_ConceptoJerquiaDev('prop') 
        for c in vtas:
            if c[0] not in check:                
                check.append(c[0])
                dat.append(c)
        for c in dat:
            if c[8]!=None: sum+=c[8]
            if c[9]!=None: sum+=c[9]
        if sum==0: return[]
        return [aux[0],'10','00','',aux[2],ofi,'','','',round(sum)]

    def extraer_Descuentos(self,vtas)->list:
        datos=[]
        for x in vtas:
            if x[7]==2:
                if (x[5] and x[6])!=None: datos.append([x[5],x[6]])
        return datos

    def calcular_Descuentos(self,descuentos,ofi)->list:
        self.__ipoDescuento=0
        aux=[0,0]
        for x in descuentos:
            aux[0]+=x[0]
            aux[1]+=x[1]
        if (aux[0] and aux[1])!=0:
            aux[1]=abs(round(aux[1]/(1+self.__valIpoC)))
            self.__ipoDescuento=aux[1]*self.__valIpoC
            aux1=self.buscar_ConceptoJerarquia('disc')
            datos=self.adicionar_Definiciones([[aux1[0],'10','00','',aux1[2],ofi,'',aux1[6],aux[0],aux[1]]])
            return datos[0]
        return []

    def sumar_Productos(self,vtas)->list:
        ppds=[]
        datos=[]
        for x in vtas:
            if (x[5] and x[6])!=None:
                if x[3]!=3:
                    if len(ppds)==0:
                        ppds.append(x[3])
                        datos.append(x)
                    elif x[3]in ppds:
                        for y in datos:
                            if x[3]==y[3]:
                                y[5]+=x[5]
                                y[6]+=x[6]
                    else:
                        ppds.append(x[3])
                        datos.append(x)
        return datos

    def arreglar_Sushis(self,vtas,bandera)->list:
        datos=[]
        for x in vtas:
            if bandera:
                if x[2]==8:datos.append(x)
            else:
                if x[2]!=8:datos.append(x)
        return datos

    def orden_Final(self,vtas,ofi)->list:
        datos=[]
        for x in vtas:
            datos.append(['Concepto','10','00','MST',x[2],ofi,str(x[4]),x[3],x[5],x[6]])
        return datos

    def adicionar_ConceptoJerarquia(self,vtasf)->list:
        datos=[]
        aparte=[]
        for x in vtasf:
            if x[8]<0 or x[9]<0:
                datos.append(x)
                continue
            aux=self.buscar_ConceptoJerarquia(x[4])
            if len(aux)!=0:
                if aux[5]=='n':
                    x[0]=aux[0]
                    x[4]=aux[2]
                    datos.append(x)
                elif aux[5]=='s':
                    if len(aparte)!=0:
                        bandera=True
                        for y in aparte:
                            if y[0]==aux[0] and y[4]==aux[2]:
                                y[8]+=x[8]
                                y[9]+=x[9]
                                bandera=False
                                break
                        if bandera:
                            x[0]=aux[0]
                            x[4]=aux[2]
                            x[6]=''
                            x[7]=''
                            aparte.append(x)
                    else:
                        x[0]=aux[0]
                        x[4]=aux[2]
                        x[6]=''
                        x[7]=''
                        aparte.append(x)
        if len(aparte)!=0: datos=datos+aparte

        return datos

    def adicionar_ConceptoJerarquiaDev(self,vtasf)->list:
        datos=[]
        aparte=[]
        for x in vtasf:
            if int(x[8])<0 or int(x[9])<0:
                aux=self.buscar_ConceptoJerquiaDev(x[4])
                if len(aux)!=0:
                    if aux[5]=='n':             
                        x[0]=aux[0]
                        x[4]=aux[2]
                        x[8]=abs(x[8])
                        x[9]=abs(x[9])
                        datos.append(x)
                    elif aux[5]=='s':
                        if len(aparte)!=0:
                            bandera=True
                            for y in aparte:
                                if y[0]==aux[0] and y[4]==aux[2]:
                                    y[8]+=x[8]
                                    y[9]+=x[9]
                                    bandera=False
                                    break
                            if bandera:
                                x[0]=aux[0]
                                x[4]=aux[2]
                                x[6]=''
                                x[7]=''
                                x[8]=abs(x[8])
                                x[9]=abs(x[9])
                                aparte.append(x)
                        else:
                            x[0]=aux[0]
                            x[4]=aux[2]
                            x[6]=''
                            x[7]=''
                            x[8]=abs(x[8])
                            x[9]=abs(x[9])
                            aparte.append(x) 
            else:
                datos.append(x)
        if len(aparte)!=0: datos=datos+aparte
        return datos

    def calcular_Quitar_Ico(self,vtas):
        datos=[]
        for x in vtas:
            valConcepto=self.buscar_ValConcepto(x[0])
            if valConcepto==self.__valIpoC:
                x[9]=round(x[9]/(1+self.__valIpoC))
                self.__icoTotal+=x[9]*self.__valIpoC
                datos.append(x)
            elif valConcepto==1:
                x[9]=round(x[9])
                datos.append(x)
            else:
                x[9]=round(x[9]/(1+valConcepto))
                datos.append(x)
        return datos

    def eliminar_Ceros(self,vtas)->list:
        datos=[]
        for x in vtas:
            if x[8]!=0:
                datos.append(x)
        return datos

    def adicionar_Definiciones(self,vtasf)->list:
        for x in vtasf:
            aux=self.buscar_Definiciones(x[5],x[6])
            x[3]=aux[0]
            x[6]=aux[1]
        return vtasf

    def adicionar_IpoConsumo(self,ofi)->list:
        aux=self.buscar_ConceptoJerarquia('ico')
        if len(aux)!=0: return [aux[0],'10','00','',aux[2],ofi,'','','',round(self.__icoTotal-self.__ipoDescuento)]
        return []

    def arreglar_Domicilios(self,vtasf)->list:
        for x in vtasf:
            if x[0]=='0010':
                x[3]=''
                x[4]=''
                x[8]=''
        return vtasf

    def rutina(self)->str:
        self.__conf=file().configuraciones()
        self.cargarConfig()
        puntos=ctcon().getConexiones()
        for i in puntos:
            if self.comprobar_Reportes(i[1],i[2]):
                print(f'Creando->{i[1]}:')
                if self.__hoy.day<11: self.analizarDb(i[0],i[1],i[2],False,False)
                elif self.__hoy.day==11: self.analizarDb(i[0],i[1],i[2],False,True)
                elif self.__hoy.day>11: self.analizarDb(i[0],i[1],i[2],True,False)
                else: print('Error inesperado')
            else: print(f'{i[1]}->Reporte existente')
        return f'Rutina Terminada {self.__hoy}'

if __name__=='__main__':
    prueba=CtrlReportes()