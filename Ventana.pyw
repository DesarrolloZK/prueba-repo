import tkinter as tk
from tkinter.font import BOLD
from CtrlControl import *
class Ventana():
    __conect=CtrlConexion()
    def __init__(self) -> None:
        #Ventana Raiz      
        self.__raiz=tk.Tk()
        self.__raiz.title('Interfaz')
        self.__raiz.iconbitmap('Iconos/lista.ico')
        self.__raiz.resizable(False,False)
        self.__wventana=900
        self.__hventana=800
        self.__wtotal = self.__raiz.winfo_screenwidth()
        self.__htotal = self.__raiz.winfo_screenheight()
        self.__pwidth = round(self.__wtotal/2-self.__wventana/2)
        self.__pheight = round(self.__htotal/2-self.__hventana/2)
        self.__raiz.geometry(str(self.__wventana)+"x"+str(self.__hventana)+"+"+str(self.__pwidth)+"+"+str(self.__pheight))
        #Frame que se 'empaquetara en la ventana'
        self.__miFrame=tk.Frame(bg='#4170CF',width=self.__wventana,height=self.__hventana)
        self.__miFrame.columnconfigure(0,weight=1)

        #Menu
        self.__menuBar=tk.Menu(self.__miFrame)
        self.__raiz.config(menu=self.__menuBar)
        self.__mInicio=tk.Menu(self.__menuBar,tearoff=0)
        self.__mInicio.add_command(label='Salir')
        self.__mConexiones=tk.Menu(self.__menuBar,tearoff=0)
        self.__mConexiones.add_command(label='Lista')
        self.__mConsultas=tk.Menu(self.__menuBar,tearoff=0)
        self.__mConsultas.add_command(label='Archivo')
        self.__menuBar.add_cascade(label='Inicio',menu=self.__mInicio)
        self.__menuBar.add_cascade(label='Conexiones',menu=self.__mConexiones)
        self.__menuBar.add_cascade(label='Consultas',menu=self.__mConsultas)

        #Variables asociadas a los componentes de la ventana
        self.__bsName=tk.StringVar()
        self.__bsPropiedad=tk.StringVar()

        #Campos de texto y botones
        tk.Label(self.__miFrame,text='_Sistemas Zona K_',bg='#4170CF',font=('Cambria',15,BOLD)).grid(row=0,column=0,sticky=tk.EW)
        tk.Label(self.__miFrame,text='_Nombre Server_',font=('Cambria',15,BOLD)).grid(row=1,column=0)
        tk.Entry(self.__miFrame,textvariable=self.__bsName,font=('Cambria',15,BOLD)).grid(row=2,column=0)
        tk.Label(self.__miFrame,text='_Propiedad_',bg='#4170CF',font=('Cambria',15,BOLD)).grid(row=3,column=0,sticky=tk.EW)
        tk.Entry(self.__miFrame,textvariable=self.__bsPropiedad,font=('Cambria',15,BOLD)).grid(row=4,column=0)
        self.__miFrame.pack(fill=tk.BOTH,expand=True)

        self.__raiz.mainloop()

if __name__=='__main__':
    Ventana()