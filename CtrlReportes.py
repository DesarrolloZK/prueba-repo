from CtrlConexion import CtrlConexion as ctcon
from Archivos import Archivos as file
from Archivos import Archivos as arc
from calendar import monthrange as mr
from tkinter import messagebox
from datetime import datetime
from datetime import timedelta
import decimal

class CtrlReportes():
    #Metodo constructor
    #Aqui traemos la informacion del archivo de configuracion
    def __init__(self)->None:
        self.__conf=file().configuraciones()
        self.cargarConfig()
        

    def cargarConfig(self)->None:
        if len(self.__conf)!=0:
            self.__consulta=None
            self.__valIpoC=None
            self.__valConJer=[]
            self.__valConJerDev=[]
            self.__consulta=None
            self.__ctcon=ctcon()
            self.__hoy=datetime.now()
            self.cargar_ConceptoJerarquia()
            self.cargar_ConceptoJerarquiaDev()
            self.cargar_Definiciones()
            for x in self.__conf:
                if x[0].upper()=='QUERY':self.__consulta=x[1]
                elif x[0].upper()=='IPOCONSUMO':self.__valIpoC=decimal.Decimal(x[1])/100
            if (self.__consulta or self.__valIpoC)==None: print('No hay query disponible o no se ha establecido un valor de impuesto al consumo')
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
                return [i[0],i[2],i[5]]
            if str(jer)=='None':
                return self.buscar_ConceptoJerarquia(1)
        return []
    
    def buscar_ConceptoJerquiaDev(self,jer)->list:
        self.cargar_ConceptoJerarquiaDev()      
        for i in self.__conJerDev:
            if str(jer)==i[1]:
                return [i[0],i[2],i[5]]
        return []

    def buscar_ValConcepto(self,conc)->decimal.Decimal:
        conceptos=self.__valConJer+self.__valConJerDev
        for x in conceptos:
            if x[0]==conc:
                if x[0]=='-1': return decimal.Decimal(x[1].replace('-',''))
                elif x[0]!='0': return decimal.Decimal(x[1])/decimal.Decimal('100')
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
        #try:
            vtas=[]
            descuentos=[]
            consultaDia=[]
            datos=self.__ctcon.consultar(sName,self.__consulta)
            print(arc.escribirConsulta(datos,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d-%m-%Y'),'Bruta'))
            #for f in datos:
                #print(type(f[0]),type(f[1]),type(f[2]),type(f[3]),type(f[4]),type(f[5]),type(f[6]),type(f[7]),type(f[8]),type(f[9]),type(f[10]))
            print(f'----------------------{prop}----------------------------')
            for i in datos:
                if i[10]!=None:
                    bandera=self.verificar_DiaAnterior(i[1]) or self.verificar_MesAnterior(i[1]) or self.verificar_AnioAnterior(i[1])
                    if i[7]==1 and bandera:
                        consultaDia.append(i)
                        vtas.append([i[0],i[1].strftime('%d%m%Y %H:%M'),i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
                    if i[7]==2 and bandera:
                        consultaDia.append(i)
                        descuentos.append([i[5],i[6]])
            print(arc.escribirConsulta(consultaDia,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d-%m-%Y'),'Diaria'))
            suma=0
            if len(vtas)!=0:
                if reporte:
                    vtas=self.ordenar_Infomacion(vtas,descuentos,ofi)
                    for z in vtas:
                        suma+=z[9]
                    print(f'Final: {suma}')
                    print(arc.reportes(vtas,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d%m%Y')))
                if reportes:
                    del vtas
                    vtas=arc.traerConsultaDiaria(prop,ofi)
                    print(arc.reportes(vtas,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d%m%Y')))
            else: print('No datos')
        #except Exception as e:
            #print(f'Error en el analisis de la Db\nError: {e}')

    def convertir_Datos(self,vtas)->list:
        datos=[]
        for x in vtas:
            x[0]=int(x[0])
            x[1]=datetime.strptime(x[1],)
        return datos

    def ordenar_Infomacion(self,vtas,descuentos,ofi)->list:
        vtasf=[]
        self.__icoTotal=0
        vtas=self.filtrar_Ppds(vtas)
        propinas=self.suma_Propinas(vtas,ofi)
        descuentos=self.calcular_Descuentos(descuentos,ofi)
        vtas=self.sumar_Productos(vtas)
        vtasf=self.orden_Final(vtas,ofi)
        vtasf=self.adicionar_ConceptoJerarquia(vtasf)
        vtasf=self.adicionar_ConceptoJerarquiaDev(vtasf)
        vtasf=self.calcular_Quitar_Ico(vtasf)
        vtasf=self.eliminar_Ceros(vtasf)
        vtasf=self.adicionar_Definiciones(vtasf)
        if len(propinas)>0:vtasf.append(propinas)
        if len(descuentos)>0:vtasf.append(descuentos)
        vtasf.append(self.adicionar_IpoConsumo(ofi))
        return vtasf

    def filtrar_Ppds(self,vtas)->list:
        datos=[]
        for x in vtas:
            if x[3]>99999:
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
        return [aux[0],'10','00','',aux[1],ofi,'','','',round(sum)]

    def calcular_Descuentos(self,descuentos,ofi)->list:
        self.__ipoDescuento=0
        aux=[0,0]
        for x in descuentos:
            if x[0]!=None:aux[0]+=abs(x[0])
            if x[1]!=None:aux[1]+=abs(x[1])
        if (aux[0] and aux[1])!=0:
            aux[1]=round(aux[1]/(1+self.__valIpoC))
            self.__ipoDescuento=aux[1]*self.__valIpoC
            aux1=self.buscar_ConceptoJerarquia('disc')
            return [aux1[0],10,'00','',aux1[1],ofi,'',3,aux[0],aux[1]]
        return []

    def sumar_Productos(self,vtas)->list:
        datos=[]
        suma=0
        for x in vtas:
            if len(datos)==0:
                if (x[5] and x[6])!=None:datos.append(x)                    
            else:
                b=True
                for y in datos:
                    if (x[5] and x[6])!=None:
                        if y[2]==x[2] and y[3]==x[3] and y[4]==x[4]:
                            y[5]+=x[5]
                            y[6]+=x[6]
                            b=False
                            break
                    else:b=False
                if b:datos.append(x)
        for z in datos:
            suma+=z[6]
        print(f'Funcion suma: {round(suma/decimal.Decimal(1.08))}')
        return datos

    def orden_Final(self,vtas,ofi)->list:
        datos=[]
        for x in vtas:
            datos.append(['Concepto','10','00','MST',x[2],ofi,str(x[4]),x[3],x[5],x[6]])
        return datos

    def adicionar_ConceptoJerarquia(self,vtasf)->list:
        datos=[]
        aparte=[]
        suma=0
        for x in vtasf:
            if x[8]<0 or x[9]<0:
                datos.append(x)
                continue
            aux=self.buscar_ConceptoJerarquia(x[4])
            if len(aux)!=0:
                if aux[2]=='n':
                    x[0]=aux[0]
                    x[4]=aux[1]
                    datos.append(x)
                elif aux[2]=='s':
                    if len(aparte)!=0:
                        bandera=True
                        for y in aparte:
                            if y[0]==aux[0] and y[4]==aux[1]:
                                y[8]+=x[8]
                                y[9]+=x[9]
                                bandera=False
                                break
                        if bandera:
                            x[0]=aux[0]
                            x[4]=aux[1]
                            x[6]=''
                            x[7]=''
                            aparte.append(x)
                    else:
                        x[0]=aux[0]
                        x[4]=aux[1]
                        x[6]=''
                        x[7]=''
                        aparte.append(x)
        for z in datos+aparte:
            suma+=z[9]
        print(f'Funcon Concepto: {round(suma/decimal.Decimal(1.08))}')
        if len(aparte)!=0: datos=datos+aparte
        return datos

    def adicionar_ConceptoJerarquiaDev(self,vtasf)->list:
        datos=[]
        aparte=[]
        suma=0
        for x in vtasf:
            if int(x[8])<0 and int(x[9])<0:
                aux=self.buscar_ConceptoJerquiaDev(x[4])
                if len(aux)!=0:
                    if aux[2]=='n':             
                        x[0]=aux[0]
                        x[4]=aux[1]
                        x[8]=x[8]*-1
                        x[9]=x[9]*-1
                        datos.append(x)
                    elif aux[2]=='s':
                        if len(aparte)!=0:
                            bandera=True
                            for y in aparte:
                                if y[0]==aux[0] and y[4]==aux[1]:
                                    y[8]+=x[8]
                                    y[9]+=x[9]
                                    bandera=False
                                    break
                            if bandera:
                                x[0]=aux[0]
                                x[4]=aux[1]
                                x[6]=''
                                x[7]=''
                                x[8]=x[8]*-1
                                x[9]=x[9]*-1
                                aparte.append(x)
                        else:
                            x[0]=aux[0]
                            x[4]=aux[1]
                            x[6]=''
                            x[7]=''
                            x[8]=x[8]*-1
                            x[9]=x[9]*-1
                            aparte.append(x) 
            else:
                datos.append(x)
        for z in datos+aparte:
            suma+=z[9]
        print(f'Funcon ConceptoDev: {round(suma/decimal.Decimal(1.08))}')
        if len(aparte)!=0: datos=datos+aparte
        return datos

    def calcular_Quitar_Ico(self,vtas):
        datos=[]
        suma=0
        for x in vtas:
            valConcepto=self.buscar_ValConcepto(x[0])
            if valConcepto==self.__valIpoC:
                x[9]=round(x[9]/(1+self.__valIpoC))
                self.__icoTotal+=x[9]*self.__valIpoC
                datos.append(x)
            elif valConcepto==1.0:
                x[9]=round(x[9])
                datos.append(x)
            else:
                if x[7]==201581:
                    print(x)
                x[9]=round(x[9]/(1+valConcepto))
                datos.append(x)
        for z in datos:
            suma+=z[9]
        print(f'Funcon Calcular_Quitar_Ico: {round(suma)}')
        return datos

    def eliminar_Ceros(self,vtas)->list:
        datos=[]
        suma=0
        for x in vtas:
            if x[8]!=0:
                datos.append(x)
        for z in datos:
            suma+=z[9]
        print(f'Funcon Eliminar ceros: {round(suma)}')
        return datos

    def adicionar_Definiciones(self,vtasf)->list:
        suma=0
        for x in vtasf:
            aux=self.buscar_Definiciones(x[5],x[6])
            x[3]=aux[0]
            x[6]=aux[1]
        for z in vtasf:
            suma+=z[9]
        print(f'Funcon ad Def: {round(suma)}')
        return vtasf

    def adicionar_IpoConsumo(self,ofi)->list:
        aux=self.buscar_ConceptoJerarquia('ico')
        if len(aux)!=0: return [aux[0],'10','00','',aux[1],ofi,'','','',round(self.__icoTotal-self.__ipoDescuento)]
        return []

    def rutina(self):
        puntos=ctcon().getConexiones()
        for i in puntos: self.analizarDb(i[0],i[1],i[2],True,False)
        '''
        if self.__hoy.day==1: 
            self.del_Reportes()
        if self.__hoy.day<11:
            for i in puntos: self.analizarDb(i[0],i[1],i[2],False,False)
        elif self.__hoy==11:
            for i in puntos: self.analizarDb(i[0],i[1],i[2],False,True)
        elif self.__hoy.day>11:
            for i in puntos: self.analizarDb(i[0],i[1],i[2],True,False)
        else:
            print('Error inesperado')
        '''
        
if __name__=='__main__':
    prueba=CtrlReportes()
    prueba.rutina() 
    #prueba.analizarDb('172.19.25.73\sqlexpress','716','1820',True,False)