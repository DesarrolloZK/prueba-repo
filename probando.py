test=[['a','b',1], # <-[a,b,11]
      ['a','b',6],  #---
      ['a','b',4],  #---
      ['a','c',6],  #[]
      ['a','c',8],  #---
      ['a','c',9],  #---
      ['a','n',3],  #[]
      ['a','n',4],  #---
      ['a','m',5],  #[]
      ['a','m',5],
      ['a','m',5]]  #---

def prueba(datos,totales)->list:
    try:
        if datos[0][0]==datos[1][0] and datos[0][1]==datos[1][1]:
            datos[0][2]=datos[0][2]+datos[1][2]
            datos.pop(1)
        else:
            totales.append(datos[0])
            datos.pop(0)
    except IndexError:
        totales.append(datos[0])
        return totales
    return prueba(datos,totales)

def prueba2(datos)->list:
    i=0
    while i<len(datos):
        if datos[i][1]=='c':
            datos.pop(i)
            i-=1
        i+=1
    return datos

aja=prueba2(test)

for i in aja:
    print(i)


'''
x=0
nueva=list()
try:    
    while len(test) > 0:        
        if test[x][0]==test[x+1][0] and test[x][1]==test[x+1][1]:
            test[0]=[test[x][0],test[x][1],test[x][2]+test[x+1][2]]
            test.pop(1)
        else:
            nueva.append([test[x][0],test[x][1],test[x][2]])
            test.pop(0)
        if len(test)==1:
                nueva.append([test[x][0],test[x][1],test[x][2]])
except Exception as e:
    pass
print(nueva)
'''

        






    
