class Archivos():   
        
    
    def guardarArchivo(con):        
        try:
            with open("Conexiones/Conexiones.txt","w") as wm:                
                for i in con:
                    wm.write(f'{i[0]},{i[1]},{i[2]}\n')                                 
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

if __name__=="__main__":
    for i in Archivos.leerArchivo():
        print(i)  
