from tkinter import ttk
import tkinter as tk
from .db import c,conn
import tkinter.messagebox as mb
from tkinter.filedialog import asksaveasfilename
from tkcalendar import DateEntry
import datetime as dt
import os
from PIL import Image, ImageTk

class SaleReport(tk.Toplevel):
    def __init__(self,win,*args, **kwargs):
        super().__init__(win,*args, **kwargs)
        self.win=win
        self.attributes('-topmost',True)
        self.title("Sale Report")
        self.geometry("950x680")
        win.center(self)
        self.idvar = tk.StringVar()
        self.itemname = tk.StringVar()
        self.invoicenum = tk.StringVar()

        self.from_date = tk.StringVar()
        self.to_date = tk.StringVar()
        self.search_schedule = tk.StringVar()

        self.search_img = ImageTk.PhotoImage(Image.open('./images/search.png'))

        self.report_img = ImageTk.PhotoImage(Image.open('./images/report.png'))
    def saleReportGUI(self):
        tk.Label(self,text=f"Sale Report",font=("Arial",20,"bold")).pack(pady=10)
        main_frame = ttk.Frame(self)
        main_frame.pack()
        labelfont=("Arial",10)
        entryfont=("Arial",10)
        entry_width = 15

        tk.Label(main_frame,text="Item ID:",font=labelfont).grid(column=1,row=1,sticky=tk.W,pady=10)
        ttk.Entry(main_frame,textvariable=self.idvar,width=entry_width,font=entryfont).grid(column=2,row=1,padx=10,pady=10)

        tk.Label(main_frame,text="Invoice number:",font=labelfont).grid(column=3,row=1,sticky=tk.W,pady=10)
        ttk.Entry(main_frame,textvariable=self.invoicenum,width=entry_width,font=entryfont).grid(column=4,row=1,padx=10,pady=10)

        tk.Label(main_frame,text="Item Name:",font=labelfont).grid(column=5,row=1,sticky=tk.W,pady=10)
        ttk.Entry(main_frame,textvariable=self.itemname,width=entry_width,font=entryfont).grid(column=6,row=1,padx=10,pady=10)
        
        ttk.Button(main_frame,text="Make Report",command=self.make_item_report,image=self.report_img, compound='left').grid(column=8,row=1,padx=10,pady=10)

        pady= (0,10)
        padx = 10
        self.schedule_dict = {
            "All":'all',
            "Today":0,
            "Previous 7 days (One Week)":7,
            "Previous 30 days (One Month)":30,
            "Previous 365 days (One Year)":365
        }    
        schedule = list(self.schedule_dict.keys())
        ttk.OptionMenu(main_frame,self.search_schedule, "All",*schedule).grid(column=1,columnspan=2,row=2,pady=pady)

        ttk.Label(main_frame,text="From date:").grid(column=3,row=2,padx=padx,pady=pady,sticky=tk.W)
        DateEntry(main_frame,textvariable=self.from_date, date_pattern='dd-mm-y',state='readonly').grid(column=4,row=2,pady=pady)

        ttk.Label(main_frame,text="To date:").grid(column=5,row=2,padx=padx,pady=pady,sticky=tk.W)
        DateEntry(main_frame,textvariable=self.to_date, date_pattern='dd-mm-y',state='readonly').grid(column=6,row=2,pady=pady)

        ttk.Button(main_frame,text="Find Items",command=self.search_item_according_to_date,image=self.search_img, compound='left').grid(column=8,row=2,padx=padx,pady=pady)
        
        
        

        # Creating treeview to show all sale items
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
        
        self.headings=["#","Date","Item name","Qty","Price","Dabit","Credit","Balance"]
        alignment = ['w','center','w','e','e','e','e','e']
        self.tree["columns"] = self.headings
        for index,i in enumerate(self.headings):
            self.tree.column(i, width=100, anchor=alignment[index])
            self.tree.heading(i, text=i)
        self.tree['show'] = 'headings'
        self.set_tree_data()
        self.invoicenum.trace('w',lambda *args: self.findItems('number',self.invoicenum))
        self.itemname.trace('w',lambda *args: self.findItems('item_name',self.itemname,search_type="%"))
        self.idvar.trace('w',lambda *args: self.findItems('item_id',self.idvar))

    
        self.search_schedule.trace('w',lambda *args: self.set_from_to_date())
    def set_from_to_date(self):
        num_of_days = self.schedule_dict[self.search_schedule.get()]
        if num_of_days == 'all':
            self.set_tree_data()
            return
        now = dt.date.today()
        now_date = str(now).split("-")
        now_date.reverse()
        self.from_date.set("-".join(now_date))
        to = now - dt.timedelta(days=int(num_of_days))
        to_date = str(to).split("-")
        to_date.reverse()
        self.to_date.set("-".join(to_date))

    def make_item_report(self):
        file_name = asksaveasfilename(parent=self,
                defaultextension='.pdf', filetypes=[("PDF files", '*.pdf')],
                title=f"Save Sale report file")
        if file_name:
            data={
                "columns":self.headings,
                "values":[self.tree.item(i,'values') for i in self.tree.get_children()],
                "align":['L','C','L','R','R','R','R','R'],
                "width":[50,75,200,65,85,85,85,110]
            }
            if self.search_schedule.get().lower() == "all":
                self.win.makePdf(data,"   Sale Report",file_name,pageSize='a4')
            else:
                self.win.makePdf(data,"   Sale Report",file_name,pageSize='a4',from_date=self.from_date.get(),to_date=self.to_date.get())
            os.startfile(file_name)
    def findItems(self,with_,value,search_type="="):
        value = value.get()
        if value:
            if search_type=="%":
                c.execute(f"SELECT number,date_time,item_name,quantity,price FROM invoices WHERE {with_} LIKE '{value}%'")
            else:
                c.execute(f"SELECT number,date_time,item_name,quantity,price FROM invoices WHERE {with_}='{value}'")
            data = c.fetchall()
            self.set_tree_data(data,add_all_data=False)
        else:
            self.set_tree_data()
    
    def search_item_according_to_date(self):
        from_ = self.from_date.get().split("-")
        to = self.to_date.get().split("-")
        start = dt.date(int(from_[2]),int(from_[1]),int(from_[0]))
        end = dt.date(int(to[2]),int(to[1]),int(to[0]))
        if start < end:
            return mb.showerror("Error","'From date' must be grater than or equal to 'to date'.",parent=self)
        [self.tree.delete(i) for i in self.tree.get_children()]
        balance=0
        while start >= end:
            date = str(start).split('-')
            # change yyyy-mm-dd to dd-mm-yyyy
            date.reverse()
            date="-".join(date)
            c.execute(f"SELECT number,date_time,item_name,quantity,price FROM invoices WHERE date_time='{date}' ORDER BY date_time")
            data = c.fetchall()
            if data:
                for i in data:
                    qty = int(i[3])
                    price = float(i[4])
                    if qty < 0:
                        debit = 0
                        credit = price*abs(qty)
                    else:
                        debit = price*qty
                        credit = 0
                    balance += debit-credit
                    self.tree.insert('','end',values=(i[0],i[1],i[2],qty,price,debit,credit,balance))            

            start = start - dt.timedelta(days=1)

    def set_tree_data(self,data=None,add_all_data=True):
        [self.tree.delete(i) for i in self.tree.get_children()]
        if not data and add_all_data:
            c.execute(f"SELECT number,date_time,item_name,quantity,price FROM invoices")
            data = c.fetchall()
        elif not data:
            return
        balance=0
        for i in data:
            qty = int(i[3])
            price = float(i[4])
            if qty < 0:
                debit = 0
                credit = price*abs(qty)
            else:
                debit = price*qty
                credit = 0
            balance += debit-credit
            self.tree.insert('','end',values=(i[0],i[1],i[2],qty,price,debit,credit,balance))            

