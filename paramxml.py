import os
import os.path
import sys
import subprocess

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title("yamlist")
root.withdraw()

paramExtensions = [".prc",".stdat",".stprm"]

def main(args):
    file = os.getcwd()+"/vl.prc"
    #Support Drag n Drop, or select a file manually
    if (len(args)>1):
        file = args[1]
    else:
        filetypes = (
            ('All File Types', '*.prc *.prcxml'),
            ('prc', '*.prc'),
            ('prcxml', '*.prcxml')
        )
        file = filedialog.askopenfilename(title = "Select file",filetypes =filetypes)
        if not file:
            return
    if not (os.path.exists(file)):
        messagebox.showerror(root.title(),"File does not exists")
        return

    #Determine if we are converting prc to Yaml or Yaml to prc
    inputprc = True
    path = os.path.split(file)

    ext = os.path.splitext(path[1])[1]
    if (ext.endswith("xml")):
        inputprc = False
    newExt = ext + "xml" if inputprc else ext.replace("xml","")
    newFile = file.replace(ext,newExt)

    #if (os.path.exists(newFile)):
    #    res = messagebox.askquestion(root.title(), "Overwrite existing "+newExt+" file?")
    #    if res != 'yes':
    #        return

    subcall = ["paramxml.exe",file,"-d" if inputprc else "-a","-l",os.getcwd()+"/ParamLabels.csv","-o",newFile]
    with open('output.txt', 'a+') as stdout_file:
        process_output = subprocess.run(subcall, stdout=stdout_file, stderr=stdout_file, text=True)
        print(process_output.__dict__)

    #Make sure the output file exists
    if not (os.path.exists(newFile)):
        messagebox.showerror(root.title(),"Conversion Failed")
        return


main(sys.argv)
