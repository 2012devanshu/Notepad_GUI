from tkinter import *
import tempfile, base64, zlib
from tkinter import font


class Font:
    def __init__(self):
        self.font = Tk()
        self.font.geometry("424x438+150+150")
        self.font.title("Font")
        self.font.configure(background='gray94')
        self.font.resizable(0,0)
        
        self.font_name = sorted([i for i in font.families() if i[0]!="@"])
        print(len(self.font_name))
        self.font_style_names = ['Regular', 'italic', 'bold']
        self.font_size = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
        self.font_name_val = StringVar()
        self.size_val = IntVar()
        self.style_val = StringVar()

        self.font_name_val.set('Arial')
        self.size_val.set(10)
        self.style_val.set('Regular')        


        ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
            'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

        _, ICON_PATH = tempfile.mkstemp()
        with open(ICON_PATH, 'wb') as icon_file:
            icon_file.write(ICON)
        self.font.iconbitmap(default=ICON_PATH)

        # ------------------------ Font ---------------------------

        self.font_frame = Frame(self.font, width=19, height=6)
        self.font_frame.place(x=13, y=52)
        self.font_label = Label(self.font, text='Font:')
        self.font_label.place(x=10, y=10)
        scrollbar = Scrollbar(self.font_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.mylist_font = Listbox(self.font_frame, yscrollcommand=scrollbar.set, width = 19, height=7)
        
        for i in self.font_name:
            self.mylist_font.insert(END, str(i))
        self.mylist_font.configure(font=('Arial',11))
            
        self.mylist_font.bind('<<ListboxSelect>>',self.curselect_font)
        self.mylist_font.pack()
        scrollbar.config(command=self.mylist_font.yview)
        self.font_text = Entry(self.font, width=28, relief=GROOVE, textvariable = self.font_name_val, justify=LEFT, bd=2)
        self.font_text.place(x=13, y=30, height=23)
        
        # ------------------------ Font - Styles ---------------------------

        x1 = 199
        self.style_frame = Frame(self.font, bd = 1, width=12, height=6)
        self.style_frame.place(x=x1, y=51)
        self.style_label = Label(self.font, text='Font style:')
        self.style_label.place(x=x1, y=10)
        scrollbar = Scrollbar(self.style_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.mylist_style = Listbox(self.style_frame, yscrollcommand=scrollbar.set, width = 12, height=7)
        
        for i in self.font_style_names:
            self.mylist_style.insert(END, str(i))
        self.mylist_style.configure(font=('Arial',11))
            
        self.mylist_style.bind('<<ListboxSelect>>', self.font_style_val)
        self.mylist_style.pack()
        scrollbar.config(command=self.mylist_style.yview)
        self.style_text = Entry(self.font, width=21, relief=GROOVE, textvariable = self.style_val, justify=LEFT, bd=2)
        self.style_text.place(x=x1, y=30, height=23)

        # ------------------------ Size ---------------------------

        x2 = x1 + 145
        self.size_frame = Frame(self.font, bd = 1, width=6, height=6)
        self.size_frame.place(x=x2, y=51)
        self.size_label = Label(self.font, text='Size:')
        self.size_label.place(x=x2, y=10)
        scrollbar = Scrollbar(self.size_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.mylist_size = Listbox(self.size_frame, yscrollcommand=scrollbar.set, width = 6, height=7)
        
        for i in self.font_size:
            self.mylist_size.insert(END, str(i))
        self.mylist_size.configure(font=('Arial',10))
            
        self.mylist_size.bind('<<ListboxSelect>>', self.font_size_val)
        self.mylist_size.pack()
        #print(font_size_val)
        scrollbar.config(command=self.mylist_size.yview)
        self.size_text = Entry(self.font, width=10, relief=GROOVE, justify=LEFT, bd=2)
        self.size_text.place(x=x2, y=30, height=23)

        # ------------------------ Sample ---------------------------
        #print((self.size_text.get()))
        self.sample_label = LabelFrame(self.font, text=' Sample ', bd=2, relief=GROOVE)
        #self.sample_label.pack()
        self.sample_label.place(x=x1, y=200, width=205, height=86)
        self.text = Label(self.sample_label,text = 'AaBbYyZz', font=( (self.font_text.get(), self.style_text.get()), int(self.size_val.get())), justify=CENTER)
        self.text.pack()
        
        # ------------------------ button ---------------------------

        self.button_ok = Button(self.font, text = 'OK', width=8, command = self.result)
        self.button_ok.place(x=265, y=400)
        self.button_cancel = Button(self.font, text = 'Cancel', width=8, command = self.font.destroy)
        self.button_cancel.place(x=345, y=400)

        mainloop()
        
        print('Last:  ',self.font_name_val)  

    def result(self):
        
        self.output = ((self.font_text.get(), self.style_text.get()), int(self.size_val.get()))
        print(self.output)
        self.font.destroy()
        return self.output

    def curselect_font(self, event):
        widget = event.widget
        selection=widget.curselection()
        element = widget.get(selection)
        #element = str(self.mylist_font.get(ACTIVE))
        print(element)
        self.font_name_val.set(element)
        self.font_text.delete (0,len(self.font_text.get()))
        self.font_text.insert(END, element)
        self.text.config(font=( (element, self.style_text.get()), int(self.size_val.get())))


    def font_size_val(self, event):
        widget = event.widget
        selection=widget.curselection()
        picked = widget.get(selection)
        #picked = int(self.mylist_size.get(ACTIVE))
        self.size_val.set("")
        self.size_val.set(int(picked))
        self.size_text.delete (0,len(self.size_text.get()))
        self.size_text.insert(END, picked)
        self.text.config(font=( (self.font_text.get(), self.size_text.get()), int(picked)))

    def font_style_val(self, event):
        widget = (event.widget).curselection()
        selection=widget
        picked = widget.get(selection)
        #picked = self.mylist_style.get(ACTIVE)
        self.style_val.set(picked)
        self.style_text.delete (0,len(self.style_text.get()))
        self.style_text.insert(END, picked)
        self.text.config(font=( (self.font_text.get(), picked), int(self.size_val.get())))

    def font_name_func(self, event):
        widget = event.widget
        selection=widget.curselection()
        picked = widget.get(selection)
        self.font_name_val.set(picked)
        self.font_text.delete (0,len(self.font_text.get()))
        self.font_text.insert(END, picked)
        self.text.config(font=( (self.font_name_val, self.style_val), int(self.size_val.get())))



    '''def font_name_func (self,event) :
        widget = (event.widget)
        selection=widget.curselection()
        picked = widget.get(selection)
        #print(widget)
        #print(selection)
        #print(picked)
        #self.font_name_val = picked
        #self.text.set(self.font_name_val)
        #self.text.config(font=(self.font_name_val,10))'''



f = Font()
#print(f.result())






'''#self.style_frame = Frame(self.root, bg='white')
        #self.style_frame.place(x=5, y=10)
        #self.root.mainloop()
        self.text1 = Text(self.root)
        self.text1.pack()
        butt = Button (self.root, command=self.press)
        butt.pack()
        #text1.configure(font='helvetica 12')
        #text2 = Text(self.root, font=(('Lucida Handwriting', 'italic'),15))
        #text2.pack()
        #text2.insert(END,'This is new')
        mainloop()
        def press(self):
        self.text1.configure(font='helvetica 12')
        print("done")'''
