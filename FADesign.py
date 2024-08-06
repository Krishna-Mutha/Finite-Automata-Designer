from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mg
from tkinter.ttk import *
from PIL import ImageTk,Image
import pygraphviz as pgv
r=Tk()
global statenumber,nodes,finalstate
statenumber=1
finalstate=[]
def updateList():
    global opts,state1,state2,nodes
    nodes=graph.nodes()
    opts.config(values=nodes[1::])
    state1.config(values=nodes)
    state2.config(values=nodes)
def refreshImage():
    global img,display
    img=Image.open("graph.png")
    width,height=img.size
    if(width>750 and height <=340):
        img=img.resize((750,height))
    elif(height>340 and width<=750):
        img=img.resize((width,340))
    elif(height>340 and width>750):
        img=img.resize((750,340))
    # img=img.resize((750,340))
    img=ImageTk.PhotoImage(img)
    display.config(image=img)
    display.image=img
def forget():
    global opts,confirmdelbtn
    opts.place_forget()
    confirmdelbtn.place_forget()
def confirmdel():
    global opts,state1,state2,nodes
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
        if(state1.get()==temp_del):
            state1.set("")
        if(state2.get()==temp_del):
            state2.set("")
        refreshImage()
        updateList()
def delete():
    global opts,confirmdelbtn
    opts.place(relx=0.65,rely=0.09,anchor="w")
    confirmdelbtn.place(relx=0.77,rely=0.09,anchor="w")
def reset():
    global display,statenumber,nodes,finalstate
    forget()
    statenumber=1
    graph.clear()
    graph.add_node("Start")
    graph.layout(prog='sfdp', args='-Goverlap=scale')
    graph.draw("graph.png")
    nodes=graph.nodes()
    finalstate=[]
    refreshImage()
    updateList()
def addState():
    global statenumber,display,nodes
    forget()
    graph.add_node("q"+str(statenumber))
    graph.layout(prog='sfdp', args='-Goverlap=scale')
    graph.draw("graph.png")
    nodes=graph.nodes()
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
def confirmfinal():
    global finalstate,nodes
    markfinal=markentry.get()
    removefinal=removeentry.get()
    if(markfinal!=""):
        temp_node=graph.get_node(markfinal)
        temp_node.attr["fillcolor"]="red"
        graph.draw("graph.png")
        finalstate.append(markfinal)
        markentry["values"]=list(set(nodes)-set(finalstate))
        removeentry["values"]=finalstate
        markentry.set("")
        refreshImage()
        t.destroy()
    if(removefinal!=""):
        temp_node=graph.get_node(removefinal)
        temp_node.attr["fillcolor"]="white"
        graph.draw("graph.png")
        finalstate.remove(removefinal)
        removeentry["values"]=finalstate
        markentry["values"]=list(set(nodes)-set(finalstate))
        removeentry.set("")
        refreshImage()
        t.destroy()
    if(removefinal=="" and markfinal==""):
        mg.showerror("Error","Select a state")
        t.focus_force()
def configFinal():
    global markentry,removeentry,t,nodes
    t=Tk()
    Label(t,text="Mark a final state",font=("Arial",12)).place(relx=0.2,rely=0.1,anchor="center")
    Label(t,text="Remove a final state",font=("Arial",12)).place(relx=0.7,rely=0.1,anchor="center")
    markentry=Combobox(t,state="readonly")
    removeentry=Combobox(t,state="readonly")
    markentry["values"]=list(set(nodes)-set(finalstate))
    removeentry["values"]=finalstate
    confirm=Button(t,text="Confirm",command=confirmfinal)
    markentry.place(relx=0.2,rely=0.2,anchor="center")
    confirm.place(relx=0.45,rely=0.6,anchor="center")
    removeentry.place(relx=0.7,rely=0.2,anchor="center")
    t.geometry("500x200")
    t.title("Configure Final State")
    t.resizable(False,False)
    t.mainloop()
def test():
    test_string=testentry.get()
    if(test_string!=""):
        currentnode="Start"
        edges=graph.edges(keys=True)
        for i in test_string:
            for j in graph.out_edges_iter(currentnode,keys=True):
                if(i==j[2]):
                    currentnode=j[1]
                    break
            continue
        if(currentnode in finalstate):
            print("Passed")
        else:
            print("Failed")
graph=pgv.AGraph(directed=True,strict=False)
graph.node_attr["style"]="filled"
graph.node_attr["fillcolor"]="white"
graph.add_node("Start")
graph.layout(prog='sfdp', args='-Goverlap=scale')
graph.draw("graph.png")
nodes=graph.nodes()
img=Image.open("graph.png")
# img=img.resize((750,340))
img=ImageTk.PhotoImage(img)
state1=Combobox(r,state="readonly",width=10)
state2=Combobox(r,state="readonly",width=10)
state1.config(values="Start")
state2.config(values="Start")
configfinal=Button(r,text="Configure Final States",command=configFinal)
confirmdelbtn=Button(r,text="Delete",command=confirmdel)
opts=Combobox(r,state="readonly",width=10)
delbtn=Button(r,text="Delete Node",command=delete)
resetbtn=Button(r,text="Reset",command=reset)
addbtn=Button(r,text="Add New State",command=addState)
title=Label(r,text="Finite Automata Designer",font=("Arial",20))
testbtn=Button(r,text="Test",command=test)
testentry=Entry(r,width=60)
display=tk.Label(r,image=img,width=750,height=340)
edgelabel=Entry(r)
addlabel=Button(r,text="Add",command=addLabel)
Label(r,text="to",font=("Arial",12)).place(relx=0.41,rely=0.25,anchor="center")
Label(r,text="Transitions",font=("Arial",16)).place(relx=0.35,rely=0.18,anchor="center")
Label(r,text="Transition Label",font=("Arial",12)).place(relx=0.63,rely=0.18,anchor="center")
Label(r,text="Test input string",font=("Arial",16)).place(relx=0.38,rely=0.32,anchor="center")
edgelabel.place(relx=0.64,rely=0.25,anchor="center")
testbtn.place(relx=0.79,rely=0.37,anchor="center")
configfinal.place(relx=0.22,rely=0.09,anchor="center")
testentry.place(relx=0.5,rely=0.37,anchor="center")
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