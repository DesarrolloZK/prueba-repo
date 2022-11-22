import os
class Archivos():   
        
    
    def guardarArchivo(con):        
        try:
            with open("Conexiones/Conexiones.txt","w") as wm:                
                for i in con:
                    wm.write(f'{i[0]},{i[1]},{i[2]}{os.linesep}')                                 
                wm.close()
            return True
        except Exception as e:
            print(f"Error de escritura:\n{e}")
            return False

    def traerConexiones()->list:
        lista=list()
        try:
            with open("Conexiones/Conexiones.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(','))
                r.close()
            return lista
            
        except FileNotFoundError as fnf:
            print(fnf)     
            return []
    
    def traerTransacciones():
        lista=list()
        try:
            with open("Tablas/Type.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(':'))
            return lista
        except FileNotFoundError as fnf:
            print(fnf)
            return []

    def finalFile(datos,propiedad,ofiVent,fecha)->str:
        def reporte():
            with open(f'Reportes/{propiedad}/{ofiVent}VTAS{fecha}.txt','w') as wm:
                    for i in datos:
                        if i[6]!=None:                                                
                            wm.write(i)
                    wm.close()
            return 'Creado exitosamente'

        try:
            os.mkdir(f'Reportes/{propiedad}')
            return reporte()
        except FileExistsError as fee:
            try:
                return reporte()
            except Exception as e:
                return 'Error al escribir archivo '+str(e)
        except IOError as ioe:
            return f'Error: {ioe}'

        

            

