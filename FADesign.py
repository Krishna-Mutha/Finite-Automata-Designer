from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mg
from tkinter.ttk import *
from PIL import ImageTk,Image
import pygraphviz as pgv
r=Tk()
statenumber=1
def reset():
    global display,statenumber
    statenumber=1
    graph.clear()
    graph.add_node("Start")
    graph.layout()
    graph.draw("graph.png")
    img=ImageTk.PhotoImage(Image.open("graph.png"))
    display.config(image=img)
    display.image=img
def addState():
    global statenumber,display
    graph.add_node("q"+str(statenumber))
    graph.layout()
    graph.draw("graph.png")
    img=ImageTk.PhotoImage(Image.open("graph.png"))
    display.config(image=img)
    display.image=img
    statenumber+=1
graph=pgv.AGraph(directed=True)
graph.add_node("Start")
graph.layout()
graph.draw("graph.png")
img=Image.open("graph.png")
img=ImageTk.PhotoImage(img)
resetbtn=Button(r,text="Reset",command=reset)
addbtn=Button(r,text="Add New State",command=addState)
title=Label(r,text="Finite Automata Designer",font=("Arial",20))
display=Label(r,image=img)
display.place(relx=0.5,rely=0.7,anchor="center")
resetbtn.place(relx=0.3,rely=0.09)
addbtn.place(relx=0.4,rely=0.09)
title.pack()
r.title("Finite Automata Designer")
r.geometry("800x600")
r.mainloop()