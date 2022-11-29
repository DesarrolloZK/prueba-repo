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
        






    
