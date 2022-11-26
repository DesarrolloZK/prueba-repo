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

    def escArchDia(datos,propiedad,ofi,my)->str:
        def diario():
            with open(f'Consultas/{propiedad}-{ofi}/1a10-{my}.txt','a+') as wm:
                    for i in datos:                                               
                        wm.write(f'{i[0]};{i[1]};{i[2]};{i[3]};{i[4]};{i[5]};{i[6]};{i[7]};{i[8]};{i[9]}\n')
                    wm.close()
            return 'Creado exitosamente'
        try:
            os.mkdir(f'Consultas/{propiedad}-{ofi}')
            return diario()
        except FileExistsError as fee:
            try:
                return diario()
            except Exception as e:
                return f'Error al escribir archivo: {str(e)}'
        except FileNotFoundError as fne:
            return f'Error: {fne}'

    def reportes(datos,propiedad,ofiVent,fecha)->str:
        def crear():
            with open(f'Reportes/{propiedad}/{ofiVent}VTAS{fecha}.txt','w') as wm:
                for i in datos:
                    wm.write(f'{i[1]}\n')
                wm.close()
        try:
            os.mkdir(f'Reportes/{propiedad}')
            return crear()
        except FileExistsError as fee:
            try:
                return crear()
            except Exception as e:
                return f'Error al escribir archivo reporte {str(e)}'
        except FileNotFoundError as fne:
            return f'Error: {fne}'

        

            

