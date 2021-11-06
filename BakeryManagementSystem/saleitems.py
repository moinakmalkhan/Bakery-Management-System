from tkinter import ttk
import tkinter as tk
from .db import c,conn
import tkinter.messagebox as mb
import datetime as dt
import time
class SaleItems(tk.Toplevel):
    def __init__(self,win,*args, **kwargs):
        super().__init__(win,*args, **kwargs)
        self.win=win
        self.attributes('-topmost',True)
        self.title("Sale Items")
        self.geometry("1000x600")
        win.center(self)
        self.searchvalue = tk.StringVar()
        self.searchvalue.trace("w",lambda *args: self.findItem())
        self.itemname = tk.StringVar()
        self.quantity = tk.StringVar()
        self.totalprice = tk.StringVar()
        self.balanceprice = tk.StringVar()
        self.payment = tk.StringVar()
        self.invoice_number = tk.StringVar()
        self.invoice_number.trace('w',lambda *args: self.findInvoice())        
        def find_balance(*args):
            try:
                self.balanceprice.set(float(self.totalprice.get())-float(self.payment.get())) if (self.totalprice.get() and self.payment.get()) else self.balanceprice.set(self.totalprice.get())
            except ValueError:
                pass

        self.payment.trace("w",find_balance)
        self.price = tk.StringVar()
        self.create_bill = tk.BooleanVar()
        self.create_bill.set(True)
        self.searchwith_dict = {"Item ID:":"id","Item Name:":"item_name"}
        self.searchwith = tk.StringVar()
        self.searchwith.trace("w",lambda *args: self.findItem())
    def saleItemGUI(self):
        tk.Label(self,text="Sale Items",font=("Arial",20,"bold")).pack(pady=10)
        top_frame = ttk.Frame(self)
        top_frame.pack()
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM)
        labelfont=("Arial",10)
        entryfont=("Arial",11)
        entwidth=13
        padx=(0,5)
        pady=10
        # creating top frame entrys and labels
        ttk.OptionMenu(top_frame,self.searchwith,"Item ID:","Item ID:","Item Name:").grid(column=1,row=1,padx=padx,pady=pady)
        self.searchwith_ent = ttk.Entry(top_frame,textvariable=self.searchvalue,width=entwidth,font=entryfont)
        self.searchwith_ent.grid(column=2,row=1,padx=padx,pady=pady)
        
        tk.Label(top_frame,text="Quantity:",font=labelfont).grid(column=3,row=1,padx=padx,pady=pady)
        self.qtyent = ttk.Entry(top_frame,textvariable=self.quantity,width=entwidth,font=entryfont)
        self.qtyent.grid(column=4,row=1,padx=padx,pady=pady)
        

        tk.Label(top_frame,text="Item name:",font=labelfont).grid(column=5,row=1,padx=padx,pady=pady)
        itemname_ent = ttk.Entry(top_frame,textvariable=self.itemname,width=entwidth,font=entryfont,state="readonly")
        itemname_ent.grid(column=6,row=1,padx=padx,pady=pady)
        
        tk.Label(top_frame,text="Price:",font=labelfont).grid(column=7,row=1,padx=padx,pady=pady)
        price_ent = ttk.Entry(top_frame,textvariable=self.price,width=entwidth,font=entryfont,state="readonly")
        price_ent.grid(column=8,row=1,padx=padx,pady=pady)

        tk.Label(top_frame,text="Invoice #:",font=labelfont).grid(column=9,row=1,padx=padx,pady=pady)
        invoice_num_ent=ttk.Entry(top_frame,textvariable=self.invoice_number,width=entwidth,font=entryfont)
        invoice_num_ent.grid(column=10,row=1,padx=padx,pady=pady)

        self.submit_btn = ttk.Button(top_frame,text="Add",command=self.add_item)
        # self.bind("<Return>",lambda *args: self.add_item())
        self.submit_btn.grid(column=11,row=1,pady=10)


        # creating bottom frame entrys and labels
        pady=(0,10)
        tk.Label(bottom_frame,text="Total:",font=labelfont).grid(column=1,row=1,padx=padx,pady=pady)
        total_ent = ttk.Entry(bottom_frame,textvariable=self.totalprice,width=entwidth,font=entryfont,state="readonly")
        total_ent.grid(column=2,row=1,padx=padx,pady=pady)
        
        tk.Label(bottom_frame,text="Payment:",font=labelfont).grid(column=3,row=1,padx=padx,pady=pady)
        payment_ent = ttk.Entry(bottom_frame,textvariable=self.payment,width=entwidth,font=entryfont)
        payment_ent.grid(column=4,row=1,padx=padx,pady=pady)

        tk.Label(bottom_frame,text="Balance:",font=labelfont).grid(column=5,row=1,padx=padx,pady=pady)
        ttk.Entry(bottom_frame,textvariable=self.balanceprice,width=entwidth,font=entryfont,state="readonly").grid(column=6,row=1,padx=padx,pady=pady)

        ttk.Checkbutton(bottom_frame,variable=self.create_bill,text="Create Bill").grid(column=8,row=1,padx=padx,pady=pady)
        ttk.Button(bottom_frame,text="Change to Return",command=self.change_to_return).grid(column=10,row=1,padx=padx,pady=pady) 

        ttk.Button(bottom_frame,text="Submit",command=self.submit_data).grid(column=11,row=1,padx=padx,pady=pady) 

        # Creating treeview to show items
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
        
        self.headings=["ID","Item name","Quantity","Price","Total"]

        self.tree["columns"] = self.headings
        for i in self.headings:
            if i in ['ID',"Item name"]:
                self.tree.column(i, width=100, anchor=tk.W)
            else:
                self.tree.column(i, width=100, anchor=tk.E)
            self.tree.heading(i, text=i)
        self.tree['show'] = 'headings'

        
        # Binding events
        def on_control_down(item_num=False):
            item = self.tree.get_children()
            if item and not self.tree.selection():
                self.tree.selection_clear()
                self.tree.focus(item[item_num])
                self.tree.selection_add(item[item_num])
            self.tree.focus_set()
        payment_ent.bind("<Return>",lambda *args: self.submit_data())
        price_ent.bind("<Return>",lambda *args: self.add_item())
        self.qtyent.bind("<Return>",lambda *args: self.add_item())

        self.qtyent.bind("<Alt-Left>",lambda *args: self.searchwith_ent.focus())
        self.qtyent.bind("<Alt-Right>",lambda *args: invoice_num_ent.focus())
        self.qtyent.bind("<Alt-Down>",lambda *args: payment_ent.focus())

        invoice_num_ent.bind("<Alt-Left>",lambda *args: self.qtyent.focus())
        invoice_num_ent.bind("<Alt-Right>",lambda *args: payment_ent.focus())
        invoice_num_ent.bind("<Alt-Down>",lambda *args: payment_ent.focus())

        self.searchwith_ent.bind("<Alt-Left>",lambda *args: payment_ent.focus())
        self.searchwith_ent.bind("<Alt-Right>",lambda *args: self.qtyent.focus())
        self.searchwith_ent.bind("<Alt-Down>",lambda *args: payment_ent.focus())
        payment_ent.bind("<Alt-Left>",lambda *args: self.searchwith_ent.focus())
        payment_ent.bind("<Alt-Right>",lambda *args: invoice_num_ent.focus())
        payment_ent.bind("<Alt-Up>",lambda *args: self.searchwith_ent.focus())
        self.bind("<Control-Down>",lambda *args:on_control_down())
        self.bind("<Control-Up>",lambda *args: on_control_down(-1))
        self.tree.bind("<Delete>",self.delete_item)
        self.tree.bind("<Double-Button-1>",self.update_item)
        self.set_invoice_number()
    def change_to_return(self):
        data = [self.tree.item(i,'values') for i in self.tree.get_children()]
        if data:
            self.delete_tree_data()
            for i in data:
                price = float(i[3])
                qty = -int(i[2])
                total = price*qty
                self.tree.insert('','end',values=[i[0],i[1],qty,price,total])
            self.findTotalPrice()
    def reset_entry(self,all_=False):
        self.itemname.set("")                    
        self.price.set("") 
        self.quantity.set("")
        if all_:
            self.totalprice.set("0")
            self.payment.set("0")
            self.balanceprice.set("0")
    def findItem(self):
        with_ = self.searchwith_dict[self.searchwith.get()]
        value=self.searchvalue.get().strip()
        if value:
            c.execute(f"SELECT item_name,price FROM items WHERE {with_}='{value}'")
            data=c.fetchall()
            if data:
                data=data[-1]
                self.itemname.set(data[0])                    
                self.price.set(data[1])  
            else:
                self.reset_entry() 
        else:
            self.reset_entry() 
    
    def update_item(self,*arg):
        select = self.tree.selection()
        if select:
            data = self.tree.item(select,'values')
            self.tree.delete(select)
            self.searchvalue.set(data[0])
            self.searchwith.set("Item ID:")
            self.quantity.set(data[2])
            self.qtyent.focus()

    def findTotalPrice(self):
        total=0
        for i in self.tree.get_children():
            total+=float(self.tree.item(i,'values')[-1])
        self.totalprice.set(total)
    def delete_item(self,*arg):
        select = self.tree.selection()
        if select:
            self.tree.delete(select)                
    def validate_data(self):
        try:
            update=False
            searchval = self.searchvalue.get().strip()
            searchwith = self.searchwith_dict[self.searchwith.get()]
            if searchwith=="item_name":
                c.execute(f"SELECT id FROM items WHERE {searchwith}='{searchval}'")
                data = c.fetchall()
                if data:
                    searchval = data[-1][0]
                else:
                    return False,False
            quantity = int(self.quantity.get().strip())
            itemname = self.itemname.get().strip()
            price = float(self.price.get().strip())
            if not searchval:
                return False,False
            if not quantity:
                mb.showerror("Error","Quantity not found.\nPlease type quantity.",parent=self)
                return False,False
            if not itemname:
                return False,False
            for i in self.tree.get_children():
                if int(searchval) == int(self.tree.item(i,'values')[0]):
                    update=i
                    break
            return (searchval,itemname,quantity,price,quantity*price),update

        except ValueError:
            return False,False
    def set_invoice_number(self,set_=True):
        c.execute("SELECT MAX(number) FROM invoices")
        data = c.fetchall()
        if data[-1][0]!=None:
            val = int(data[-1][0])+1
            if set_:
                self.invoice_number.set(val)
            return val
        else:
            if set_:
                self.invoice_number.set("1")
            return 1
    def add_item(self):
        data,update=self.validate_data()
        if update and data:
            self.tree.item(update,value=data)
        elif data:
            self.tree.insert('','end',value=data)
        self.findTotalPrice()
        self.searchvalue.set("")
        self.searchwith_ent.focus()
    def delete_tree_data(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
    def findInvoice(self):
        val = self.invoice_number.get().strip()
        if val:
            c.execute(f"SELECT item_id,item_name,quantity,price FROM invoices WHERE number='{val}'")
            data=c.fetchall()
            if data:
                self.delete_tree_data()
                self.reset_entry(all_=True)
                for i in data:
                    self.tree.insert('','end',value=[i[0],i[1],i[2],i[3],float(i[3])*int(i[2])])
                self.findTotalPrice()
            else:
                self.delete_tree_data()
        else:
            self.delete_tree_data()
    def submit_data(self):
        data = [self.tree.item(i,'values') for i in self.tree.get_children()]
        values=[]
        self.set_invoice_number()
        for i in data:
            values.append(i[1:])
            invoice_number = self.invoice_number.get()
            qty = int(i[2])
            status = "add"
            if qty < 0:
                status = "return"
            c.execute(f"SELECT quantity FROM items WHERE id='{i[0]}'")
            old_qty = int(c.fetchall()[-1][-1])
            new_qty = old_qty - qty
            c.execute(f"UPDATE items SET quantity='{new_qty}' WHERE id='{i[0]}'")
            insert_val = (invoice_number,time.strftime("%d-%m-%Y"),i[0],i[1],qty,i[3],status)
            c.execute(f"INSERT INTO invoices VALUES {insert_val}")
        conn.commit()
        if self.create_bill.get():
            totalprice=0
            for i in values:
                totalprice+=float(i[-1])
            values.append(["","","Total :",totalprice])
            data={
                'columns':self.headings[1:],
                'values':values,
                'width':[380,90,120,150],
                'align':['L','R','R','R'],
                "invoice_number":self.invoice_number.get()
            }
            filename="sale.pdf"
            self.win.makePdf(data,"Invoice Heading",filename,print_invoice=True,putDate=False,write_empty_values=False)
            self.win.print_pdf(filename)
            
        self.reset_entry(True)        
        self.delete_tree_data()
        self.set_invoice_number()
        self.searchwith_ent.focus()
