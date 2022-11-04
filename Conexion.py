from asyncio.windows_events import NULL
import pyodbc
#Clase para controlar la conexion con la base de datos
class ControlConexion():
    #Metodo constructor para asignar los datos necesarios para la conexion
    def __init__(self,sName,propiedad,ofiVentas) -> None:
        self.__serverName=sName
        self.__propiedad=propiedad
        self.__ofiVentas=ofiVentas
        self.__DATABASE="CheckPostingDB"
        self.__USER="ivkdb"
        self.__PASSWORD="Grup0IVK1*"
        self.__conexion=NULL
        
    #Funcion en cargada de realizar la conexion y retornar true si se establece la conexion
    #y retornar flase si no se establece dicha conexion
    def conectar(self)->bool:
        try:            
            self.__conexion=pyodbc.connect('DRIVER={ODBC Driver 18 for SQL server};'+
            'SERVER='+self.__serverName+';DATABASE='+self.__DATABASE+';UID='+self.__USER+';PWD='+self.__PASSWORD+
            ';ENCRYPT=No')
            return True
        except:
            return False

    #Funcion para realizar consultas en la base de datos
    #Esta funcion  es solo de prueba.
    def consulta(self,sentencia)->list:
        try:
            with self.__conexion.cursor() as cursor:
                con=cursor.execute(sentencia+';').fetchall()
                return con
        except Exception as e:
            print(f"Error al consultar: {e}")
    
    def getServerName(self)->str:
        return self.__serverName

    def getSUser(self)->str:
        return self.__USER
    
    def getDataBase(self)->str:
        return self.__DATABASE

    def getPropiedad(self)->str:
        return self.__propiedad


   

if __name__=="__main__":

    listaConexiones=list()
    
    test=ControlConexion("172.19.101.139\sqlexpress","Dapo82")    
    if test.conectar():
        print(f"Conexion establecida con {test.getServerName()}")
        listaConexiones.append(test)
    else:
        print(f"Error al conectar con {test.getServerName()}")
    
    test=ControlConexion("172.19.101.121\sqlexpress","Luna")

    if test.conectar():
        print(f"Conexion establecida con {test.getServerName()}")
        listaConexiones.append(test)
    else:
        print(f"Error al conectar con {test.getServerName()}")
    
    print(int(listaConexiones[0].consulta("select * from dbo.SAP_int")[0][7]))
    print("---------------separardor----------------\n")
    print(listaConexiones[1].consulta("select * from dbo.MENU_ITEM_CLASS"))
    