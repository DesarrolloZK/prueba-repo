import tkinter as tk

class Ventana():

    def __init__(self) -> None:

        self.__raiz=tk.Tk()
        self.__raiz.title('Interfaz')
        self.__raiz.iconbitmap('Iconos/lista.ico')
        self.__raiz.resizable(False,False)
        self.__wventana=700
        self.__hventana=800
        self.__wtotal = self.__raiz.winfo_screenwidth()
        self.__htotal = self.__raiz.winfo_screenheight()
        self.__pwidth = round(self.__wtotal/2-self.__wventana/2)
        self.__pheight = round(self.__htotal/2-self.__hventana/2)
        self.__raiz.geometry(str(self.__wventana)+"x"+str(self.__hventana)+"+"+str(self.__pwidth)+"+"+str(self.__pheight))
        self.__miFrame=tk.Frame(bg='gray',width=self.__wventana,height=self.__hventana)
        self.__miFrame.pack(expand=True)
        self.__raiz.mainloop()

if __name__=='__main__':
    Ventana()