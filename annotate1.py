''''
####required installs######
None

##### To do  ###
1. Disable the next/prev button on excedding the pointer.

'''

from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import pathlib
import glob, os 
import matplotlib.image as mpimg
from PIL import Image, ImageTk
from tkinter import font as tkFont
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
### required classes

def set_image(top,path):
    global img3
    img = Image.open(path)
    img2 = img.resize((616,820),Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(img2)
    panel = Label(top,image = img3, justify=LEFT)
    panel.place(x=0,y=0)

####  default params
ext='JPG';
label_filename = 'labels.csv';
PROD=1;  ## run on default folder if 0.
Xres=1080;
Yres=850;
# setup gui
root = Tk(className='Image labeling GUI')
root.geometry(str(Xres)+'x'+str(Yres));
root.resizable(0,0)

#f = Figure()
#a = f.add_subplot(111)
## get the folder with images
#answer = filedialog.askdirectory(parent=root,
  #                               initialdir=os.getcwd(),
   #                              title="Please select a folder:")
messagebox.showinfo("warning","Select the images folder");                                 
if(PROD):
    flder = filedialog.askdirectory(initialdir =  "./", title = "Select A Folder")+'/'
else:
    flder='./set1/';

print('folder selected '+flder);


## check if the annotation exists partially/ if not create file
p = pathlib.Path(flder+label_filename)
filenames=[];
if p.is_file(): 
    print('annoation file exists');
    with open(flder+label_filename, encoding="utf-8") as file:
        filenames = [l.split(',')[0] for l in file]
    print(filenames);
   
else:
    print('creating new label file');
    label_file=open(flder+label_filename, 'w')
    label_file.close();
    
list_files=arr = glob.glob(flder+'*.'+ext)
list_files=sorted(list_files)
print(list_files);
LEN=len(list_files);
cur_ptr=-1;

while(cur_ptr<(LEN)):
    cur_ptr=cur_ptr+1;
    if(cur_ptr>=LEN):
        messagebox.showinfo("warning","Annotation is already done: Thank You");
        exit(0);
    #print(list_files[cur_ptr],cur_ptr,LEN)
    if not any(list_files[cur_ptr] in s for s in filenames):
        break;
    

print('pounter at '+str(cur_ptr));

cur_file=list_files[cur_ptr]
set_image(root,cur_file)

    
global sevrity_sel,ispresent_sel,type_sel,gradable;
sevrity_sel=0;
ispresent_sel=0;
type_sel=0;
gradable=1;

def NextCallback():
    global cur_ptr,ispresent_sel,sevrity_sel, type_sel,gradable;
    if(ispresent_sel==0):
        messagebox.showinfo("warning","Please select if cataract is present or not");
        return;
        
    if(sevrity_sel==0 and ispresent_var.get()==1):
        messagebox.showinfo("warning","Please select the severity"); 
        return;
        
    if(type_sel==0 and ispresent_var.get()==1):
        messagebox.showinfo("warning","Please select the type"); 
        return;
        
    comments = comment_box.get(1.0, END) 
    label_file=open(flder+label_filename, 'a')
    label_file.write(list_files[cur_ptr]+','+str(gradable)+','+str(ispresent_var.get())+','+str(sevrity.get())+','+str(type_cat.get())+','+str(comments));
    label_file.close();
    while(cur_ptr<LEN):
        cur_ptr=cur_ptr+1;
        if(cur_ptr>=LEN):
            messagebox.showinfo("warning","Annotation is already done: Thank You");
            exit(0);
        if not any(list_files[cur_ptr] in s for s in filenames):
            break;
            
    if(cur_ptr>=LEN):
        messagebox.showinfo("Annotation is already done: Thank You");
        exit(0);        
    cur_file=list_files[cur_ptr]
    set_image(root,cur_file)
    sevrity_sel=0;
    ispresent_sel=0;
    type_sel=0;
    gradable=1;
    text_progress.config(text="Progress:"+str(cur_ptr)+'/'+str(LEN));
    print(list_files[cur_ptr]+','+str(gradable)+','+str(ispresent_var.get())+','+str(sevrity.get())+','+str(type_cat.get())+','+str(comments));
    
def PrevCallback():
    global type_sel,sevrity_sel,ispresent_sel,gradable;
    type_sel=1;
    sevrity_sel=1;   
    ispresent_sel=1;
    gradable=0;
    NextCallback();

def sev_callback():
    global sevrity_sel;
    print('in sev call');
    sevrity_sel=1;

def ispresent_callback():
    global ispresent_sel;
    print('in present call');
    ispresent_sel=1;
    
    
def type_callback():
    global type_sel
    type_sel=1;


hev36=tkFont.Font(family='Helvetica', size=15, weight='bold');
text_progress = Label(root, height=1, width=15,font=hev36,text="Progress:"+str(cur_ptr+1)+'/'+str(LEN))
text_progress.place(x=int(0.75*Xres),y=(0.01*Yres));

## 
nextButton = Button(root, text ="Next", command = NextCallback,width=10,height=2, font=hev36).place(x=int(0.8*Xres),y=(0.73*Yres))

not_gradable = Button(root, text ="Not gradable", command = PrevCallback,width=10,height=1, font=hev36).place(x=int(0.8*Xres),y=(0.85*Yres))

## is present Radiobutton
ispresent_var = tk.IntVar()
ispresent_var.set(1)  # initializing the choice, i.e. Python
vales={'Yes':1,'No':0};
for (text,val) in vales.items():
    tk.Radiobutton(root, text=text,font=hev36,padx = 20,variable=ispresent_var,value=val,command=ispresent_callback).place(x=int(0.85*Xres),y=(0.25*Yres+int(val)*30));
    
text = Label(root, height=1, width=15,font=hev36,text="Is cataract Present")
text.place(x=int(0.68*Xres),y=(0.27*Yres));

## severity radio button
sevrity = tk.IntVar()
sevrity.set(0)  # initializing the choice, i.e. Python
vales={'1':1,'2':2,'3':3,'4':4};
for (text,val) in vales.items():
   tk.Radiobutton(root, text=text,font=hev36,padx = 20,variable=sevrity,value=val,command=sev_callback).place(x=int(0.85*Xres),y=(0.3*Yres+int(val)*30));
    
text2 = Label(root, height=1, width=9,font=hev36,text="Severity")
text2.place(x=int(0.76*Xres),y=(0.4*Yres));

# Type
type_cat = tk.IntVar()
type_cat.set(0)  # initializing the choice, i.e. Python
vales={'nuclear':1,'cortical':2,'sucapsular':3};#, , 
for (text,val) in vales.items():
   tk.Radiobutton(root, text=text,font=hev36,padx = 20,variable=type_cat,value=val,command=type_callback).place(x=int(0.85*Xres),y=(0.5*Yres+int(val)*30));
    
text2 = Label(root, height=1, width=9,font=hev36,text="Type")
text2.place(x=int(0.77*Xres),y=(0.55*Yres));


## comments
comment_box=Text(root, height=2, width=15);
comment_box.place(x=int(0.8*Xres),y=(0.67*Yres));

text3 = Label(root, height=1, width=9,font=hev36,text="Comments")
text3.place(x=int(0.69*Xres),y=(0.67*Yres));




if(cur_ptr!=0):
    messagebox.showinfo("warning","Already "+str(cur_ptr)+' images are labeled');
    
root.mainloop()