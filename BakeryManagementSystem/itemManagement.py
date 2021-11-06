
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as mb
from .db import c,conn
from PIL import Image, ImageTk
import time
from tkinter.filedialog import asksaveasfilename
from tkcalendar import DateEntry
import datetime as dt
import os

class ItemManagement(tk.Toplevel):
    """
    This class is use for add/update/delete/search Items.
    Note: only admin can access this gui.
    """
    def __init__(self,win,*args, **kwargs):
        super().__init__(win,*args, **kwargs)
        self.win=win
        self.title(f"Items Management")
        self.geometry("950x680")
        win.center(self)
        self.attributes('-topmost',True)
        self.idvar = tk.StringVar()
        self.idvar.trace('w',lambda *args: self.findItem('a.id',self.idvar))
        self.itemnamevar = tk.StringVar()
        self.itemnamevar.trace('w',lambda *args: self.findItem('a.item_name',self.itemnamevar))
        self.categoryvar = tk.StringVar()
        self.categoryvar.trace('w',lambda *args: self.findItem('b.name',self.categoryvar))
        self.pricevar = tk.StringVar()
        self.pricevar.trace('w',lambda *args: self.findItem('a.price',self.pricevar))

        self.from_date = tk.StringVar()
        self.to_date = tk.StringVar()
        self.search_schedule = tk.StringVar()
    
        cwd = os.getcwd()

        self.add_item_img = ImageTk.PhotoImage(Image.open(f'{cwd}\\images\\add_item.png'))

        self.delete_img = ImageTk.PhotoImage(Image.open(f'{cwd}\\images\\delete.png'))

        self.edit_img = ImageTk.PhotoImage(Image.open(f'{cwd}\\images\\edit_item.png'))

        self.search_img = ImageTk.PhotoImage(Image.open(f'{cwd}\\images\\search.png'))

        self.report_img = ImageTk.PhotoImage(Image.open(f'{cwd}\\images\\report.png'))

    def itemManagementGUI(self):
        tk.Label(self,text="Item Management",font=("Arial",20,'bold')).pack(pady=(5,0))
         # Creating frame
        tree_frame = tk.Frame(self)
        top_frame = tk.LabelFrame(self,text="Search Item With")
        top_frame.pack(side=tk.TOP,pady=10)
        tree_frame.pack(fill=tk.BOTH,expand=True)
        padx=10
        pady=(0,5)
        # we add entries in top frame to search Items
        ttk.Label(top_frame,text="Item ID:").grid(column=1,row=1,padx=padx, pady=pady,sticky=tk.W)
        ttk.Entry(top_frame,textvariable=self.idvar).grid(column=2,row=1,pady=pady)

        ttk.Label(top_frame,text="Item name:").grid(column=3,row=1,padx=padx,pady=pady,sticky=tk.W)
        ttk.Entry(top_frame,textvariable=self.itemnamevar).grid(column=4,row=1,pady=pady)
        
        ttk.Label(top_frame,text="Category:").grid(column=5,row=1,padx=padx,pady=pady,sticky=tk.W)
        ttk.Entry(top_frame,textvariable=self.categoryvar).grid(column=6,row=1,pady=pady)

        ttk.Label(top_frame,text="Price:").grid(column=7,row=1,padx=padx,pady=pady,sticky=tk.W)
        ttk.Entry(top_frame,textvariable=self.pricevar).grid(column=8,row=1,pady=pady)

        ttk.Button(top_frame,text="Add items",command=self.add_update_item_GUI,image=self.add_item_img, compound='left').grid(column=9,row=1,padx=padx,pady=pady)

        self.schedule_dict = {
            "All":'all',
            "Today":0,
            "Previous 7 days (One Week)":7,
            "Previous 30 days (One Month)":30,
            "Previous 365 days (One Year)":365
        }    
        schedule = list(self.schedule_dict.keys())
        ttk.OptionMenu(top_frame,self.search_schedule, "All",*schedule).grid(column=1,columnspan=2,row=2,pady=pady)

        ttk.Label(top_frame,text="From date:").grid(column=3,row=2,padx=padx,pady=pady,sticky=tk.W)
        DateEntry(top_frame,textvariable=self.from_date, date_pattern='dd-mm-y',state='readonly').grid(column=4,row=2,pady=pady)

        ttk.Label(top_frame,text="To date:").grid(column=5,row=2,padx=padx,pady=pady,sticky=tk.W)
        DateEntry(top_frame,textvariable=self.to_date, date_pattern='dd-mm-y',state='readonly').grid(column=6,row=2,pady=pady)

        ttk.Button(top_frame,text="Find Items",command=self.search_item_according_to_date,image=self.search_img, compound='left').grid(column=8,row=2,padx=padx,pady=pady)
        
        ttk.Button(top_frame,text="Make Report",command=self.make_item_report,image=self.report_img, compound='left').grid(column=9,row=2,padx=padx,pady=pady)
        
        

        # Creating treeview to show currnet items
        self.tree = ttk.Treeview(tree_frame, selectmode='browse',show='headings')
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vsb.set)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=hsb.set)
        self.tree.pack(fill=tk.BOTH,expand=True)
        
        self.headings = ['Item ID', 'Date', 'Item name', 'Category', 'Weight', 'Quantity', 'Price', 'Expire date']

        self.tree["columns"] = self.headings
        for i in self.headings:
            self.tree.column(i, width=100, anchor=tk.W)
            self.tree.heading(i, text=i)
        self.tree['show'] = 'headings'
        self.update_tree()
        tree_menu = tk.Menu(self, tearoff = 0) 
        self.tree.bind("<Delete>",lambda *arg: self.delete_item())
        self.tree.bind("<Double-Button-1>",lambda *arg: self.add_update_item_GUI(action="Update"))
        tree_menu.add_command(label ="Edit this item", command=lambda : self.add_update_item_GUI(action="Update"), image=self.edit_img, compound='left')
        tree_menu.add_command(label ="Delete this item", image=self.delete_img, compound='left',command=self.delete_item)
        def show_tree_menu(event): 
            if self.tree.selection():
                try: 
                    tree_menu.tk_popup(event.x_root, event.y_root) 
                finally: 
                    tree_menu.grab_release() 
        self.tree.bind("<Button-3>", show_tree_menu) 
        self.bind("<Control-r>", lambda *args: self.make_item_report()) 
        self.bind("<Control-R>", lambda *args: self.make_item_report()) 
        self.search_schedule.trace('w',lambda *args: self.set_from_to_date())
    def make_item_report(self):
        file_name = asksaveasfilename(parent=self,
                defaultextension='.pdf', filetypes=[("PDF files", '*.pdf')],
                title=f"Save items report file")
        if file_name:
            data={
                "columns":self.headings,
                "values":[self.tree.item(i,'values') for i in self.tree.get_children()],
                "align":['L','C','L','L','R','R','R','C'],
                "width":[50,75,190,150,70,60,100,75]
            }
            if self.search_schedule.get().lower() == "all":
                self.win.makePdf(data,"   Items Report",file_name,pageSize='a4')
            else:
                self.win.makePdf(data,"   Items Report",file_name,pageSize='a4',from_date=self.from_date.get(),to_date=self.to_date.get())
            os.startfile(file_name)
    def search_item_according_to_date(self):
        from_ = self.from_date.get().split("-")
        to = self.to_date.get().split("-")
        start = dt.date(int(from_[2]),int(from_[1]),int(from_[0]))
        end = dt.date(int(to[2]),int(to[1]),int(to[0]))
        if start < end:
            return mb.showerror("Error","'From date' must be grater than or equal to 'to date'.",parent=self)
        [self.tree.delete(i) for i in self.tree.get_children()]
        while start >= end:
            date = str(start).split('-')
            # change yyyy-mm-dd to dd-mm-yyyy
            date.reverse()
            date="-".join(date)
            c.execute(f"SELECT a.id,a.date_time,a.item_name,b.name,a.weight,a.quantity,a.price,a.expire_date FROM items a INNER JOIN category b ON a.category_id=b.id WHERE a.date_time='{date}' ORDER BY a.date_time")
            data = c.fetchall()
            if data:
                for i in data:
                    self.tree.insert("",'end',values=i)
            start = start - dt.timedelta(days=1)

    def set_from_to_date(self):
        num_of_days = self.schedule_dict[self.search_schedule.get()]
        if num_of_days == 'all':
            self.update_tree()
            return
        now = dt.date.today()
        now_date = str(now).split("-")
        now_date.reverse()
        self.from_date.set("-".join(now_date))
        to = now - dt.timedelta(days=int(num_of_days))
        to_date = str(to).split("-")
        to_date.reverse()
        self.to_date.set("-".join(to_date))
    def findItem(self,with_,value):
        value=value.get()
        if with_=='a.id':
            c.execute(f"SELECT a.id,a.date_time,a.item_name,b.name,a.weight,a.quantity,a.price,a.expire_date FROM items a INNER JOIN category b ON a.category_id=b.id WHERE {with_}='{value}' ORDER BY {with_}")
        else:
            c.execute(f"SELECT a.id,a.date_time,a.item_name,b.name,a.weight,a.quantity,a.price,a.expire_date FROM items a INNER JOIN category b ON a.category_id=b.id WHERE {with_} LIKE '{value}%' ORDER BY {with_}")
        data = c.fetchall()
        if data:
            self.update_tree(data)
        elif not data and value:
            [self.tree.delete(i) for i in self.tree.get_children()]
        else:
            self.update_tree()
        
    def delete_item(self):
        if self.tree.selection():
            if mb.askyesno("Delete Item","Do you want to delete this Item?",parent=self):
                data=self.tree.item(self.tree.selection(),'values')
                c.execute(f"DELETE FROM items WHERE id='{data[0]}'")
                conn.commit()
                self.update_tree()
    def open_add_item_windows(self):
        self.itemManagementGUI()
        self.add_update_item_GUI()
    def add_update_item_GUI(self,action="Add"):
        select=self.tree.selection()
        if action=="Update" and select or action=="Add":
            style = ttk.Style(self)
            style.configure('additemoptionmenufont.TMenubutton', font=('Arial',13),width=21,background="#fff")
            
            self.add_item_window=tk.Toplevel(self)
            self.attributes('-topmost',False)
            self.add_item_window.attributes("-topmost",True)
            def on_close():
                self.add_item_window.destroy()
                self.attributes('-topmost',True)
            self.add_item_window.protocol("WM_DELETE_WINDOW", on_close )

            self.add_item_window.geometry("750x300")
            self.win.center(self.add_item_window)
            entrywidth=20
            entryfont=('Arial',14)
            labelfont = ('Arial',13)
            padx=(10,5)
            pady=8
            self.itemid = tk.StringVar()
            self.itemname = tk.StringVar()
            self.quantity = tk.StringVar()
            self.price = tk.StringVar()
            self.expire_date = tk.StringVar()
            self.weight = tk.StringVar()
            self.category = tk.StringVar()
            
            tk.Label(self.add_item_window,text=f"{action} Item",font=("Arial",20,'bold')).pack(pady=(5,0))
            main_frame=ttk.Frame(self.add_item_window)
            main_frame.pack()
            tk.Label(main_frame,text="Item ID:", font=labelfont).grid(column=1, row=1, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.itemid, font=entryfont,width=entrywidth).grid(column=2, row=1, sticky=tk.W)
            self.win.set_id('items',self.itemid)

            tk.Label(main_frame,text="Item name:", font=labelfont).grid(column=3, row=1, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.itemname, font=entryfont,width=entrywidth).grid(column=4, row=1, sticky=tk.W)

            tk.Label(main_frame,text="Weight:", font=labelfont).grid(column=1, row=2, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.weight, font=entryfont,width=entrywidth).grid(column=2, row=2, sticky=tk.W)

            tk.Label(main_frame,text="Quantity:", font=labelfont).grid(column=3, row=2, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.quantity, font=entryfont,width=entrywidth).grid(column=4, row=2, sticky=tk.W)

            tk.Label(main_frame,text="Category:", font=labelfont).grid(column=1, row=3, sticky=tk.W, padx=padx, pady=pady)
            category = []
            c.execute("SELECT name FROM category")
            for i in c.fetchall():
                category.append(i[0])
            ttk.OptionMenu(main_frame,self.category,"", *category, style='additemoptionmenufont.TMenubutton').grid(column=2, row=3, sticky=tk.W)

            tk.Label(main_frame,text="Price:", font=labelfont).grid(column=3, row=3, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.price, font=entryfont,width=entrywidth).grid(column=4, row=3, sticky=tk.W)

            tk.Label(main_frame,text="Expire date:", font=labelfont).grid(column=1, row=4, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.expire_date, font=entryfont,width=entrywidth).grid(column=2, row=4, sticky=tk.W)



            if action.lower()=="add":
                self.addbtn=ttk.Button(main_frame,text=action,command=self.add_update_item)
                self.add_item_window.bind("<Return>", lambda *args:self.add_update_item)
            else:
                self.addbtn=ttk.Button(main_frame,text=action,command=lambda: self.add_update_item(True))
                self.add_item_window.bind("<Return>",lambda *args: self.add_update_item(True))
                data = self.tree.item(select,'values')
                c.execute(f"SELECT a.id,a.item_name,b.name,a.weight,a.quantity,a.price,a.expire_date FROM items a INNER JOIN category b ON a.category_id=b.id WHERE a.id='{data[0]}'")
                self.find_items_to_add(data[0])
            self.addbtn.grid(column=2,row=6,sticky=tk.W,padx=padx,pady=pady)
            self.itemid.trace('w',lambda *args: self.find_items_to_add())
    def find_items_to_add(self,itemid=None):
        if itemid:
            query=f"SELECT a.id,a.item_name,b.name,a.weight,a.quantity,a.price,a.expire_date FROM items a INNER JOIN category b ON a.category_id=b.id WHERE a.id='{itemid}'"
        else:
            query=f"SELECT a.id,a.item_name,b.name,a.weight,a.quantity,a.price,a.expire_date FROM items a INNER JOIN category b ON a.category_id=b.id WHERE a.id='{self.itemid.get()}'"
        c.execute(query)
        data=c.fetchall()
        if data:
            self.addbtn.configure(text="Update",command=lambda: self.add_update_item(True))
            self.add_item_window.bind("<Return>",lambda *args: self.add_update_item(True))
            data=data[-1]
            self.itemid.set(data[0])
            self.itemname.set(data[1])
            self.category.set(data[2])
            self.weight.set(data[3])
            self.quantity.set(data[4])
            self.price.set(data[5])
            self.expire_date.set(data[6])
        else:
            self.addbtn=ttk.Button(text="Add",command=self.add_update_item)
            self.add_item_window.bind("<Return>", lambda *args:self.add_update_item)
            self.reset_item_form()
    def reset_item_form(self):
        self.itemname.set("")
        self.category.set("")
        self.weight.set("")
        self.quantity.set("")
        self.price.set("")
        self.expire_date.set("")
    def validate_input_data(self,update=False):
        itemname = self.itemname.get().strip()
        category = self.category.get().strip()
        weight = self.weight.get().strip()
        quantity = int(self.quantity.get().strip())
        price = self.price.get().strip()
        expire_date = self.expire_date.get().strip()
        def validate_error(val):
            mb.showerror("Validate Error",val,parent=self.add_item_window)
        if not itemname:
            validate_error("Item name not found.")
            return False,False
        elif not category:
            validate_error("Category not found.")
            return False,False
        elif not weight:
            validate_error("Weight not found.")
            return False,False
        elif not quantity:
            validate_error("Quantity not found.")
            return False,False
        elif not price:
            validate_error("Price not found.")
            return False,False
        elif not expire_date:
            validate_error("Expire date not found.")
            return False,False
        c.execute(f"SELECT quantity FROM items WHERE id='{self.itemid.get().strip()}'")
        data = c.fetchall()
        if data and not update:
            quantity += int(data[-1][-1])
            update = True
        if not update:
            c.execute(f"SELECT id,quantity FROM items WHERE item_name='{itemname}'")
            data = c.fetchall()
            if data:
                if mb.askyesno("Already exists",f"This item is already exists on id number {data[-1][0]}.\nDo you want to update information?",parent=self.add_item_window):
                    quantity += int(data[-1][-1])
                    update = True
                    self.itemid.set(data[-1][0])
                else:
                    return False,False
        c.execute(f"SELECT id FROM category WHERE name='{category}'")
        data=c.fetchall()
        if data:
            data=data[-1][-1]
        else:
            data="Deleted"
        return (time.strftime("%d-%m-%Y"),itemname,data,weight,str(quantity),price,expire_date),update
    def add_update_item(self,update=None):
        data,update=self.validate_input_data(update)
        if data and not update:
            query=f"INSERT INTO items(date_time,item_name,category_id,weight,quantity,price,expire_date) VALUES(?,?,?,?,?,?,?)"
            print(query,data)
            c.execute(query)
            conn.commit()
            mb.showinfo("Success","item successfully added.",parent=self.add_item_window)
            self.reset_item_form()
            self.win.set_id('items',self.itemid)
            self.update_tree()
        elif data and update:
            query=f"""UPDATE items SET item_name='{data[1]}',
            category_id='{data[2]}',
            weight='{data[3]}',
            quantity='{data[4]}',
            price='{data[5]}',
            expire_date='{data[6]}'
            WHERE id={self.itemid.get()}"""
            c.execute(query)
            conn.commit()
            mb.showinfo("Success","item successfully Updated.",parent=self.add_item_window)
            self.add_item_window.destroy()
            self.attributes('-topmost',False)
            self.update_tree()
        
        
    def update_tree(self,data=None):
        if not data:
            c.execute(f"SELECT a.id,a.date_time,a.item_name,b.name,a.weight,a.quantity,a.price,a.expire_date FROM items a INNER JOIN category b ON a.category_id=b.id ")
            data=c.fetchall()
        if data:
            [self.tree.delete(i) for i in self.tree.get_children()]
            for i in data:
                self.tree.insert('','end',values=i)


