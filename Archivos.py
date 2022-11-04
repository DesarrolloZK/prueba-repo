import pickle

class Archivos():   
        
    
    def guardarArchivo(prueba):
        with open("Conexiones.pickle","wb") as f:            
            pickle.dump(prueba,f)
            print("Archivo guardado")

