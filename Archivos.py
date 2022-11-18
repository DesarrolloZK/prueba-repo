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

    def leerArchivo()->list:
        lista=list()
        try:
            with open("Conexiones/Conexiones.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(','))
                r.close()
            return lista
            
        except Exception as e:            
            return[]
    
    def finalFile(datos)->str:
        #print(f'{datos}\n---------------\n')
        try:
            with open('Reportes/Dapo82/VTAS'+datos[0][1].strftime('%d%m%Y')+'.txt','w') as wm:
                for i in datos:
                    if i[1] != None:
                        wm.write(f'{i[0]};{i[1].strftime("%d/%m/%y")};{i[2]};{i[3]};{i[4]};{i[5]};{i[6]}\n')
                wm.close()
                return 'Creado exitosamente'
        except Exception as e:
            return f'Error al escribir archivo vtas\n Error: {e}'     

