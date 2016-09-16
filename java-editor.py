import os

import tkinter as tk
from tkinter import font
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_menu()
        self.create_main()
        self.lines = []

        self.properties = []
        self.property_vals = []
        self.filepath = ""
        self.file = ""
        self.loaded = False

        root.geometry('{}x{}'.format(640,480))
        root.resizable(width=False,height=False)

    def cls(self):
        os.system('cls' if os.name=="nt" else 'clear')

    def save(self,loaded):
        if (not loaded):
            popup = Tk()
            label = Label(popup,text="You need to load a file to save it. Common sense")
            close = Button(popup,text="Close",command=lambda : popup.destroy())
            close.pack(side=BOTTOM)
            label.pack(side=TOP)
            return


        newlines = []
        for a in range(0,self.properties.__len__()):
            newlines.append(str(self.properties[a]).split("=")[0]+ "=" + str(self.property_vals[a])+"\n")

        file_opt = options = {}
        options['filetypes'] = [('PROPERTIES files', '.properties')]
        options['initialfile'] = 'myprops.properties'
        options['parent'] = root

        filename = asksaveasfilename(**file_opt)

        if filename:
            file = open(filename, 'w')
            file.writelines(newlines)

    def parsefile(self,osfile):
        try:
            newos = os.open(osfile,os.O_RDWR)
            self.open_button.destroy()
            self.open_label.destroy()
        except OSError:
            print("Unable to load .properties file")
            sys.exit()

        file = os.fdopen(newos,"r+")

        lines = file.readlines()


        for line in lines:
            line = line.replace("\n","")
            if ("=" in line): self.properties.append(line)


        for prop in self.properties:
            self.property_vals.append(prop.split("=")[1])
        loaded = True
        return file

    def create_main(self):
        self.open_label = Label(root,text="Open a file to start.",font=tk.font.Font(size=20))
        self.open_label.pack(side=TOP,pady=root.winfo_height())
        self.open_button = Button(root,text="Open",command=lambda : self.load_file(),font=tk.font.Font(size=14))
        self.open_button.pack(side=TOP,pady=root.winfo_height()/2)


    def create_menu(self):
        menu_bar = Menu(root)

        file_menu = Menu(menu_bar,tearoff=0)

        file_menu.add_command(label="Open",command=lambda : self.load_file())
        file_menu.add_command(label="Save",command=lambda : self.save(self))
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=lambda : sys.exit())

        about_menu = Menu(menu_bar,tearoff=0)
        about_menu.add_command(label="Info",command=lambda : self.show_info())

        menu_bar.add_cascade(label="File",menu=file_menu)
        menu_bar.add_cascade(label="About",menu=about_menu)

        root.config(menu=menu_bar)

        root.resizable(width=True,height=True)

    def create_list(self):
        #Create Listbox
        list_font = font.Font(size=18)
        list = Listbox(root,font=list_font)
        list.pack(ipadx=root.winfo_width(),ipady=root.winfo_height())

        #Add Scrollbar
        scrollbar = Scrollbar(list,orient=VERTICAL)
        scrollbar.pack(side=RIGHT,fill=Y)

        list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=list.yview)
        list.bind("<<ListboxSelect>>", self.onSelect)

        for num in range(self.properties.__len__()):

            list.insert(END,str(self.properties[num].split("=")[0]).upper())

        for prop in self.properties:
            print(". "+str(prop).split("=")[0])
        print("35. Save and Exit")

    def load_file(self):

        osfile = askopenfilename(filetypes=(("Properties Files", "*.properties"),
                                           ("All files", "*.*") ))
        if osfile:
            self.file = self.parsefile(osfile)
            self.create_list()

    def edit_value(self,num):
        print(num)
        edit_win = Tk()
        edit_win.title(str(self.properties[num]).split("=")[0])
        edit_win.geometry('{}x{}'.format(300,112))
        edit_win.resizable(width=False,height=False)
        v = StringVar()
        e = Entry(edit_win,textvariable=v)
        if (self.property_vals[num] == ""): e.insert(END,"NULL")
        else: e.insert(END,self.property_vals[num])


        label = Label(edit_win,text="Enter New Value")
        label.pack(side="top")
        e.pack(side="top",ipady=5,padx=50)
        btn = Button(edit_win,text="Save",command=lambda : self.save_value(e.get(),num,edit_win))
        btn.pack(side="bottom",pady=10)

    def save_value(self,val,num,win):
        close = True
        print(self.property_vals[num])
        self.property_vals[num] = val
        print(self.property_vals[num])
        win.destroy()



    def show_info(self):
        print("Info")
        info_win = Tk()
        info_win.geometry("{}x{}".format(300,112))
        info_win.title("Info")

        about_txt = Label(info_win,text="Java Properties Editor")
        author_txt = Label(info_win,text="Author:Nathan Estrada")

        about_txt.pack(side="top")
        author_txt.pack(side="top")

        close_btn = Button(info_win,text="Close",command=lambda : info_win.destroy())
        close_btn.pack(side="bottom",ipady=10,ipadx=15)


    def onSelect(self, event):
        widget = event.widget
        selection = widget.curselection()
        self.edit_value(selection[0])


root = tk.Tk()
root.title("Java Properties Editor")
root.size = 100
app = Application(master=root)
app.mainloop()
