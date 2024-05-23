import tkinter as tk

import os
import os.path
from os import listdir
from os.path import isfile, join
import sys
import pathlib
import shutil
import subprocess
import imghdr

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

import configparser
config = configparser.ConfigParser()


from multiprocessing import Process
import threading
from queue import Queue

root = TkinterDnD.Tk()
root.currentDir = os.getcwd()

#assumedLocation of img program if no config
defaultLocation = root.currentDir + "\img2nutexb.exe"
#default configuration
defaultConfig = configparser.ConfigParser()
defaultConfig['DEFAULT'] = {
    'arcDir': "",
    'sourceFile' : "",
    'modFile' : "",
    }


def CreateConfig():
    print("creating valid config")
    with open('config.ini', 'w+') as configfile:
        defaultConfig.write(configfile)
    config.read('config.ini')

#truncate strings for labels
def truncate(string,direciton=W,limit=40,ellipsis=True):
    if (len(string) < 3):
        return string
    text = ""
    addEllipsis = "..." if (ellipsis) else ""
    if direciton == W:
        text = addEllipsis+string[len(string)-limit:len(string)]
    else:
        text = string[0:limit]+addEllipsis
    return text

#show message
def message(text,type=""):
    type = type.lower()
    #what do you mean match type is only for 3.10?!?
    if type=="error":
        messagebox.showerror(root.title(),text)
    elif type=="warning":
        messagebox.showwarning(root.title(),text)
    else:
        messagebox.showinfo(root.title(),text)
    print(type+": "+text)
    
#check to make sure that the program is a valid file
def ValidExe():
    if (not root.arcDir): return False
    if (os.path.isdir(root.arcDir)):
    	return True
    return False

#make sure that it is a validated destination folder, otherwise quit
def IsValidArc():
    #Is this the directory with ArcExplorer.exe?
    if (os.path.exists(root.arcDir + r"/ArcExplorer.exe")):
        return True
    return False

#open folder dialogue
def setarcDir():
    messagebox.showinfo(root.title(),"Set ArcExplorer directory")
    root.arcDir = filedialog.askdirectory(title = "Select your ArcExplorer directory")
    if (root.arcDir == ""):
        root.destroy()
        sys.exit("Invalid folder")
    if (IsValidArc() == False):
        messagebox.showerror(root.title(),"Please select the root of your ArcExplorer folder")
        root.destroy()
        sys.exit("Invalid folder")
        

def ValidatePorgram():
    #if we don't have arc folder, then ask for it!
    if (ValidExe() == False):
        setarcDir()

        #write new location to config
        config.set("DEFAULT","arcDir",root.arcDir)
        with open('config.ini', 'w+') as configfile:
            config.write(configfile)

    #create output file
    outputFile = open('output.txt','w+')
    outputFile.close()


def HasValidSource():
    validPath = os.path.isfile(root.sourceFile)
    if (validPath):
    	return True
    return False

def HasValidMod():
    return os.path.isfile(root.modFile)

def setSource(value = ""):
    if value=="":
	    value = filedialog.askopenfilename(title = "Source File")
    root.sourceFile = value
    if (root.sourceFile != ""):
        root.source_color = ValidateFile(root.sourceFile,False)
        root.source_entry.config(text = truncate(root.sourceFile), fg = root.source_color)

    config.set("DEFAULT","sourceFile",root.sourceFile)
    with open('config.ini', 'w+') as configfile:
        config.write(configfile)

def findSource():
    toReturn = ""
    if root.modFile == "":
        return

    categories = ["/fighter/","/stage/","/ui/"]
    for cat in categories:
        if cat in root.modFile:
            filePath = root.modFile[root.modFile.index(cat):]
            toReturn = (root.arcDir+"/export"+filePath).replace("xml","")
            if (os.path.exists(toReturn)):
                break

    if not (os.path.exists(toReturn)):
        messagebox.showerror(root.title(),filePath + "not extracted from Arc")
        return
    setSource(toReturn)

def setMod(value=""):
    if value=="":
	    value = filedialog.askopenfilename(title = "Mod File")
    root.modFile = value
    if (root.modFile != ""):
        root.mod_color = ValidateFile(root.modFile,True)
        root.mod_entry.config(text = truncate(root.modFile), fg = root.mod_color)

    config.set("DEFAULT","modFile",root.modFile)
    with open('config.ini', 'w+') as configfile:
        config.write(configfile)

#GUI
def startGUI():
    #root.iconbitmap("icon.ico")
    root.width=450
    root.height=200
    root.geometry(str(root.width)+"x"+str(root.height))

    pythonInfo = "Python: " + sys.version
    root.status = Label(root, text=truncate(pythonInfo,E,14,False), bd=1, relief=SUNKEN, anchor=E)
    root.status.pack(side = BOTTOM, fill=X)
    mainlabel = Label(root, text="Drag and Drop param files into white space,\n or select them with the buttons", bd=1, relief=SUNKEN, anchor=N)
    mainlabel.pack(side = TOP, fill=X)

    sourceFrame = Frame(root)
    sourceFrame.pack()
    modFrame = Frame(root)
    modFrame.pack()
      

    source_label = Label(sourceFrame,width=50,text="Source File")
    source_label.pack(padx=8, side = TOP)
    root.source_color = ValidateFile(root.sourceFile,False)
    root.source_entry = Label(sourceFrame,width=45,relief="sunken",bg="white",text=truncate(root.sourceFile),fg=root.source_color)
    root.source_entry.drop_target_register(DND_FILES)
    root.source_entry.dnd_bind('<<Drop>>', lambda e: setSource(e.data))
    root.source_entry.pack(padx=8, side = LEFT)


    mod_label = Label(modFrame,width=50,text="Mod File")
    mod_label.pack(padx=8, side = TOP)
    root.mod_color = ValidateFile(root.modFile,True)
    root.mod_entry = Label(modFrame,width=45,relief="sunken",bg="white",text=truncate(root.modFile),fg=root.mod_color)
    root.mod_entry.drop_target_register(DND_FILES)
    root.mod_entry.dnd_bind('<<Drop>>', lambda e: setMod(e.data))
    root.mod_entry.pack(padx=8, side = LEFT)

    source_sep = Frame(sourceFrame,width = 4)
    source_sep.pack(side = RIGHT)
    find_btn = Button(sourceFrame, text = "Auto",width=7, command=findSource)
    find_btn.pack(padx=0,side = RIGHT)
    source_sep = Frame(sourceFrame,width = 4)
    source_sep.pack(side = RIGHT)
    source_btn = Button(sourceFrame, text = "Set",width=15, command=setSource)
    source_btn.pack(padx=0,side = RIGHT)

    mod_sep = Frame(modFrame,width = 8)
    mod_sep.pack(side = RIGHT)
    mod_btn = Button(modFrame, text = "Set",width=15, command=setMod)
    mod_btn.pack(padx=0,side = RIGHT)
    #create run button
    btnFrame = Frame(root)
    btnFrame.pack(side = BOTTOM,pady=8)
    run_btn = Button(btnFrame, text="Run", command=run,anchor=S,width=20)
    run_btn.pack(side = LEFT,padx=8)
    patch_btn = Button(btnFrame, text="Patch", command=patch,anchor=S,width=20)
    patch_btn.pack(side = RIGHT)

paramExtensions = [".prc",".stdat",".stprm"]
def ValidateFile(img,isMod):
    arcPath = root.arcDir in img
    if arcPath and isMod:
        return "orange"
    elif arcPath==False and isMod==False:
        return "orange"

    ext = os.path.splitext(img)[1]
    for param in paramExtensions:
    	if (ext == param) or (ext == param+"x") or (ext == param+"xml"):
    		return "black"
    return "red"

def printAndWrite(string,color="black"):
    print(string)
    root.status.config(text = string, fg = color)
    with open("output.txt", "a") as file:
        file.write(string)
        file.write("\n")
        
#main functions
def run():    
    main_run()

def patch():    
    main_run(True)

def main_run(patch=False):    
    #.\parcel patch prc.prc prc.prcxml prc_new.prc
    hasRed = (root.source_color == "red" or root.mod_color == "red")
    hasOrange = (root.source_color == "orange" or root.mod_color == "orange")
    if hasRed:
        messagebox.showerror(root.title(),"One or both files are not compatible with parcel!")
        return
    if hasOrange:
        if (root.mod_color == "orange"):
            res = messagebox.askquestion(root.title(), "Your mod file is located inside your ArcExplorer directory, do you still wish to create a patch file?")
        else:
            res = messagebox.askquestion(root.title(), "Your source file is located outside your ArcExplorer directory, do you still wish to create a patch file?")
        if res != 'yes':
            return

    xFile = root.modFile+"x"
    xmlFile = root.modFile+"xml"
    if patch:
        patchFile = root.modFile.replace("xml","")
    else:
        patchFile = os.path.splitext(root.sourceFile)[0]+"_new"+os.path.splitext(root.sourceFile)[1]

    subcallx = ["parcel.exe","diff",root.sourceFile,root.modFile,xFile]
    subcallxml = ["parcel.exe","diff",root.sourceFile,root.modFile,xmlFile,"--type","xml","--hashes",os.getcwd()+"/ParamLabels.csv"]
    subcallpatch = ["parcel.exe","patch",root.sourceFile,root.modFile,patchFile]

    with open('output.txt', 'a+') as stdout_file:
    	if root.modFile.endswith("xml") or root.modFile.endswith("x") or patch==True:
            process_output = subprocess.run(subcallpatch, stdout=stdout_file, stderr=stdout_file, text=True)
            print("Patch")
            print(process_output.__dict__)
    	else:
	        process_output = subprocess.run(subcallx, stdout=stdout_file, stderr=stdout_file, text=True)
	        print(process_output.__dict__)
	        process_output = subprocess.run(subcallxml, stdout=stdout_file, stderr=stdout_file, text=True)
	        print(process_output.__dict__)
    printAndWrite("Patch Created!")

def init(sourceFile="",modFile="",currentDir=""):
    root.title("parcelGUI")



    #create a config if necessary
    if (not os.path.isfile(root.currentDir + r"\config.ini")):
        CreateConfig()
    config.read('config.ini')

    #search and destination directory functions
    root.sourceFile = config["DEFAULT"]["sourceFile"]
    root.modFile = config["DEFAULT"]["modFile"]
    if not os.path.isfile(root.sourceFile):
    	root.sourceFile=""
    if not os.path.isfile(root.modFile):
    	root.modFile=""
    with open('config.ini', 'w+') as configfile:
        config.write(configfile)


    root.arcDir = config["DEFAULT"]["arcDir"]

#on window closed
def onClosed():
    root.destroy()
    sys.exit("User exited")
    

def Main():
    init()
    root.deiconify()
    ValidatePorgram()
    startGUI()

if __name__ == '__main__':
    Main()
    root.protocol("WM_DELETE_WINDOW", onClosed)
    root.mainloop()

