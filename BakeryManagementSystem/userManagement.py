from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as mb
from .db import c,conn
from PIL import Image, ImageTk
import time
import os
class UserManagement(tk.Toplevel):
    """
    This class is use for add/update/delete users.
    Note: only admin can access this gui.
    """
    def __init__(self,win,*args, **kwargs):
        super().__init__(win,*args, **kwargs)
        self.win=win
        self.title(f"User Management")
        self.geometry("920x600")
        win.center(self)
        self.attributes('-topmost',True)
        
        self.idvar = tk.StringVar()
        self.idvar.trace('w',lambda *args: self.findUser('id',self.idvar))
        self.usernamevar = tk.StringVar()
        self.usernamevar.trace('w',lambda *args: self.findUser('username',self.usernamevar))
        self.emailvar = tk.StringVar()
        self.emailvar.trace('w',lambda *args: self.findUser('email',self.emailvar))
        self.phonevar = tk.StringVar()
        self.phonevar.trace('w',lambda *args: self.findUser('phone',self.phonevar))

        cwd = os.getcwd()

        self.add_user_img = ImageTk.PhotoImage(Image.open(f'{cwd}\\images\\add_user.png'))

        self.delete_img = ImageTk.PhotoImage(Image.open(f'{cwd}\\images\\delete.png'))

        self.edit_img = ImageTk.PhotoImage(Image.open(f'{cwd}\\images\\edit_user.png'))

    def userManagementGUI(self):
        tk.Label(self,text="User Management",font=("Arial",20,'bold')).pack(pady=(5,0))
        
        # Creating frame
        tree_frame = tk.Frame(self)
        top_frame = tk.LabelFrame(self,text="Search User With")
        top_frame.pack(side=tk.TOP,pady=10)
        tree_frame.pack(fill=tk.BOTH,expand=True)

        # we add entries in top frame to search users
        ttk.Label(top_frame,text="User ID:").grid(column=1,row=1,pady=10,padx=10)
        ttk.Entry(top_frame,textvariable=self.idvar).grid(column=2,row=1)

        ttk.Label(top_frame,text="Username:").grid(column=3,row=1,padx=10)
        ttk.Entry(top_frame,textvariable=self.usernamevar).grid(column=4,row=1)
        
        ttk.Label(top_frame,text="Email:").grid(column=5,row=1,padx=10)
        ttk.Entry(top_frame,textvariable=self.emailvar).grid(column=6,row=1)

        ttk.Label(top_frame,text="Phone:").grid(column=7,row=1,padx=10)
        ttk.Entry(top_frame,textvariable=self.phonevar).grid(column=8,row=1)

        ttk.Button(top_frame,text="Add User",command=self.add_update_user_GUI,image=self.add_user_img, compound='left').grid(column=9,row=1,padx=10)
        
        # Creating treeview to show currnet users
        self.tree = ttk.Treeview(tree_frame, selectmode='browse',show='headings')
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vsb.set)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=hsb.set)
        self.tree.pack(fill=tk.BOTH,expand=True)
        
        headings = ["User ID","Joining Date", "Full name", "Username", "Email", "Address", "Phone", "CNIC", "User Status"]

        self.tree["columns"] = headings
        for i in headings:
            self.tree.column(i, width=100, anchor=tk.W)
            self.tree.heading(i, text=i)
        self.tree['show'] = 'headings'
        self.update_tree()
        tree_menu = tk.Menu(self, tearoff = 0) 
        self.bind("<Delete>",lambda *arg: self.delete_user())
        self.bind("<Double-Button-1>",lambda *arg: self.add_update_user_GUI(action="Update"))
        tree_menu.add_command(label ="Edit this User", command=lambda : self.add_update_user_GUI(action="Update"), image=self.edit_img, compound='left')
        tree_menu.add_command(label ="Delete this User", image=self.delete_img, compound='left',command=self.delete_user)
        def show_tree_menu(event): 
            if self.tree.selection():
                try: 
                    tree_menu.tk_popup(event.x_root, event.y_root) 
                finally: 
                    tree_menu.grab_release() 
        self.tree.bind("<Button-3>", show_tree_menu) 
    def delete_user(self):
        if self.tree.selection():
            if mb.askyesno("Delete User","Do you want to delete this user?",parent=self):
                data=self.tree.item(self.tree.selection(),'values')
                c.execute(f"DELETE FROM user WHERE id={data[0]}")
                conn.commit()
                self.update_tree()
    def open_add_user_windows(self):
        self.userManagementGUI()
        self.add_update_user_GUI()
    def add_update_user_GUI(self,action="Add"):
        select=self.tree.selection()
        if action=="Update" and select or action=="Add":
            style = ttk.Style(self)
            style.configure('adduseroptionmenufont.TMenubutton', font=('Arial',13),width=21,background="#fff")
            
            self.add_user_window=tk.Toplevel(self)
            self.attributes('-topmost',False)
            self.add_user_window.attributes("-topmost",True)
            def on_close():
                self.add_user_window.destroy()
                self.attributes('-topmost',True)
            self.add_user_window.protocol("WM_DELETE_WINDOW", on_close )

            self.add_user_window.geometry("750x300")
            self.win.center(self.add_user_window)
            entrywidth=20
            entryfont=('Arial',14)
            padx=(10,5)
            pady=8
            self.userid = tk.StringVar()
            self.fullname = tk.StringVar()
            self.username = tk.StringVar()
            self.password = tk.StringVar()
            self.re_password = tk.StringVar()
            self.email = tk.StringVar()
            self.address = tk.StringVar()
            self.phone = tk.StringVar()
            self.cnic = tk.StringVar()
            self.userstatus = tk.StringVar()
            labelfont = ('Arial',13)
            tk.Label(self.add_user_window,text=f"{action} User",font=("Arial",20,'bold')).pack(pady=(5,0))
            main_frame=ttk.Frame(self.add_user_window)
            main_frame.pack()
            tk.Label(main_frame,text="User ID:", font=labelfont).grid(column=1, row=1, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.userid, state='readonly', font=entryfont,width=entrywidth).grid(column=2, row=1, sticky=tk.W)
            self.win.set_id('user',self.userid)

            tk.Label(main_frame,text="Full name:", font=labelfont).grid(column=3, row=1, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.fullname, font=entryfont,width=entrywidth).grid(column=4, row=1, sticky=tk.W)

            tk.Label(main_frame,text="Username:", font=labelfont).grid(column=1, row=2, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.username, font=entryfont,width=entrywidth).grid(column=2, row=2, sticky=tk.W)

            tk.Label(main_frame,text="Password:", font=labelfont).grid(column=3, row=2, sticky=tk.W, padx=padx, pady=pady)
            passent=ttk.Entry(main_frame,textvariable=self.password, show="●", font=entryfont,width=entrywidth)
            passent.grid(column=4, row=2, sticky=tk.W)

            tk.Label(main_frame,text="Password (Again):", font=labelfont).grid(column=1, row=3, sticky=tk.W, padx=padx, pady=pady)
            passent2=ttk.Entry(main_frame,textvariable=self.re_password, show="●", font=entryfont,width=entrywidth)
            passent2.grid(column=2, row=3, sticky=tk.W)

            passent.bind("<Button-3>",lambda e: self.win.show_hide_password(passent) )
            passent2.bind("<Button-3>",lambda e: self.win.show_hide_password(passent2) )

            tk.Label(main_frame,text="Email:", font=labelfont).grid(column=3, row=3, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.email, font=entryfont,width=entrywidth).grid(column=4, row=3, sticky=tk.W)

            tk.Label(main_frame,text="Address:", font=labelfont).grid(column=1, row=4, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.address, font=entryfont,width=entrywidth).grid(column=2, row=4, sticky=tk.W)

            tk.Label(main_frame,text="CNIC:", font=labelfont).grid(column=3, row=4, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.cnic, font=entryfont,width=entrywidth).grid(column=4, row=4, sticky=tk.W)

            tk.Label(main_frame,text="Phone:", font=labelfont).grid(column=1, row=5, sticky=tk.W, padx=padx, pady=pady)
            ttk.Entry(main_frame,textvariable=self.phone, font=entryfont,width=entrywidth).grid(column=2, row=5, sticky=tk.W)

            tk.Label(main_frame,text="User Status:", font=labelfont).grid(column=3, row=5, sticky=tk.W, padx=padx, pady=pady)
            ttk.OptionMenu(main_frame,self.userstatus,"",'Normal User','admin', style='adduseroptionmenufont.TMenubutton').grid(column=4, row=5, sticky=tk.W)
            self.addbtn=ttk.Button(main_frame,text=action,command=eval(f"self.{action.lower()}_user"))
            self.add_user_window.bind("<Return>",eval(f"self.{action.lower()}_user"))
            self.addbtn.grid(column=2,row=6,sticky=tk.W,padx=padx,pady=pady)
            if action=="Update":
                data = self.tree.item(select,'values')
                c.execute(f"SELECT id,name,username,password,email,address,phone,cnic,status FROM user WHERE id={data[0]}")
                data=c.fetchall()[-1]
                self.userid.set(data[0])
                self.fullname.set(data[1])
                self.username.set(data[2])
                self.password.set(data[3])
                self.re_password.set(data[3])
                self.email.set(data[4])
                self.address.set(data[5])
                self.phone.set(data[6])
                self.cnic.set(data[7])
                self.userstatus.set(data[8])
    def reset_user_form(self):
        self.userid.set("")
        self.fullname.set("")
        self.username.set("")
        self.password.set("")
        self.re_password.set("")
        self.email.set("")
        self.address.set("")
        self.phone.set("")
        self.cnic.set("")
        self.userstatus.set("")
    def validate_input_data(self,update=False):
        username = self.username.get().strip()
        email = self.email.get().strip()
        password = self.password.get().strip()
        fullname = self.fullname.get().strip()
        address = self.address.get().strip()
        cnic = self.cnic.get().strip()
        phone = self.phone.get().strip()
        userstatus = self.userstatus.get().strip()
        def validate_error(val):
            mb.showerror("Validate Error",val,parent=self.add_user_window)

        if not fullname:
            validate_error("Name not found.")
            return False
        elif not username:
            validate_error("Username not found.")
            return False
        elif not self.password.get():
            validate_error("Password not found.")
            return False
        elif password != self.re_password.get():
            validate_error("Passwords are mismatch.")
            return False
        elif len(password)<8:
            validate_error("Password must be more than 8 characters long")
            return False
        elif not email:
            validate_error("Email not found.")
            return False
        elif not address:
            validate_error("Address not found.")
            return False
        elif not cnic:
            validate_error("CNIC not found.")
            return False
        elif not phone:
            validate_error("Phone number not found.")
            return False
        elif not userstatus:
            validate_error("User status not found.")
            return False
        elif not self.win.check_special_character(password):
            validate_error("Password must consist a special character.")
            return False
        c.execute(f"SELECT id FROM user WHERE username='{username}'")
        data = c.fetchall()
        if not update:
            if data:
                validate_error("This username is already taken.\nPlease try another.")
                return False
        else:
            if data:
                if data[-1][-1] != int(self.userid.get()):
                    validate_error("This username is already taken.\nPlease try another.")
                    return False
                    
        if "@" not in email or "." not in email:
            validate_error("Invalid format of email.\nPlease type corrent email address.")
            return False
        return (time.strftime("%d-%m-%Y"),fullname,username,password,email,address,phone,cnic,userstatus)
    def add_user(self,e=None):
        data=self.validate_input_data()
        if data:
            c.execute(f"INSERT INTO user(joiningDate,name,username,password,email,address,phone,cnic,status) VALUES(?,?,?,?,?,?,?,?,?)",data)
            conn.commit()
            mb.showinfo("Success","User successfully added.",parent=self.add_user_window)
            self.reset_user_form()
            self.win.set_id('user',self.userid)
            self.update_tree()
    def update_user(self,e=None):
        data=self.validate_input_data(True)
        if data:
            c.execute(f"""UPDATE user SET name='{data[1]}',
            username='{data[2]}',
            password='{data[3]}',
            email='{data[4]}',
            address='{data[5]}',
            phone='{data[6]}',
            cnic='{data[7]}',
            status='{data[8]}' WHERE id={self.userid.get()}""")
            conn.commit()
            mb.showinfo("Success","User successfully Updated.",parent=self.add_user_window)
            self.add_user_window.destroy()
            self.attributes('-topmost',False)
            self.update_tree()
        
        
    def update_tree(self,data=None):
        if not data:
            c.execute(f"SELECT id,joiningDate,name,username,email,address,phone,cnic,status FROM user")
            data=c.fetchall()
        if data:
            [self.tree.delete(i) for i in self.tree.get_children()]
            for i in data:
                self.tree.insert('','end',values=i)

    def findUser(self,with_,value):
        value=value.get()
        if with_=='id':
            c.execute(f"SELECT id,joiningDate,name,username,email,address,phone,cnic,status FROM user WHERE {with_}='{value}'")
        else:
            c.execute(f"SELECT id,joiningDate,name,username,email,address,phone,cnic,status FROM user WHERE {with_} LIKE '{value}%'")
        data = c.fetchall()
        if data:
            self.update_tree(data)
        elif not data and value:
            [self.tree.delete(i) for i in self.tree.get_children()]
        else:
            self.update_tree()


