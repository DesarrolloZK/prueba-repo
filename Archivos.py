import pickle

class Archivos():   
        
    
    def guardarArchivo(con):        
        try:
            with open("Conexiones/Prueba.txt","w") as wm:
                
                for i in con:
                    wm.writelines(f"{i[0]},{i[1]},{i[2]}\n")
                wm.close()
            return True
        except Exception as e:
            print(f"Error de escritura:\n{e}")
            return False

    def leerArchivo()->list:
        lista=list()
        try:
            with open("Conexiones/Prueba.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(','))
            return lista
            
        except Exception as e:
            print(f"Error de lectura:\n{e}")
            pass

    def testArchivo(con):        
        try:
            with open("Conexiones/Prueba.pickle","w") as wm:                
                for i in con:
                    pickle.dump(i,wm)
                wm.close()
            return True
        except Exception as e:
            print(f"Error de escritura:\n{e}")
            return False

'''
Archivos.guardarArchivo(["1891","luna","1134"])
Archivos.guardarArchivo(["luna1","wata1","dapo1","barra1"])
Archivos.guardarArchivo(["luna2","wata2","dapo2","barra2"])
'''
if __name__=="__main__":
    print(Archivos.leerArchivo())    