from tkinter.font import BOLD
from CtrlControl import *
import tkinter as tk
import pandas as pd
class Ventana():
    __conect=CtrlConexion()

    def __init__(self) -> None:
        #Ventana Raiz      
        self.__raiz=tk.Tk()
        self.__raiz.title('Interfaz')
        self.__raiz.iconbitmap('Iconos/lista.ico')
        self.__raiz.resizable(False,False)
        self.__wventana=int(round(self.__raiz.winfo_screenwidth()*0.7,0))
        self.__hventana=int(round(self.__raiz.winfo_screenheight()*0.6,0))
        self.__wtotal = self.__raiz.winfo_screenwidth()
        self.__htotal = self.__raiz.winfo_screenheight()
        self.__pwidth = round(self.__wtotal/2-self.__wventana/2)
        self.__pheight = round(self.__htotal/2-self.__hventana/2)
        self.__raiz.geometry(str(self.__wventana)+"x"+str(self.__hventana)+"+"+str(self.__pwidth)+"+"+str(self.__pheight))

        #Menu
        self.__menuBar=tk.Menu(self.__raiz)
        self.__raiz.config(menu=self.__menuBar)
        self.__mInicio=tk.Menu(self.__menuBar,tearoff=0)
        self.__mInicio.add_command(label='<--',command=lambda:[self.cambiar_Frames(1)])
        self.__mInicio.add_separator()
        self.__mInicio.add_command(label='Salir')
        self.__mConexiones=tk.Menu(self.__menuBar,tearoff=0)
        self.__mConexiones.add_command(label='Lista',command=lambda:[self.cambiar_Frames(2)])
        self.__mConsultas=tk.Menu(self.__menuBar,tearoff=0)
        self.__mConsultas.add_command(label='Archivo')
        self.__menuBar.add_cascade(label='Inicio',menu=self.__mInicio)
        self.__menuBar.add_cascade(label='Conexiones',menu=self.__mConexiones)
        self.__menuBar.add_cascade(label='Consultas',menu=self.__mConsultas)
        self.ventana_Inicio()
        self.ventana_Conexiones()
        self.cambiar_Frames(1)
        self.__raiz.mainloop()

    def cambiar_Frames(self,x):
        #self.__conFrame.pack_forget()
        #self.__iniFrame.pack_forget()
        self.__conFrame.destroy()        
        self.__iniFrame.destroy()
        if x==1:
            self.ventana_Inicio()
            self.__iniFrame.pack(fill=tk.BOTH,expand=True)
        elif x==2:
            self.ventana_Conexiones()
            self.__conFrame.pack(fill=tk.BOTH,expand=True)
            #Campos de texto y botones
        
    def ventana_Inicio(self):
        self.__iniFrame=tk.Frame(bg='#4170CF',width=self.__wventana,height=self.__hventana)

    def ventana_Conexiones(self):
        #Frame que se 'empaquetara en la ventana'
        self.__conFrame=tk.Frame(bg='#32BB6A',width=self.__wventana,height=self.__hventana)
        #self.__conFrame.columnconfigure(0,weight=1)
        self.__conFrame.columnconfigure(2,weight=1)
        self.__conFrame.rowconfigure(index=0,weight=1)
        self.__conFrame.rowconfigure(index=1,weight=1)
        self.__conFrame.rowconfigure(index=2,weight=1)
        self.__conFrame.rowconfigure(index=3,weight=1)
        self.__conFrame.rowconfigure(index=4,weight=1)
        self.__conFrame.rowconfigure(index=5,weight=1)
        self.__conFrame.rowconfigure(index=6,weight=1)
        self.__conFrame.rowconfigure(index=7,weight=1)
        self.__conFrame.rowconfigure(index=8,weight=1)
        self.__conFrame.rowconfigure(index=9,weight=1)
        self.__conFrame.rowconfigure(index=10,weight=1)
        self.__conFrame.rowconfigure(index=11,weight=1)


        #Variables asociadas a los componentes de la ventana
        self.__bsName=tk.StringVar()
        self.__bsPropiedad=tk.StringVar()
        self.__bsOfiVentas=tk.StringVar()

        #Componentes de las ventanas
        tk.Label(self.__conFrame,text='Sistemas Zona K',bg='#32BB6A',font=('Cambria',15,BOLD)).grid(row=0,column=0,columnspan=3,sticky=tk.EW)
        tk.Label(self.__conFrame,text='_Nombre Server_',bg='#32BB6A',font=('Cambria',15,BOLD)).grid(row=1,column=0,columnspan=2)
        tk.Entry(self.__conFrame,textvariable=self.__bsName,font=('Cambria',12,BOLD)).grid(row=2,column=0,columnspan=2)
        tk.Label(self.__conFrame,text='_Propiedad_',bg='#32BB6A',font=('Cambria',15,BOLD)).grid(row=3,column=0,columnspan=2,sticky=tk.EW)
        tk.Entry(self.__conFrame,textvariable=self.__bsPropiedad,font=('Cambria',12,BOLD)).grid(row=4,column=0,columnspan=2)
        tk.Label(self.__conFrame,text='_Ofi. Ventas_',bg='#32BB6A',font=('Cambria',15,BOLD)).grid(row=5,column=0,columnspan=2,sticky=tk.EW)
        tk.Entry(self.__conFrame,textvariable=self.__bsOfiVentas,font=('Cambria',12,BOLD)).grid(row=6,column=0,columnspan=2)
        tk.Button(self.__conFrame,text='Nueva').grid(row=7,column=0,columnspan=2,padx=2)
        tk.Button(self.__conFrame,text='Agregar').grid(row=8,column=0,columnspan=2,padx=2)        
        tk.Button(self.__conFrame,text='Editar').grid(row=9,column=0,columnspan=2,padx=2)
        tk.Button(self.__conFrame,text='Eliminar').grid(row=10,column=0,columnspan=2,padx=2)
        tk.Button(self.__conFrame,text='Probar').grid(row=11,column=0,columnspan=2,padx=2)
        tk.Frame(self.__conFrame,bg='white',relief='groove',bd=3).grid(row=1,column=2,rowspan=11,padx=3,pady=3,sticky=tk.N+tk.S+tk.E+tk.W)

if __name__=='__main__':
    Ventana()