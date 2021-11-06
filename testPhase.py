import tkinter as tk
import sqlite3
conn = sqlite3.connect("./database.db")
c = conn.cursor()
import tkinter.messagebox as mb

class NewLoginWindow(tk.Tk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state("zoomed")
        self.usernamevar = tk.StringVar()
        self.passwordvar = tk.StringVar()

    def create_window(self):
        self.title("Bakery Management System")
        # self.geometry("510x200")
        self.state("zoomed")
        self.protocol("WM_DELETE_WINDOW", lambda : self.destroy() )

        tk.Label(self,text=" Bakery Management System ", bd=10, relief=tk.RIDGE, font=("Arial",30,'bold') ,bg='#1B437E').pack(padx=5, pady=(15,5))
        entframe = tk.Frame(self, bd=10, relief=tk.RIDGE)
        entframe.pack(pady=(10,0))
        labfont=("Arial",16,"bold")
        entfont=("Arial",16)
        usernamelab = tk.Label(entframe,text="Username:",font=labfont,fg="blue")
        usernamelab.grid(column=1,row=1,sticky=tk.W,padx=10)
        self.usernameent = tk.Entry(entframe,textvariable=self.usernamevar,border=10,font=entfont,width=25,bg="yellow")
        self.usernameent.grid(column=2,row=1,padx=(20,60))

        passwordlab = tk.Label(entframe,text="Paswword:",font=labfont)
        passwordlab.grid(column=1,row=2,sticky=tk.W,padx=10)
        passwordent = tk.Entry(entframe,border=10,font=entfont,width=25,show="*",textvariable=self.passwordvar)
        passwordent.grid(column=2,row=2,padx=(20,60))

        btnframe = tk.Frame(self, bd=5, relief=tk.RIDGE)
        btnframe.pack()
        btnwidth=17
        btnfont=("Arial",12,"bold")
        tk.Button(btnframe,text="Login", command=self.authenticate, width=btnwidth, font=btnfont, relief=tk.GROOVE).grid(column=1,row=1)
        tk.Button(btnframe,text="Reset", command=self.reset_login_form, width=btnwidth, font=btnfont, relief=tk.GROOVE).grid(column=2,row=1)
        tk.Button(btnframe,text="Exit Window",command=lambda : self.destroy() ,width=btnwidth, font=btnfont, relief=tk.GROOVE).grid(column=3,row=1)
        
        btnframe2 = tk.Frame(self, bd=5, relief=tk.RIDGE)
        btnframe2.pack()
        btnwidth=25
        btnfont=("Arial",12,"bold")
        self.stockbtn = tk.Button(btnframe2,text="Stock", width=btnwidth, font=btnfont, relief=tk.GROOVE,state='disabled')
        self.stockbtn.grid(column=1,row=1)
        self.sellbtn = tk.Button(btnframe2,text="Sell" ,width=btnwidth, font=btnfont, relief=tk.GROOVE,state='disabled')
        self.sellbtn.grid(column=2,row=1)
    def reset_login_form(self):
        self.usernamevar.set("")
        self.passwordvar.set("")
        self.usernameent.focus()
    def check_special_character(self,string):
        characters = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        for i in characters:
            if i in string:
                return True
        return False
    def authenticate(self):
        uname = self.usernamevar.get() 
        passw = self.passwordvar.get()
        if uname and passw:
            if not self.check_special_character(passw):
                mb.showerror("Login Error","Password must consist at least one special character.")
                return
            c.execute(f"SELECT name,status FROM user WHERE username='{uname}' AND password='{passw}'")
            data = c.fetchall()
            if data:
                self.user=data[-1]
                self.usernamevar.set("")
                self.passwordvar.set("")
                self.stockbtn['state']=tk.NORMAL
                self.sellbtn['state']=tk.NORMAL

            else:
                mb.showerror("Authentication error","Username or password is incorrent.")
        else:
            mb.showerror("Login error","Please type Username and Password before login.")
if __name__ == "__main__":
    # win=tk.Tk()
    # win.withdraw()
    w=NewLoginWindow()
    w.create_window()
    w.mainloop()
    # win.mainloop()

