# imports
from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageOps
from datetime import datetime as dt
import sqlite3 as sq
from random import randint
import os
folder_address = '/'.join(__file__.split('\\')[:-1])


# funcs
def idmake(): return randint(1e7, 1e8)


def get_time_str():
    return dt.now().strftime('%Y/%m/%d | %H:%M')


def connect_make():
    if not os.path.isdir(folder_address + '/DB'):
        os.mkdir(folder_address + '/DB')
    else:
        if os.path.isfile(folder_address + '/DB/data.db'):
            return sq.connect(folder_address + '/DB/data.db')
    conn = sq.connect(folder_address + '/DB/data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE USERS (username TEXT, password TEXT)')
    c.execute('CREATE TABLE SELLS (idsell INTEGER, seller TEXT, buyer TEXT, metrazh INTEGER, price INTEGER, info TEXT, address TEXT, type TEXT, phone TEXT, date TEXT)')
    c.execute("INSERT INTO USERS (username, password) VALUES ('admin', 'example')")
    c.execute("INSERT INTO SELLS (idsell, seller, buyer, metrazh, price, info, address, type, phone, date) VALUES (10000000, 'آقای کریمی', 'خانم زعفرانی', 150, 2000000, 'خانه نوساخت و با پارکینگ', 'تهران تهران خ17شهریور ک سماواتی ک نعمت پ 6 واحد 1', 'آپارتمان', '09351221555', '2022/05/09 | 11:41')")
    conn.commit()
    return conn


connect_make()
# class of making new account page


class MakeAcc(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open(
            folder_address + "/Picture/MakeAccb.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        title = Label(self, text=' ساخت اکانت جدید ', font=(
            'arial bold', 30), bg='powder blue', relief='ridge', bd=15)
        title.place(relx=0.5, rely=0.1, anchor=CENTER)

        infoframe = Frame(self, width=100, height=250,
                          relief='ridge', bg='yellow', bd=15)
        infoframe.place(relx=0.25, rely=0.6, anchor=CENTER)

        Username = StringVar()
        Password = StringVar()
        Password_re = StringVar()

        usernamelabel = Label(infoframe, text='Username',
                              font=('arial', 10), bg='powder blue')
        usernamelabel.grid(row=0, column=0)

        usernameentry = Entry(infoframe, textvariable=Username, width=25)
        usernameentry.grid(row=0, column=1)

        passwordlabel = Label(infoframe, text='Password',
                              font=('arial', 10), bg='powder blue')
        passwordlabel.grid(row=1, column=0)

        passwordentry = Entry(
            infoframe, textvariable=Password, width=25, show='*')
        passwordentry.grid(row=1, column=1)

        password_re_label = Label(
            infoframe, text='Password', font=('arial', 10), bg='powder blue')
        password_re_label.grid(row=2, column=0)

        password_re_entry = Entry(
            infoframe, textvariable=Password_re, width=25, show='*')
        password_re_entry.grid(row=2, column=1)

        Label(infoframe, text='Repeat the password to confirm it.',
              width=30).grid(row=3, columnspan=2)

        makebtn = Button(self, text='ساخت اکانت', font=('arial', 15), bg='cadet blue', fg='cornsilk', relief='ridge',
                         bd=5, command=lambda: self.makeaccfunc(Username.get(), Password.get(), Password_re.get()))
        makebtn.place(relx=0.16, rely=0.83, anchor=CENTER)

        resetbtn = Button(self, text='پاک کردن', font=('arial', 15), bg='cadet blue', fg='cornsilk',
                          relief='ridge', bd=5, command=lambda: self.reset(usernameentry, passwordentry, password_re_entry))
        resetbtn.place(relx=0.33, rely=0.83, anchor=CENTER)

        backbtn = Button(self, text='بازگشت', font=('arial', 12), bg='yellow', relief='ridge', bd=3, command=lambda: (
            self.controller.show_frame(Login), self.reset(usernameentry, passwordentry, password_re_entry)))
        backbtn.place(relx=0.89, rely=0.9)

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

    def reset(self, *entrys):
        for ent in entrys:
            ent.delete(0, END)
        entrys[0].focus()

    def makeaccfunc(self, usr, pss, rpss):
        if pss != rpss:
            mb.showerror('Inputs Error',
                         'Passwords doesn\'t match.\nTry Again!')
            return
        if len(pss) < 5 or len(usr) < 5:
            mb.showerror(
                'Input Error', 'Passwords and Usernames should at least be 5 characters.\nTry a longer one!')
            return
        c = self.controller.conn.cursor()
        users = c.execute('SELECT username FROM USERS').fetchall()
        if (usr,) in users:
            mb.showerror(
                'Input Error', 'Selected username is already taken.\nPick another one!')
            return
        c.execute(
            'INSERT INTO USERS (username, password) VALUES (?, ?)', (usr, pss))
        self.controller.conn.commit()
        mb.showinfo('Info', 'New account is maden successfully.')


# class of login page
class Login(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.configure(bg='powder blue')

        btnmakeaccount = Button(self, text='اکانت جدید', font=(
            'arial bold', 15), bg='yellow', command=lambda: controller.show_frame(MakeAcc))
        btnmakeaccount.place(relx=.98, rely=0.98, anchor=SE)

        title = Label(self, text=' صفحه ورود مشاور املاک ', font=(
            'arial bold', 30), bg='cadet blue', relief='ridge', bd=15)
        title.place(relx=0.5, rely=0.1, anchor=CENTER)
        Username = StringVar()
        Password = StringVar()

        loginframe = Frame(self, width=500, heigh=150,
                           relief='ridge', bg='cadet blue', bd=15)
        loginframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        usernamelabel = Label(loginframe, text='Username  ', font=(
            'arial bold', 20), bg='cadet blue', fg='cornsilk')
        usernamelabel.grid(row=0, column=0)

        self.txtuser = Entry(loginframe, font=(
            'arial bold', 20), textvariable=Username)
        self.txtuser.grid(row=0, column=1)

        empty = Label(loginframe, text='', font=('arial', 1), bg='cadet blue')
        empty.grid(row=1, column=0)

        passlabel = Label(loginframe, text='Password  ', font=(
            'arial', 20, 'bold'), bg='cadet blue', fg='cornsilk')
        passlabel.grid(row=2, column=0)
        self.txtpass = Entry(loginframe, font=(
            'arial bold', 20), show="*", textvariable=Password)
        self.txtpass.grid(row=2, column=1)

        btnframe = Frame(self, width=300, heigh=80,
                         relief='ridge', bg='cadet blue', bd=15)
        btnframe.place(relx=0.5, rely=0.8, anchor=CENTER)

        btnlogin = Button(btnframe, text='ورود', width=10, font=(
            'arial', 20, 'bold'), command=lambda: self.login(Username.get(), Password.get()))
        btnlogin.grid(row=0, column=0)

        btnreset = Button(btnframe, text='پاک کردن', width=10, font=(
            'arial', 20, 'bold'), command=lambda: self.reset(self.txtuser, self.txtpass))
        btnreset.grid(row=0, column=1)

    def reset(self, *entrys):
        for ent in entrys:
            ent.delete(0, END)
        entrys[0].focus()

    def login(self, usr, pss):
        if self.get(usr, pss):
            self.controller.username = usr
            self.controller.password = pss
            self.reset(self.txtuser, self.txtpass)
            self.controller.show_frame(First)
        else:
            self.reset(self.txtuser, self.txtpass)
            mb.showerror(
                'Login Error', 'Login info was not correct.\nTry again!')
            self.txtuser.focus()

    def get(self, usr, pss):
        c = self.controller.conn.cursor()
        data = c.execute('SELECT * FROM USERS').fetchall()
        return (usr, pss) in data


# class of main page
class First(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = Image.open(folder_address + "/Picture/Firstb.jpg")
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        btnframe = Frame(self, width=300, heigh=80,
                         relief='ridge', bg='cadet blue', bd=18)
        btnframe.place(relx=0.5, rely=0.2, anchor=CENTER)

        btnmakesell = Button(btnframe, text='تنظیم قرارداد جدید', font=(
            'arial bold', 15), bg='powder blue', command=lambda: self.controller.show_frame(NewSell))
        btnmakesell.grid(row=0, column=0)

        btnchecksell = Button(btnframe, text='تاریخچه قراردادها', font=(
            'arial bold', 15), bg='powder blue', command=lambda: self.controller.show_frame(History))
        btnchecksell.grid(row=0, column=1)

        btnpasschange = Button(btnframe, text='تعویض رمز عبور', font=(
            'arial bold', 15), bg='powder blue', command=self.change_pass)
        btnpasschange.grid(row=1, column=0)
        btnexit = Button(self, text=' خروج از برنامه ', font=(
            'arial bold', 15), bg='powder blue', fg='red', relief='ridge', bd=5, command=self.controller.destroy)
        btnexit.place(relx=0.5, rely=0.92, anchor=CENTER)

        btndelacc = Button(btnframe, text='    حذف اکانت    ', font=(
            'arial bold', 15), bg='#FF7F7F', fg='red', command=self.delacc)
        btndelacc.grid(row=1, column=1)

        clockframe = Frame(self, width=110, heigh=140,
                           relief='ridge', bg='brown', bd=12)
        clockframe.place(relx=0.15, rely=0.7, anchor=CENTER)

        clocklabel = Label(clockframe, font=('arial', 16),
                           bg='cadet blue', relief='ridge')

        def time():
            string = dt.now().strftime('%H:%M:%S %p')
            clocklabel.config(text=string)
            clocklabel.after(200, time)
        time()
        clocklabel.grid(row=0, column=0)

        datelabel = Label(clockframe, font=('arial', 14),
                          bg='cadet blue', relief='ridge', width=11)

        def date():
            string = dt.now().strftime('%Y/%m/%d')
            datelabel.config(text=string)
            datelabel.after(600, date)
        date()
        datelabel.grid(row=1, column=0)

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

    def change_pass(self):
        root = Tk()
        root.configure(bg='cadet blue')
        root.title('change pass')
        root.geometry('250x32')
        root.resizable(width=False, height=False)
        passw = Entry(root)
        passw.grid(row=0, column=0, padx=4)
        btnchange = Button(root, text='Change Password!',
                           command=lambda: self.change_pass_to(passw))
        btnchange.grid(row=0, column=1, padx=4, pady=3)

    def change_pass_to(self, passwen):
        passw = passwen.get()
        print(passw)
        if len(passw) < 5:
            mb.showerror(
                'Input Error', 'Passwords should at least be 5 characters.\nTry a longer one!')
            passwen.delete(0, END)
            return
        if self.controller.password == passw:
            mb.showerror(
                'Input Error', 'Using your old password\nTry another password!')
            passwen.delete(0, END)
            return
        c = self.controller.conn.cursor()
        c.execute('UPDATE USERS SET password=? WHERE username=?',
                  (passw, self.controller.username))
        self.controller.conn.commit()
        mb.showinfo('Info', 'Your password has changed successfully.')

    def delacc(self):
        if not mb.askyesno('Deleting Account', 'Are you sure?'):
            return
        c = self.controller.conn.cursor()
        if self.controller.username == 'admin':
            mb.showerror('Delete main account',
                         'The main account of app, is not removable.')
            return
        c.execute('DELETE FROM USERS WHERE username=?',
                  (self.controller.username,))
        self.controller.conn.commit()


# class of add a new sell page
class NewSell(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = Image.open(folder_address + "/Picture/NewSellb.jpg")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        title = Label(self, text=' عقد قرارداد جدید ', font=(
            'araial', 30, 'bold'), bg='powder blue', relief='ridge', bd=15)
        title.place(relx=0.5, rely=0.15, anchor=CENTER)

        dataframe = LabelFrame(self, text='تعیین کردن',
                               padx=10, pady=10, bg='#a0dcf4')
        dataframe.place(relx=0.1, rely=0.2, anchor=CENTER)

        self.selltypes = ('زمین', 'آپارتمان', 'ویلا')
        items = StringVar(value=self.selltypes)
        checklist = Listbox(dataframe, listvariable=items,
                            width=10, height=5, bg='#ace4f4')
        checklist.pack(side=LEFT, fill=BOTH)

        sellframe = LabelFrame(self, text='مشخصات',
                               padx=5, pady=3, bg='#38bce4')
        sellframe.place(relx=0.81, rely=0.63, anchor=CENTER)

        sellerst = StringVar()
        buyerst = StringVar()
        metrazhst = StringVar()
        pricest = StringVar()
        phonest = StringVar()

        selleren = Entry(sellframe, textvariable=sellerst, width=25)
        selleren.grid(row=0, column=0)

        buyeren = Entry(sellframe, textvariable=buyerst, width=25)
        buyeren.grid(row=1, column=0)

        metrazhen = Entry(sellframe, textvariable=metrazhst, width=25)
        metrazhen.grid(row=2, column=0)

        priceen = Entry(sellframe, textvariable=pricest, width=25)
        priceen.grid(row=3, column=0)

        phoneen = Entry(sellframe, textvariable=phonest, width=25)
        phoneen.grid(row=4, column=0)

        infoen = Text(sellframe, width=23, height=4)
        infoen.grid(row=6, rowspan=2, columnspan=2)

        addressen = Text(sellframe, width=23, height=3)
        addressen.grid(row=9, rowspan=2, columnspan=2)

        sellerl = Label(sellframe, text='فروشنده', bg='#38bce4')
        sellerl.grid(row=0, column=1)

        buyerl = Label(sellframe, text='خریدار', bg='#38bce4')
        buyerl.grid(row=1, column=1)

        metrazhl = Label(sellframe, text='متراژ', bg='#38bce4')
        metrazhl.grid(row=2, column=1)

        pricel = Label(sellframe, text='قیمت', bg='#38bce4')
        pricel.grid(row=3, column=1)

        phonel = Label(sellframe, text='تلفن', bg='#38bce4')
        phonel.grid(row=4, column=1)

        infol = Label(sellframe, text='اطلاعات', bg='#38bce4')
        infol.grid(row=5, columnspan=2)

        addressl = Label(sellframe, text='آدرس', bg='#38bce4')
        addressl.grid(row=8, columnspan=2)

        idframe = LabelFrame(self, text='کد قرارداد',
                             padx=8, pady=5, bg='#38bce4')
        idframe.place(relx=0.75, rely=0.09)

        idl = Label(idframe, text='کد شناسایی', bg='#38bce4')
        idl.grid(row=0, column=1)

        idnuml = Label(idframe, relief='ridge', bg='cadet blue', fg='cornsilk')
        self.idofsell = self.idchange(idnuml)
        idnuml.grid(row=0, column=0)

        backbtn = Button(self, text='بازگشت', font=('arial', 12), bg='yellow', relief='ridge', bd=3, command=lambda: (self.controller.show_frame(First),
                                                                                                                      self.reset(
                                                                                                                          selleren, buyeren, metrazhen, priceen, phoneen),
                                                                                                                      infoen.delete(
                                                                                                                          '1.0', END),
                                                                                                                      addressen.delete(
                                                                                                                          '1.0', END),
                                                                                                                      checklist.selection_clear(
                                                                                                                          0, END),
                                                                                                                      self.idchange(idnuml)))
        backbtn.place(relx=0.04, rely=0.96, anchor=SW)

        sellbtn = Button(self, text='عقد قرار داد', font=('arial', 20, 'bold'), bg='brown', relief='ridge', bd=5, command=lambda: self.sell(self.idofsell,
                                                                                                                                            sellerst.get(),
                                                                                                                                            buyerst.get(),
                                                                                                                                            metrazhst.get(),
                                                                                                                                            pricest.get(),
                                                                                                                                            infoen.get(
                                                                                                                                                '1.0', END),
                                                                                                                                            addressen.get(
                                                                                                                                                '1.0', END),
                                                                                                                                            (checklist.curselection(
                                                                                                                                            ) + (None,))[0],
                                                                                                                                            phonest.get()))
        sellbtn.place(relx=0.37, rely=0.9, anchor=CENTER)

    def sell(self, idsell, seller, buyer, metrazh, price, info, address, choice, phone):
        seller, buyer, metrazh, price, info, address = seller.strip(), buyer.strip(
        ), metrazh.strip(), price.strip(), info.strip(), address.strip()
        if not all((seller, buyer, metrazh, price, info, address)) or choice == None:
            mb.showerror('Inputs Error', 'Please fill all of the fields!')
            return
        c = self.controller.conn.cursor()
        sl = (idsell, seller, buyer, int(metrazh), int(price), info,
              address, self.selltypes[choice], phone, get_time_str())
        if sl[1:-1] in c.execute('SELECT seller, buyer, metrazh, price, info, address, type, phone FROM SELLS').fetchall():
            mb.showerror('Repeated Sell', 'This sell has been already saved.')
            return

        c.execute('INSERT INTO SELLS (idsell, seller, buyer, metrazh, price, info, address, type, phone, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sl)
        mb.showinfo('Info', 'The sell has been saved successfully.')
        self.controller.conn.commit()

    def idchange(self, label):
        ls = self.controller.conn.cursor().execute(
            'SELECT idsell FROM SELLS').fetchall()
        r = idmake()
        while (r,) in ls:
            r = idmake()
        label.config(text=f'{r}')
        return r

    def reset(self, *entrys):
        for ent in entrys:
            ent.delete(0, END)
        entrys[0].focus()

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


# class of history page
class History(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = Image.open(folder_address + "/Picture/Historyb.jpg")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        self.counter = 0

        self.backbtn = Button(self, text='بازگشت', font=('arial', 12), bg='yellow', relief='ridge', bd=3, command=lambda: (self.reset_counter(),
                                                                                                                           self.controller.show_frame(First)))
        self.backbtn.place(relx=0.99, rely=0.98, anchor=SE)

        idframe = LabelFrame(self, text='کد قرارداد',
                             padx=8, pady=5, bg='#38bce4')
        idframe.place(relx=0.98, rely=0.05, anchor=NE)
        nextbtn = Button(idframe, text='   بعدی   ', font=(
            'arial', 12), relief='raised', command=lambda: self.get_deal(+1))
        lastbtn = Button(idframe, text='   قبلی   ', font=(
            'arial', 12), relief='raised', command=lambda: self.get_deal(-1))
        nextbtn.grid(row=2, column=2)
        lastbtn.grid(row=2, column=0)
        idl = Label(idframe, text='کد شناسایی', bg='#38bce4')
        idl.grid(row=0, column=2)

        self.idst = StringVar()
        idl = Entry(idframe, textvariable=self.idst)
        idl.grid(row=0, column=0, columnspan=2)

        searchbtn = Button(idframe, text='جست و جو', font=(
            'arial', 11), command=lambda: self.get_deal(s=self.idst.get()))
        searchbtn.grid(row=2, column=1)

        self.get_deal()

    def reset_counter(self):
        self.counter = 0
        self.get_deal()

    def show_deal(self, deal):
        try:
            for i in (self.infoframe,):
                i.destroy()
        except:
            pass
        idnum, seller, buyer, metrazh, price, info, address, type, phone, date = deal

        self.infoframe = LabelFrame(self, text='اطلاعات قرارداد', bg='#b4e4fc')
        self.infoframe.place(relx=0.005, rely=0.48, anchor=NW)

        self.idf = LabelFrame(self.infoframe, width=500)
        self.idf.grid(row=0, column=0, padx=7, pady=10)

        self.idcodel = Label(self.idf, text='کد شناسایی', padx=1, pady=2)
        self.idcodel.grid(row=0, column=1, )
        self.idnuml = Label(self.idf, text=str(
            idnum), relief='ridge', bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.idnuml.grid(row=0, column=0)

        self.sellerf = LabelFrame(self.infoframe)
        self.sellerf.grid(row=0, column=1, padx=7, pady=10)
        self.sellercode = Label(
            self.sellerf, text='نام فروشنده', padx=1, pady=2)
        self.sellercode.grid(row=0, column=1)
        self.sellername = Label(self.sellerf, text=seller, relief='ridge',
                                bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.sellername.grid(row=0, column=0)

        self.buyerf = LabelFrame(self.infoframe)
        self.buyerf.grid(row=0, column=2, padx=7, pady=10)
        self.buyercode = Label(self.buyerf, text='نام خریدار', padx=1, pady=2)
        self.buyercode.grid(row=0, column=1)
        self.buyername = Label(self.buyerf, text=buyer, relief='ridge',
                               bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.buyername.grid(row=0, column=0)

        self.metrazhf = LabelFrame(self.infoframe)
        self.metrazhf.grid(row=0, column=3, padx=7, pady=10)
        self.metrazhcode = Label(
            self.metrazhf, text='متراژ ملک', padx=1, pady=2)
        self.metrazhcode.grid(row=0, column=1)
        self.metrazhnum = Label(self.metrazhf, text=str(
            metrazh), relief='ridge', bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.metrazhnum.grid(row=0, column=0)

        self.pricef = LabelFrame(self.infoframe)
        self.pricef.grid(row=1, column=0, padx=7, pady=10)
        self.pricecode = Label(self.pricef, text='قیمت ملک', padx=1, pady=2)
        self.pricecode.grid(row=0, column=1)
        self.pricenum = Label(self.pricef, text=str(
            price), relief='ridge', bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.pricenum.grid(row=0, column=0)

        self.phonef = LabelFrame(self.infoframe)
        self.phonef.grid(row=1, column=1, padx=7, pady=10)
        self.phonecode = Label(self.phonef, text='شماره تلفن', padx=1, pady=2)
        self.phonecode.grid(row=0, column=1)
        self.phonenum = Label(self.phonef, text=phone, relief='ridge',
                              bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.phonenum.grid(row=0, column=0)

        self.datef = LabelFrame(self.infoframe)
        self.datef.grid(row=1, column=2, columnspan=2, padx=7, pady=10)
        self.datecode = Label(
            self.datef, text='تاریخ عقد قرار داد', padx=1, pady=2)
        self.datecode.grid(row=0, column=1)
        self.datenum = Label(self.datef, text=date, relief='ridge',
                             bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.datenum.grid(row=0, column=0)

        self.addressf = LabelFrame(self.infoframe)
        self.addressf.grid(row=2, columnspan=4, padx=7, pady=10, sticky=E)
        self.addresscode = Label(self.addressf, text='ادرس', padx=1, pady=2)
        self.addresscode.grid(row=0, column=1)
        self.addressnum = Label(self.addressf, text=address, relief='ridge',
                                bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.addressnum.grid(row=0, column=0)

        self.infof = LabelFrame(self.infoframe)
        self.infof.grid(row=3, columnspan=4, padx=7, pady=10, sticky=E)
        self.infocode = Label(self.infof, text='اطلاعات', padx=1, pady=2)
        self.infocode.grid(row=0, column=1)
        self.infonum = Label(self.infof, text=info, relief='ridge',
                             bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.infonum.grid(row=0, column=0)

    def get_deal(self, a=0, s=0):
        c = self.controller.conn.cursor()
        lst = c.execute('SELECT * FROM SELLS').fetchall()
        n = len(lst)
        if type(s) == str:
            if s:
                k = [i for i in lst if i[0] == int(s)]
                if not k:
                    mb.showerror(
                        'Input Error', 'The entererd id doesn\'t match with any saved deals.')
                    self.idst.set('')
                    return
                self.show_deal(k[0])
                return
            mb.showerror('Input Error', 'The field is empty.')
            return
        self.counter += a
        self.counter %= n
        self.idst.set(lst[self.counter][0])
        self.show_deal(lst[self.counter])

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


# main window(App)
class App(Tk):
    def __init__(self, *args, **keywargs):
        self.conn = connect_make()
        Tk.__init__(self, *args, **keywargs)
        self.geometry('600x400')
        self.resizable(width=False, height=False)
        self.title('مشاور املاک')
        self.iconbitmap(folder_address + '/Picture/icon.ico')

        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, First, MakeAcc, NewSell, History,):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            self.show_frame(F)

        self.show_frame(Login)

    def show_frame(self, cont):
        self.frames[cont].tkraise()


# make an instance and run the app
app = App()
app.mainloop()
