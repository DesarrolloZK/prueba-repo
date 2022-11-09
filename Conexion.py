from asyncio.windows_events import NULL
import pyodbc
#Clase para controlar la conexion con la base de datos
class Conexion():
    #Metodo constructor para asignar los datos necesarios para la conexion
    def __init__(self) -> None:
        self.__serverName=None
        self.__propiedad=None
        self.__ofiVentas=None
        self.__conect=None
        
        
    #Funcion en cargada de realizar la conexion y retornar true si se establece la conexion
    #y retornar flase si no se establece dicha conexion
    def conectar(self,sName,prop,ofVen)->bool:
        self.__serverName=sName
        self.__propiedad=prop
        self.__ofiVentas=ofVen
        try:            
            self.__conect=pyodbc.connect('DRIVER={ODBC Driver 18 for SQL server};'+
            'SERVER='+self.__serverName+
            ';DATABASE=CheckPostingDB;UID=ivkdb;PWD=Grup0IVK1*;ENCRYPT=No')            
            return True
        except:
            return False

    #Funcion para realizar consultas en la base de datos
    #Esta funcion  es de prueba.
    def consulta(self,sentencia)->list:
        try:
            with self.__conect.cursor() as cursor:               
                return cursor.execute(sentencia+';').fetchall()
        except Exception as e:
            print(f"Error al consultar: {e}")
    
    def cerrarConexion(self):
        self.__conect.close()
    
    def getServerName(self)->str:
        return self.__serverName
    
    def getPropiedad(self)->str:
        return self.__propiedad
    
    def getOfiVentas(self)->str:
        return self.__ofiVentas
'''
p=Conexion()
print(p.conectar('172.19.101.139\sqlexpress','test','1305'))
print(p.consulta('select * from dbo.SAP_int'))'''