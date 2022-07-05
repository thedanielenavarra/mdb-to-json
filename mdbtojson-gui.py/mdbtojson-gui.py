#!/usr/bin/python3

from tkinter import *
import os
import sys
from tkinter import filedialog

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
        print("PARSE")
        o.root.destroy()
        o.parseForm=Parse()

    def read(o):
        print("READ")
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