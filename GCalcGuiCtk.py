#imports
import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from GCDbSqlite import GCDbSqlite

class GCalcGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=GCDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title("General Weighted Average Calculator")
        self.geometry('1400x630')
        self.config(bg='#49302E')
        self.resizable(False, False)

        self.font1 = ('Garamond', 15, 'bold')
        self.font2 = ('Garamond', 12, 'bold')

        self.clc_label = self.newCtkLabel('Class Code')
        self.clc_label.place(x=1090, y=20)
        self.clc_entry = self.newCtkEntry()
        self.clc_entry.place(x=1090, y=50)

        self.subject_label = self.newCtkLabel('Subject')
        self.subject_label.place(x=1090, y=90)
        self.subject_cboxVar = StringVar()
        self.subject_cboxOptions = ['English', 'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Social Science']
        self.subject_cbox = self.newCtkComboBox(options=self.subject_cboxOptions, 
                                    entryVariable=self.subject_cboxVar)
        self.subject_cbox.place(x=1090, y=120)

        self.units_label = self.newCtkLabel('Units')
        self.units_label.place(x=1090, y=160)
        self.units_cboxVar = StringVar()
        self.units_cboxOptions = ["1.0", "2.0", "3.0", "4.0", "5.0"]
        self.units_cbox = self.newCtkComboBox(options=self.units_cboxOptions, 
                                    entryVariable=self.units_cboxVar)
        self.units_cbox.place(x=1090, y=190)

        self.gpercent_label = self.newCtkLabel('Grade Percentage')
        self.gpercent_label.place(x=1090, y=230)
        self.gpercent_entry = self.newCtkEntry()
        self.gpercent_entry.place(x=1090, y=260)



        self.add_button = self.newCtkButton(text='Add Class',
                                onClickHandler=self.add_entry,
                                fgColor='#DDFFAB', bgColor='#49302E',
                                hoverColor='#00850B',
                                borderColor='#DDFFAB')
        self.add_button.place(x=1090,y=320)

        self.delete_button = self.newCtkButton(text='Delete Class',
                                    onClickHandler=self.delete_entry, 
                                    fgColor='#FFA078', bgColor='#49302E',
                                    hoverColor='#AE0000',
                                    borderColor='#FFA078')
        self.delete_button.place(x=1090,y=360)

        self.new_button = self.newCtkButton(text='New Class', bgColor='#49302E', fgColor='#FFFFFF', borderColor='#FFFFFF',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=1090,y=400)

        self.update_button = self.newCtkButton(text='Update Class', bgColor='#49302E', fgColor='#FFFFFF', borderColor='#FFFFFF',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=1090,y=440)

        self.import_button = self.newCtkButton(text='Import from CSV', bgColor='#49302E', fgColor='#FFFFFF', borderColor='#FFFFFF' ,
                                    onClickHandler=self.import_from_csv)
        self.import_button.place(x=1090,y=480)

        self.export_button = self.newCtkButton(text='Export to CSV', bgColor='#49302E', fgColor='#FFFFFF', borderColor='#FFFFFF',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=1090,y=520)

        self.exjson_button = self.newCtkButton(text='Export to JSON', bgColor='#49302E', fgColor='#FFFFFF', borderColor='#FFFFFF',
                                    onClickHandler=self.export_to_json)
        self.exjson_button.place(x=1090,y=560)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#49302E',
                        fieldlbackground='#BB9C82')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Class Code', 'Subject', 'Units', 'Grade Percentage', 'Grade Point', 'Current GWA')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Class Code', anchor=tk.CENTER, width=15)
        self.tree.column('Subject', anchor=tk.CENTER, width=150)
        self.tree.column('Units', anchor=tk.CENTER, width=10)
        self.tree.column('Grade Percentage', anchor=tk.CENTER, width=145)
        self.tree.column('Grade Point', anchor=tk.CENTER, width=75)
        self.tree.column('Current GWA', anchor=tk.CENTER, width=75)

        self.tree.heading('Class Code', text='Class Code')
        self.tree.heading('Subject', text='Subject')
        self.tree.heading('Units', text='Units')
        self.tree.heading('Grade Percentage', text='Grade Percentage')
        self.tree.heading('Grade Point', text='Grade Point')
        self.tree.heading('Current GWA', text='Current GWA')

        self.tree.place(x=40, y=20, width=1000, height=580)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#49302E'
        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#49302E'
        widget_FgColor='#FFF'
        widget_BgColor='#49302E'
        widget_BorderColor='#FFF'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor, bg_color = widget_BgColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#49302E'
        widget_FgColor='#FFF'
        widget_BgColor='#49302E'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#FFF'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor, bg_color = widget_BgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#49302E'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=260
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        classes = self.db.get_grades()
        self.tree.delete(*self.tree.get_children())
        x=1
        for cl in classes:
            gpoint = self.db.get_gpoint(cl[3])
            gwa = self.db.get_gwa()
            if x==1:
                cl = cl+(gpoint, gwa) 
            else:
                cl = cl+(gpoint, '')          
            print(cl)
            self.tree.insert('', END, values=cl)
            x+=1

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.clc_entry.delete(0, END)
        self.subject_cboxVar.set('English')
        self.units_cboxVar.set('1.0')
        self.gpercent_entry.delete(0, END)

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.clc_entry.insert(0, row[0])
            self.subject_cboxVar.set(row[1])
            self.units_cboxVar.set(row[2])
            self.gpercent_entry.insert(0, row[3])
        else:
            pass

    def add_entry(self):
        clc=self.clc_entry.get()
        gpercent=self.gpercent_entry.get()
        units=self.units_cboxVar.get()
        subject=self.subject_cboxVar.get()

        if not (clc and subject and units and gpercent):
            messagebox.showerror('Error', 'Enter all fields.')
        elif len(clc)!=5 or clc not in [str(i) for i in range(10000, 100000)]:
            messagebox.showerror('Error', 'Enter a proper class code.')
        elif gpercent not in [str(i) for i in range(101)]:
            messagebox.showerror('Error', 'Enter a correct grade.')
        elif self.db.class_exists(clc):
            messagebox.showerror('Error', 'Class already exists')
        else:
            self.db.add_class(clc, subject, units, gpercent)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a class to delete')
        else:
            clc = self.clc_entry.get()
            self.db.delete_class(clc)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        gpercent=self.gpercent_entry.get()
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a class to update')
        elif gpercent not in [str(i) for i in range(101)]:
            messagebox.showerror('Error', 'Enter a correct grade.')
        else:
            clc=self.clc_entry.get()
            subj=self.subject_cboxVar.get()
            units=self.units_cboxVar.get()
            gpercent=self.gpercent_entry.get()
            self.db.update_class(subj, units, gpercent, clc)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')
    
    def import_from_csv(self):
        self.db.import_csv()
        self.add_to_treeview()
        messagebox.showinfo('Success', f'Data imported from {self.db.dbName}.csv')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')
    
    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.json')

    

  
