from tkinter import ttk
import tkinter as tk
from .db import c,conn
import tkinter.messagebox as mb

class AddCategory(tk.Toplevel):
    def __init__(self,win,*args, **kwargs):
        super().__init__(win,*args, **kwargs)
        self.win=win
        self.category_name = tk.StringVar()
        self.attributes('-topmost',True)
        self.title("Add Category")
        self.geometry("500x400")
        win.center(self)
        self.idvar = tk.StringVar()
        self.namevar = tk.StringVar()
    def addCategoryGUI(self):
        tk.Label(self,text=f"Add Category",font=("Arial",20,"bold")).pack(pady=10)
        main_frame = ttk.Frame(self)
        main_frame.pack()
        labelfont=("Arial",13)
        entryfont=("Arial",14)
        tk.Label(main_frame,text="ID:",font=labelfont).grid(column=1,row=1,sticky=tk.W,pady=10)
        ttk.Entry(main_frame,textvariable=self.idvar,state='readonly',width=30,font=entryfont).grid(column=2,row=1,padx=10,pady=10)
        self.win.set_id('category',self.idvar)
        tk.Label(main_frame,text="Name:",font=labelfont).grid(column=1,row=2,sticky=tk.W,pady=10)
        ttk.Entry(main_frame,textvariable=self.namevar,width=30,font=entryfont).grid(column=2,row=2,padx=10,pady=10)

        self.submit_btn = ttk.Button(main_frame,text="Add",command=self.add_category)
        self.bind("<Return>",lambda *args: self.add_category())
        self.submit_btn.grid(column=2,row=3,pady=10)

        # Creating treeview to show categories
        tree_frame = ttk.Frame(self)
        tree_frame.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        self.tree = ttk.Treeview(tree_frame, selectmode='browse',show='headings')
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vsb.set)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=hsb.set)
        self.tree.pack(fill=tk.BOTH,expand=True)
        
        headings=["ID","Category name"]

        self.tree["columns"] = headings
        for i in headings:
            self.tree.column(i, width=100, anchor=tk.W)
            self.tree.heading(i, text=i)
        self.tree['show'] = 'headings'
        self.update_tree()
        self.tree.bind("<Delete>",self.delete_category)
        self.tree.bind("<Double-Button-1>",self.update_category)
    def get_selected_data(self):
        select = self.tree.selection()
        if select:
            return self.tree.item(select,'values')
        return False
    def update_category(self,*arg):
        data = self.get_selected_data()
        if data:
            self.idvar.set(data[0])
            self.namevar.set(data[1])
            self.submit_btn.configure(command=lambda :self.add_category(True) ,text="Update")
            self.bind("<Return>",lambda *args: self.add_category(True))
    def delete_category(self,*arg):
        data = self.get_selected_data()
        if data:
            if mb.askyesno("Delete Category","Do you want to delete this category?",parent=self):
                c.execute(f"DELETE FROM category WHERE id={data[0]}")
                conn.commit()
                self.update_tree()
    def validate_data(self,update=False):
        name = self.namevar.get().strip()
        if name:
            c.execute(f"SELECT id FROM category WHERE name='{name}'")
            data=c.fetchall()
            if update and data:
                # Here lets check that user send request to update data without any changes in category name
                # if user submit data without any changes then we have to do nothing with database. so we simply reset name field to add new category 
                if int(self.idvar.get())==int(data[-1][-1]):
                    self.namevar.set("")
                    self.win.set_id('category',self.idvar)
                    self.submit_btn.configure(command=lambda :self.add_category() ,text="Add")
                    self.bind("<Return>",lambda *args: self.add_category())
                else:
                    mb.showerror("Validate Error","This category is already exists.",parent=self)
                return False
            elif data:
                mb.showerror("Validate Error","This category is already exists.",parent=self)
                return False
        else:
            mb.showerror("Validate Error","Category name is not found.",parent=self)
            return False
        return name
    def add_category(self,update=False):
        name=self.validate_data(update)
        if not name:
            return
        if update:
            c.execute(f"UPDATE category SET name='{name}' WHERE id={self.idvar.get()}")
            self.submit_btn.configure(command=lambda :self.add_category() ,text="Add")
            self.bind("<Return>",lambda *args: self.add_category())
        else:
            c.execute(f"INSERT INTO category(name) VALUES('{name}')")
        conn.commit()
        self.win.set_id('category',self.idvar)
        self.update_tree()
        self.namevar.set("")
    def update_tree(self):
        c.execute("SELECT * FROM category")
        [self.tree.delete(i) for i in self.tree.get_children()]
        for i in c.fetchall():
            self.tree.insert('','end',values=i)
