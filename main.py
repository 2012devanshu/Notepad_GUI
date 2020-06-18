from tkinter import *
from tkinter import messagebox, ttk
from tkinter import filedialog as fd
import pyautogui as pag
import os
import time

author : 'Devanshu'

class Notepad:

    def __init__(self, root):
        self.root = root
        self.root.geometry('900x485+50+50')
        self.note_icon = PhotoImage(file='Notepad_icon.png')
        self.root.iconphoto(True, self.note_icon)
        self.data = StringVar()
        self.title = 'Untitled'
        self._file_ = None
        self._wrap_ = NONE
        self._data_trans_ = ""
        self._check_wrap_ = IntVar()
        self.root.title(self.title+' - Notepad')
        self.scroll_cursor = 'arrow'
        self.event = ""
        self.font = "Lucida Handwriting"
        self.font_style = "Regular"
        self.font_size = 16
    
    def main(self):

        menubar      =  Menu(self.root)
        fileoption   =  Menu(menubar, tearoff=0)
        editoption   =  Menu(menubar, tearoff=0)
        formatoption =  Menu(menubar, tearoff=0)
        helpoption   =  Menu(menubar, tearoff=0)

        # FILE OPTION ---------------------------------------------------------------------------------

        fileoption.add_command(label='New'+' '*20+'Ctrl+N', command= lambda : self._new_(self.event))
        fileoption.add_command(label='Open...'+' '*15+'Ctrl+O', command= lambda : self._open_(self.event))
        fileoption.add_command(label='Save'+' '*20+'Ctrl+S', command= lambda : self._save_(self.event))
        fileoption.add_command(label='Save as'+' '*16+'F12', command= lambda : self._saveas_(self.event))
        fileoption.add_separator()
        
        #fileoption.add_command(label='Print'+' '*20+'Ctrl+P', command=self.root.quit)
        #fileoption.add_separator()
        fileoption.add_command(label='Exit', command=self.root.quit)

        # EDIT OPTION ---------------------------------------------------------------------------------

        editoption.add_command(label='Undo'+' '*15+'Ctrl+Z', command= lambda : self._undo_(self.event))
        editoption.add_separator()
        editoption.add_command(label='Cut'+' '*18+'Ctrl+X', command= lambda : self._cut_(self.event))
        editoption.add_command(label='Copy'+' '*15+'Ctrl+C', command= lambda : self._copy_(self.event))
        editoption.add_command(label='Paste'+' '*15+'Ctrl+v', command= lambda : self._paste_(self.event))
        editoption.add_separator()
        editoption.add_command(label='Select All'+' '*9+'Ctrl+A', command= lambda : pag.hotkey('ctrl','a'))
        editoption.add_command(label='Time/Date'+' '*8+'F5', command= lambda : self._time_date_(self.event))

        menubar.add_cascade(label='File', menu=fileoption)
        menubar.add_cascade(label='Edit', menu=editoption)
        menubar.add_command(label="\u22EE")
        

        # FORMAT OPTION ---------------------------------------------------------------------------------

        formatoption.add_checkbutton(label='Word Wrap', command=lambda:self._word_wrap_(self.base), variable = self._check_wrap_)
       

        menubar.add_cascade(label='Format', menu=formatoption)
        menubar.add_command(label="\u22EE")
      

        # Help OPTION ---------------------------------------------------------------------------------
        
        helpoption.add_command(label='About  Notepad', command=self.about)
        menubar.add_cascade(label='Help', menu=helpoption)

        root.protocol("WM_DELETE_WINDOW", lambda : self.without_save(self.event))

        self.root.config( menu=menubar)
        self._text_box_()
        
    def about(self):
        messagebox.showinfo(title='About', message = 'Notepad created by Devanshu')


    def without_save(self,event):
        
        if self.title == 'Untitled' and self.base.get(1.0, END+"-1c") == "":
            self.root.destroy()
           
        

        elif self.title == 'Untitled':
            message = messagebox.askyesnocancel('Notepad', 'Do you want to save change to Untitled?')

            if self._file_ == "":
                self._file_ = None

            elif message == NO:
                self.root.destroy()

            elif message == YES:
                self._save_(self.event)
                self.root.destroy()
    



    def _word_wrap_(self, text):
        self.scroll_x.pack_forget()
        self.scroll_y.pack_forget()
        self._data_trans_ = text.get(1.0, END+"-1c")
        text.pack_forget()
        text.grid_forget()
        if self._check_wrap_.get() != 0:
            self._wrap_ = WORD
        else:
            self._wrap_ = NONE
        self._text_box_()

    def _text_box_(self):

        self.base = Text(self.root, wrap=self._wrap_, font=((self.font, self.font_style), self.font_size))
        self.base.grid(sticky=N + E + S + W)
        self.base.insert(END, self._data_trans_)
        self.base.config(undo=2, maxundo=2)

        if self._check_wrap_.get() == 0:
            self.scroll_x = Scrollbar(self.base, orient=HORIZONTAL, cursor=self.scroll_cursor)
            self.scroll_x.pack(side=BOTTOM, fill='x')
            self.scroll_x.config(command=self.base.xview)
            self.base.config(xscrollcommand=self.scroll_x.set)
            
        self.scroll_y = Scrollbar(self.base, cursor=self.scroll_cursor)
        self.scroll_y.pack(side=RIGHT, fill='y')
        self.scroll_y.config(command=self.base.yview)
        self.base.config(yscrollcommand=self.scroll_y.set)

        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1) 

     # ALL BINDINGS ----------------------------------------------------------------------------------------

        
        self.base.bind("<Control-n>", self._new_)
        self.base.bind("<Control-o>", self._open_)
        self.base.bind("<Control-s>", self._save_)
        self.base.bind("<F12>", self._saveas_)
        self.base.bind("<F5>", self._time_date_)
        self.base.bind("<Alt-F4>", self.without_save)

    def _new_(self, event):

            if self.title == 'Untitled':
                message = messagebox.askyesnocancel('Notepad', 'Do you want to save change to Untitled?')

                if message == YES:
                    self._save_(self.event)
                elif message == NO:
                    self.root.title("Untitled - Notepad") 
                    self.title = 'Untitled'
                    self.base.delete(1.0, END)
                else:
                    pass

    def _save_(self, event):
        if self._file_ is None:

            self._file_ = fd.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Documents",".txt"),
                                                                               ("All Files",".")])
            
            if self._file_ == "":
                self._file_ = None
            else:
                f = open(self._file_,'w')
                f.write(self.base.get(1.0,END))
                f.close()
                

        else:
            f = open(self._file_,'w')
            f.write(self.base.get(1.0,END))
            f.close()
        self.root.title(os.path.basename(self._file_)+' - Notepad')
        self.title = os.path.basename(self._file_)

    def _saveas_(self, event):
        self._file_ = fd.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Documents",".txt"),
                                                                               ("All Files",".")])

        if self._file_ == "":
            self._file_ = None
        else:
            f = open(self._file_,'w')
            f.write(self.base.get(1.0,END))
            f.close()

    def _open_(self, event):
        self._file_ = fd.askopenfilename(defaultextension=".txt",filetypes=[("Text Documents",".txt"),
                                                                               ("All Files",".")])
        if self._file_ == "":
            self._file_ = None
        else:
            f = open(self._file_,'r')
            try:
                self.base.delete(1.0, END)
            except:
                pass

            self.base.insert(1.0,f.read())
            self.root.title(os.path.basename(self._file_)+' - Notepad')
            self.title = os.path.basename(self._file_)
            f.close()

    def _cut_(self, event):
        self.base.event_generate('<<Cut>>')

    def _copy_(self, event):
        self.base.event_generate('<<Copy>>')
        #self._index_()

    def _paste_(self, event):
        self.base.event_generate('<<Paste>>')
    
    def _undo_(self, event):
        self.base.event_generate('<<Undo>>')

    
    def _time_date_(self, event):
        now = time.localtime(time.time())
        self.base.insert(END,time.strftime("%I:%M %p %d/%m/%Y", now))
        
    

if __name__ == "__main__":
    root = Tk()
    n = Notepad(root)
    n.main()
    root.mainloop()
