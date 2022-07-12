#!/usr/bin/python3

import os
import sys
import json
from os import walk
from tkinter import *
from inspect import getfile
from tkinter import filedialog
from tkinter.ttk import Treeview


def getfiles(path, extension):
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break
    return [f for f in files if f.endswith(extension)]

def gettables(db):
    tables = []
    db=open(db, 'r')
    for line in db:
        tables.append(line[:-1])
    db.close()
    return tables

class Read:
    def readtable(o):
        fn=o.data["json"]+"/"+o.selectedDB[:-6]+o.selectedTable+".json"
        print("File name: "+fn)
        f=open(fn, "r")
        l=0
        ll=0
        arr=[]
        varr=[]
        o.T_d.delete(*o.T_d.get_children())
        for line in f:
            arr=json.loads(line)
            if l==0:
                o.T_d["columns"]=[0]*len(arr)
                print("Added columns: "+str(len(arr)))
            for k in arr:
                varr.append(arr[k])
                if l==0:
                    o.T_d.column("#"+str(ll+1), width=10, stretch=NO, anchor=LEFT)
                    o.T_d.heading("#"+str(ll+1), text=k)
                    print("Adding key: "+k)
                    ll+=1
            if l==0:
                print("Adding row: ", tuple(varr))
                print("From json: ", arr)
            l+=1
            o.T_d.insert("", "end", values=tuple(varr))
            varr=[]
                


    def chgdb(o):
        if(len(o.LL_db.curselection())>0):
            o.selectedDB=o.LL_db.get(o.LL_db.curselection())
            o.LL_tables.delete(0,END)
            tables=gettables(o.data["tables"]+o.selectedDB)
            for t in tables:
                o.LL_tables.insert(END,t)

    def chgtables(o):
        if(len(o.LL_tables.curselection())>0):
            o.selectedTable=o.LL_tables.get(o.LL_tables.curselection())
            o.readtable()
        

    def read(o):
        o.data["json"]=o.E_i.get()
        o.data["tables"]=o.E_t.get()
        o.tables=getfiles(o.data["tables"], ".tables")
        o.json=getfiles(o.data["json"], ".json")
        o.LL_db.delete(0,END)
        o.LL_tables.delete(0,END)
        for f in o.tables:
            o.LL_db.insert(END,f[:])
        
    def browse(o, key):
        o.data[key]=filedialog.askdirectory(initialdir = "/",title = "Select input (."+key+") directory")
        if key=="json":
            o.E_i.delete(0,END)
            o.E_i.insert(0,o.data[key])
        elif key=="tables":
            o.E_t.delete(0,END)
            o.E_t.insert(0,o.data[key])
    def __init__(o):
        o.data={}
        o.tables=[]
        o.json=[]
        o.selectedDB=0
        o.selectedTable=0
        o.root=Tk()
        o.L_i=Label(o.root,text="JSON path:")
        o.L_i.grid(row=0,column=0)
        o.E_i=Entry(o.root)
        o.E_i.grid(row=0,column=1)
        o.B_i=Button(o.root,text="Browse",command=lambda:o.browse("json"))
        o.B_i.grid(row=0,column=2)
        o.L_t=Label(o.root,text="Tables path:")
        o.L_t.grid(row=1,column=0)
        o.E_t=Entry(o.root)
        o.E_t.grid(row=1,column=1)
        o.B_t=Button(o.root,text="Browse",command=lambda:o.browse("tables"))
        o.B_t.grid(row=1,column=2)
        o.B_read=Button(o.root,text="Read",command=lambda:o.read())
        o.B_read.grid(row=2,column=1)
        o.LL_db=Listbox(o.root)
        o.LL_db.bind("<<ListboxSelect>>",lambda event:o.chgdb())
        o.LL_db.grid(row=3,column=0)
        o.LL_tables=Listbox(o.root)
        o.LL_tables.grid(row=3,column=1)
        o.T_d=Treeview(o.root)
        o.T_d.grid(row=3,column=2)
        o.LL_tables.bind("<<ListboxSelect>>",lambda event:o.chgtables())
        o.E_i.insert(0, "/home/daniele/trash/mdbToJSON/JSON")
        o.E_t.insert(0, "/home/daniele/trash/mdbToJSON/")
        o.root.mainloop()





class Parse:
    def browse(o, key):
        if key=="logfile":
            o.data[key]=filedialog.asksaveasfilename(initialdir = "/",title = "Save log file as...",filetypes = (("log files","*.log"),("all files","*.*")))
            o.E_l.delete(0,END)
            o.E_l.insert(0,o.data[key])
        if key=="input":
            o.data[key]=filedialog.askdirectory(initialdir = "/",title = "Select input (.mdb) directory")
            o.E_i.delete(0,END)
            o.E_i.insert(0,o.data[key])
        if key=="output":
            o.data[key]=filedialog.askdirectory(initialdir = "/",title = "Select output (.json) file")
            o.E_o.delete(0,END)
            o.E_o.insert(0,o.data[key])
        if key=="table":
            o.data[key]=filedialog.askdirectory(initialdir = "/",title = "Select output (.table) directory")
            o.E_t.delete(0,END)
            o.E_t.insert(0,o.data[key])

    def start(o):
        o.data["logfile"]=o.E_l.get()
        o.data["input"]=o.E_i.get()
        o.data["output"]=o.E_o.get()
        o.data["table"]=o.E_t.get()
        o.data["execstr"]="../script/mdbtojson -l "+o.data["logfile"]+" -i "+o.data["input"]+" -o "+o.data["output"]+" -t "+o.data["table"]
        res=os.system(o.data["execstr"])
        print(o.data["execstr"], res)

    def __init__(o):
        o.execstr=""
        o.data={"logfile":"","input":"","output":"","table":""}
        o.root=Tk()
        o.root.title("MDB to JSON - Parser")
        o.root.geometry("500x500")
        o.L_l=Label(o.root,text="Log file:")
        o.L_l.grid(row=0,column=0)
        o.L_i=Label(o.root,text="Input (.mdb) path:")
        o.L_i.grid(row=1,column=0)
        o.L_o=Label(o.root,text="Output (.json) path:")
        o.L_o.grid(row=2,column=0)
        o.L_t=Label(o.root,text="Output (.table) path:")
        o.L_t.grid(row=3,column=0)
        o.E_l=Entry(o.root)
        o.E_l.grid(row=0,column=1)
        o.E_i=Entry(o.root)
        o.E_i.grid(row=1,column=1)
        o.E_o=Entry(o.root)
        o.E_o.grid(row=2,column=1)
        o.E_t=Entry(o.root)
        o.E_t.grid(row=3,column=1)
        o.B_l=Button(o.root,text="Browse",command=lambda:o.browse("logfile"))
        o.B_l.grid(row=0,column=2)
        o.B_i=Button(o.root,text="Browse",command=lambda:o.browse("input"))
        o.B_i.grid(row=1,column=2)
        o.B_o=Button(o.root,text="Browse",command=lambda:o.browse("output"))
        o.B_o.grid(row=2,column=2)
        o.B_t=Button(o.root,text="Browse",command=lambda:o.browse("table"))
        o.B_t.grid(row=3,column=2)
        o.B_start=Button(o.root,text="Start",command=o.start)
        o.B_start.grid(row=4,column=1) 
        o.root.mainloop()

class Mdbtojson:
    def parse(o):
        o.root.destroy()
        o.parseForm=Parse()

    def read(o):
        o.root.destroy()
        o.readForm=Read()
    def __init__(o):
        o.root=Tk()
        o.root.title("MDB to JSON")
        o.root.geometry("500x500")
        o.button_read=Button(o.root,text="Parse .mdb files to .json",command=o.parse)
        o.button_read.pack()
        o.button_read=Button(o.root,text="Read .json databases",command=o.read)
        o.button_read.pack()
        o.root.mainloop()
o=Mdbtojson()