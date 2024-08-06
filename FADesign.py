from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mg
from tkinter.ttk import *
from PIL import ImageTk,Image
import pygraphviz as pgv
import time
r=Tk()
statenumber=1
def updateList():
    global opts,state1,state2
    opts.config(values=graph.nodes()[1::])
    state1.config(values=graph.nodes())
    state2.config(values=graph.nodes())
def refreshImage():
    global img,display
    img=ImageTk.PhotoImage(Image.open("graph.png"))
    display.config(image=img)
    display.image=img
def forget():
    global opts,confirmdelbtn
    opts.place_forget()
    confirmdelbtn.place_forget()
def confirmdel():
    global opts
    temp_del=opts.get()
    if(temp_del!=" " and temp_del!="Deleted Successfully"):
        try:
            graph.remove_edge(temp_del)
        except:
            pass
        graph.remove_node(temp_del)
        graph.draw("graph.png")
        opts.set("Deleted Successfully")
        r.after(3000,lambda:opts.set(""))
        refreshImage()
        updateList()
def delete():
    global opts,confirmdelbtn
    opts.place(relx=0.65,rely=0.09,anchor="w")
    confirmdelbtn.place(relx=0.83,rely=0.09,anchor="w")
def reset():
    global display,statenumber
    forget()
    statenumber=1
    graph.clear()
    graph.add_node("Start")
    graph.layout(prog='sfdp', args='-Goverlap=scale')
    graph.draw("graph.png")
    refreshImage()
    updateList()
def addState():
    global statenumber,display
    forget()
    graph.add_node("q"+str(statenumber))
    graph.layout(prog='sfdp', args='-Goverlap=scale')
    graph.draw("graph.png")
    refreshImage()
    updateList()
    statenumber+=1
def addLabel():
    global state1,state2,edgelabel
    forget()
    state1var=state1.get()
    state2var=state2.get()
    edge=edgelabel.get()
    if(state1var!="" and state2var!="" and edge!=""):
        graph.add_edge(state1var,state2var,edge,label=edge)
        graph.layout(prog='sfdp', args='-Goverlap=scale')
        graph.draw("graph.png")
        refreshImage()
    else:
        mg.showerror("Error","Invalid State/Edge Name")
graph=pgv.AGraph(directed=True)
graph.add_node("Start")
graph.layout(prog='sfdp', args='-Goverlap=scale')
graph.draw("graph.png")
img=Image.open("graph.png")
img=ImageTk.PhotoImage(img)
state1=Combobox(r,state="readonly",width=10)
state2=Combobox(r,state="readonly",width=10)
state1.config(values="Start")
state2.config(values="Start")
confirmdelbtn=Button(r,text="Delete",command=confirmdel)
opts=Combobox(r,state="readonly")
delbtn=Button(r,text="Delete Node",command=delete)
resetbtn=Button(r,text="Reset",command=reset)
addbtn=Button(r,text="Add New State",command=addState)
title=Label(r,text="Finite Automata Designer",font=("Arial",20))
display=Label(r,image=img)
edgelabel=Entry(r)
addlabel=Button(r,text="Add",command=addLabel)
Label(r,text="to",font=("Arial",12)).place(relx=0.41,rely=0.25,anchor="center")
Label(r,text="Transitions",font=("Arial",16)).place(relx=0.35,rely=0.18,anchor="center")
Label(r,text="Transition Label",font=("Arial",12)).place(relx=0.63,rely=0.18,anchor="center")
edgelabel.place(relx=0.64,rely=0.25,anchor="center")
delbtn.place(relx=0.59,rely=0.09,anchor="center")
display.place(relx=0.5,rely=0.7,anchor="center")
addlabel.place(relx=0.78,rely=0.25,anchor="center")
resetbtn.place(relx=0.35,rely=0.09,anchor="center")
addbtn.place(relx=0.47,rely=0.09,anchor="center")
title.place(relx=0.5,rely=0.03,anchor="center")
state1.place(relx=0.34,rely=0.25,anchor="center")
state2.place(relx=0.48,rely=0.25,anchor="center")
r.title("Finite Automata Designer")
r.geometry("800x600")
r.resizable(False,False)
r.mainloop()