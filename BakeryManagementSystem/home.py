from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as mb
from .db import c,conn
from .userManagement import UserManagement
from .addCategory import AddCategory
from .itemManagement import ItemManagement
from .saleitems import SaleItems
from .saleReport import SaleReport
# from .advance_itemManagement import Advance_ItemManagement
# from .advance_userManagement import Advance_UserManagement
class HomeWindow:
    """
    This is main window of Bakery Management system
    """
    def __init__(self,win,user,*args, **kwargs):
        self.user=user
        self.win=win
        win.title(f"Welcome {user[0].title()}")
        win.userstatus = user[1]
        win.geometry("800x600")
        win.state("zoomed")   
        win.center(win) 
        self.HomeGUI()
    def HomeGUI(self):
        tk.Label(self.win,text="Bakery Management System",font=("Arial",20,'bold')).pack(pady=10)
        
        # Creating frame
        top_frame = tk.Frame(self.win)
        top_frame.pack(side=tk.TOP)
        middle_frame = tk.Frame(self.win)
        middle_frame.pack()
        bottom_frame = tk.Frame(self.win)
        bottom_frame.pack(side=tk.BOTTOM)
        
        # top_btn_relief = tk.FLAT
        top_btn_relief = None
        top_btn_border = 10
        top_btn_padx = 10
        top_btn_pady = 10
        top_btn_height = 3
        top_btn_width = 20
        top_btn_font = ("Arial",14)

        middle_btn_height = 6
        middle_btn_padx = 10
        middle_btn_pady = 10
        middle_btn_width = 30
        middle_btn_relief = None
        middle_btn_border = 10
        middle_btn_font = ("Arial",15)
                    
        
        
        adduserbtn = tk.Button(top_frame, text="Add User",command=self.addUser,width=top_btn_width,height=top_btn_height,font=top_btn_font,relief=top_btn_relief,border=top_btn_border)
        adduserbtn.grid(column=1,row=1,padx=top_btn_padx,pady=top_btn_pady)

        manageuserbtn = tk.Button(top_frame, text="Edit/Remove/Search User",command=self.userManagement,width=top_btn_width,height=top_btn_height,font=top_btn_font,relief=top_btn_relief,border=top_btn_border)
        manageuserbtn.grid(column=2,row=1,padx=top_btn_padx,pady=top_btn_pady)

        tk.Button(top_frame, text="Sale Report",command=self.saleReport,width=top_btn_width,height=top_btn_height,font=top_btn_font,relief=top_btn_relief,border=top_btn_border).grid(column=3,row=1,padx=top_btn_padx,pady=top_btn_pady)

        tk.Button(top_frame, text="Sign out",command=self.signOut,width=top_btn_width,height=top_btn_height,font=top_btn_font,relief=top_btn_relief,border=top_btn_border).grid(column=4,row=1,padx=top_btn_padx,pady=top_btn_pady)

        if self.win.get_user()[1]!='admin':
            adduserbtn['state']='disabled'
            manageuserbtn['state']='disabled'

        tk.Button(middle_frame, text="Add/Remove/Edit Category",command=self.addCategory,width=middle_btn_width,height=middle_btn_height,font=middle_btn_font,relief=middle_btn_relief,border=middle_btn_border).grid(column=1,row=1,padx=middle_btn_padx,pady=middle_btn_pady)

        tk.Button(middle_frame, text="Add Item",command=self.addItem,width=middle_btn_width,height=middle_btn_height,font=middle_btn_font,relief=middle_btn_relief,border=middle_btn_border).grid(column=2,row=1,padx=middle_btn_padx,pady=middle_btn_pady)

        tk.Button(middle_frame, text="Sale Items",command=self.saleItem,width=middle_btn_width,height=middle_btn_height,font=middle_btn_font,relief=middle_btn_relief,border=middle_btn_border).grid(column=1,row=2,padx=middle_btn_padx,pady=middle_btn_pady)

        tk.Button(middle_frame, text="Edit/Remove/Search Items",command=self.itemManagement,width=middle_btn_width,height=middle_btn_height,font=middle_btn_font,relief=middle_btn_relief,border=middle_btn_border).grid(column=2,row=2,padx=middle_btn_padx,pady=middle_btn_pady)


        tk.Label(bottom_frame,text="Copyright © 2021 Masab Ali & Usman").pack()

    def signOut(self):
        for widget in self.win.winfo_children():
            widget.destroy()

        self.win.withdraw()
        self.win.loginGUI()
    def saleReport(self):
        SaleReport(self.win).saleReportGUI()
    def saleItem(self):
        SaleItems(self.win).saleItemGUI()
    def addItem(self):
        ItemManagement(self.win).open_add_item_windows()
    def itemManagement(self):
        ItemManagement(self.win).itemManagementGUI()
    def addUser(self):
        UserManagement(self.win).open_add_user_windows()
    def userManagement(self):
        UserManagement(self.win).userManagementGUI()
    def addCategory(self):
        AddCategory(self.win).addCategoryGUI()
