from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as mb
from .db import c,conn
from .home import HomeWindow
import time
# import PDFNetPython3 as pdfnet
from fpdf import FPDF
from threading import Thread
import datetime as dt
class Login(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)
        self.withdraw()
        
        self.usernamevar = tk.StringVar()
        self.passwordvar = tk.StringVar()

    def loginGUI(self):
        self.login_window = tk.Toplevel(self)
        self.login_window.title("Login")
        self.login_window.geometry("510x200")
        self.center(self.login_window)
        #win.overrideredirect(True)
        # win.attributes('-disabled', True)
        self.login_window.protocol("WM_DELETE_WINDOW", lambda : self.destroy() )
        tk.Label(self.login_window,text="Bakery Management System",font=("Arial",20,'bold')).pack(pady=5)
        frame = tk.Frame(self.login_window)
        labelfont = ("Arial",15)
        entryfont = ("Arial",16)
        buttonfont = ("Arial",14)
        tk.Label(frame,text="Username: ",font=labelfont).grid(column=1,row=1,sticky=tk.W)
        ent = ttk.Entry(frame,textvariable=self.usernamevar,font=entryfont)
        ent.grid(column=2,row=1,pady=10)
        ent.focus()
        tk.Label(frame,text="Password: ",font=labelfont).grid(column=1,row=2,sticky=tk.W)
        passwordent=ttk.Entry(frame,textvariable=self.passwordvar,show="●",font=entryfont)
        passwordent.grid(column=2,row=2)
        passwordent.bind("<Button-3>",lambda e: self.show_hide_password(passwordent))
        self.login_window.bind("<Return>",lambda e: self.authenticate())
        tk.Button(frame,text="   Login   ",font=buttonfont,command=self.authenticate).grid(column=2,row=3,sticky=tk.W,pady=20)
        tk.Button(frame,text="   Close   ",font=buttonfont,command=lambda : self.destroy()).grid(column=2,row=3,sticky=tk.E,pady=20)
        frame.pack(fill=tk.BOTH,expand=True,padx=50)
    def get_user(self):
        return self.user
        
    def set_id(self,tablename,variable=None,add=1):
        c.execute(f"SELECT MAX(id) FROM {tablename}")
        data = c.fetchall()
        if data and data[-1][-1]!=None:
            val=int(data[-1][-1])+add
            if variable:
                variable.set(val)
            return val
        else:
            variable.set("1")
            return 1
    def show_hide_password(self,entry):
        if entry['show']=="●":
            entry['show']=""
        else:
            entry['show']="●"
    def authenticate(self,username=None,password=None):
        if username and password:
            c.execute(f"SELECT name,status FROM user WHERE username=? AND password=?",(username,password))
            data = c.fetchall()
            if data:
                return data[-1]
            else:
                return None
        else:
            c.execute(f"SELECT name,status FROM user WHERE username=? AND password=?",(self.usernamevar.get(),self.passwordvar.get()))
            data = c.fetchall()
            if data:
                self.user=data[-1]
                HomeWindow(self,user=data[-1])
                self.login_window.destroy()
                self.usernamevar.set("")
                self.passwordvar.set("")
                self.deiconify()

            else:
                mb.showerror("Authentication error","Username or password is incorrent.")
    
    def print_pdf(self,filename):
        pass
        # try:
        #     pdfnet.PDFNet.Initialize()
                
        #     doc = pdfnet.PDFDoc(filename)
        #     doc.InitSecurityHandler()
            
        #     printerMode = pdfnet.PrinterMode()
        #     printerMode.SetCollation(True)
        #     printerMode.SetCopyCount(1)
        #     printerMode.SetDPI(100)
        #     printerMode.SetDuplexing(pdfnet.PrinterMode.e_Duplex_Auto)
            
        #     printerMode.SetOutputColor(pdfnet.PrinterMode.e_OutputColor_Grayscale)
        #     printerMode.SetOutputQuality(pdfnet.PrinterMode.e_OutputQuality_Medium)
        #     pdfnet.Print.StartPrintJob(doc, "", doc.GetFileName(), "", None, printerMode, None)

        # except:
        #     pass
    def check_special_character(self,string):
        characters = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        for i in characters:
            if i in string:
                return True
        return False
    def makePdf(self,data,heading,filename,putDate=True,pageSize='a4',print_invoice=False,write_empty_values=True,from_date=None,to_date=None):
        """
        this function is use for create pdf reports. it takes data of table and heading of report and filename as required arguments
        and putDate, print_invoice,from_date,to_date and pageSize as optional arguments.
        putDate: if putDate is False then we not print date in at the top of reports 
        data: data is the main argument of this funtion. it contain dictionary like:
        data = {
            "width":[100,100,....],
            "columns":["column1","column2",....],
            'align':["C",'C',...],
            "values":[
                ['value1','value2'],
                .....
            ]
            "invoice_number":<invoice number>
        }
        """
        pdf = FPDF(format=pageSize, unit='in')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 18.0)
        th = pdf.font_size
        pdf.ln(th)
        pdf.text(3.1, 0.5, heading)
        pdf.ln(th)
        if putDate:
            pdf.set_font('Arial', '', 10.0)
            pdf.text(2.99, 0.7, "Publish on "+time.strftime("%d %h, %Y | %I:%M %p"))
            if from_date and to_date:
                pdf.ln(th)
                pdf.set_font('Arial', 'B', 10.0)
                pdf.text(2, 4*th, "From: ")
                pdf.set_font('Arial', '', 10.0)
                pdf.text(2.5, 4*th, from_date)
                pdf.set_font('Arial', 'B', 10.0)
                pdf.text(5, 4*th, "to: ")
                pdf.set_font('Arial', '', 10.0)
                pdf.text(5.3, 4*th, to_date)
        elif print_invoice:
            pdf.set_font('Arial', 'B', 10.0)
            pdf.text(1.99, 3*th, "Bill Number: ")
            pdf.set_font('Arial', '', 10.0)
            pdf.text(2.99, 3*th, str(data['invoice_number']))
            pdf.text(4.9, 3*th, time.strftime("%d %h, %Y | %I:%M %p"))

        pdf.set_font('Arial', 'B', 10.0)
        th = pdf.font_size
        for i in range(len(data['columns'])):
            pdf.cell(data['width'][i]/100, 2*th, data['columns'][i], border=1,align='C')
        pdf.ln(2*th)
        for row in data['values']:
            pdf.set_font('Arial', '', 9.0)
            for i in range(len(row)):
                val = str(row[i])
                if val=="Total :":
                    pdf.set_font('Arial', 'B', 9.0)
                    pdf.cell(data['width'][i]/100, 2*th,val, align=data['align'][i])
                elif val or not val and write_empty_values:
                    pdf.set_font('Arial', '', 9.0)
                    pdf.cell(data['width'][i]/100, 2*th,val , border=1,align=data['align'][i])
                elif not val and not write_empty_values:
                    pdf.cell(data['width'][i]/100, 2*th,val,align=data['align'][i])
            pdf.ln(2*th)
        pdf.output(filename, 'F')

    def center(self,win):
        """
        This function make tkinter window in center of screen.
        
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
        