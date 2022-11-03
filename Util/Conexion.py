import pyodbc


if __name__=='__main__':
    
    try:
        server="172.19.101.139\sqlexpress"
        bd="DataStore"
        username="ivkdb"
        password="Grup0IVK1*"
        conexion=pyodbc.connect('DRIVER={ODBC Driver 18 for SQL server};'+
        'SERVER='+server+';DATABASE='+bd+';UID='+username+';PWD='+password+
        ';ENCRYPT=No;')
        print(f"Conexion a {server} exitosa\n")
        

    except Exception as e:
        print(f"Error de conexion:\n {e}")

    
    try:
        with conexion.cursor() as cursor:
            prueba=cursor.execute("select * from dbo.HFI_PAYLOAD;").fetchall()

            for dat in prueba:
                print(dat)
        

        

    except Exception as e:
        print(f"Error al consultar: {e}")