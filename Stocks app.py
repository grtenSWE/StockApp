
# modules
from tkinter import *
from tkmacosx import Button
from tkmacosx import Radiobutton
from Stock_Class.Stock_Class import Stocks
from Data_class.Data_class import Data


# supporting classes
class Num():
    """this class is used for row and column gridding of the widgets"""
    def __init__(self):
        self.rn = -1
        self.cn = -1

    def rcall(self):
        """call the row number"""
        self.rn += 1
        return self.rn

    def ccall(self):
        """call the column number"""
        self.cn += 1
        return self.cn

    def rreset(self):
        """reset row number"""
        self.rn = -1
        
    def creset(self):
        """reset column number"""
        self.cn = -1

    def reset(self):
        """reset everything"""
        self.rreset()
        self.creset()


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="enter",type="", color='grey'):
        if type == "password":
            super().__init__(master,show="*")
        else:
            super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


# main GUI class
class GUI: 
    """this class runs the interface for customers"""
    def __init__(self, parent):
        # initialising fonts 
        self.MED_FONT = ("Helvetica", 65, "bold")
        self.MED_FONT1 = ("Helvetica", 36)
        self.MED_FONT2 = ("Helvetica", 36, "bold")
        self.SMALL_FONT = ("Helvetica", 26, "bold")
        self.SMALL_FONT2 = ("Helvetica", 15)
        self.SMALL_FONT3 = ("Helvetica", 18)
        self.SMALL_FONT4 = ("Helvetica", 15, "underline")
        self.SMALL_FONT5 = ("Helvetica", 15, "bold")
        self.TINY_FONT = ("Helvetica", 12)
        self.TINY_FONT2 = ("Helvetica", 12, "underline")
        
        self.ALL_STOCKS = Stocks()
        self.Data = Data()

        self.screen = ""
        self.current_screen = ""
        self.current_stock_cards = []

        # initialising main frame
        self.height = 646
        self.width = 1034 
        self.main = Frame(parent, height= self.height, width= self.width, bg='light grey')

        # initialising sub frames
        self.login_card_f = Frame(self.main, height=300, width=400, bg='white')
        self.acc_card_f = Frame(self.main, height=300, width=400, bg='white')
        self.logout_card_f = Frame(self.main, height=300, width=400, bg='white')
        self.addstock_card_f = Frame(self.main, height=300, width=400, bg='white')

        self.top_f = Frame(self.main,height=25,width=self.width,bg="white")
        self.line_f = Frame(self.main,height=5,width=self.width,bg="white")
        self.mid_f = Frame(self.main,height=20,width=self.width,bg="white")
        self.info_f = Frame(self.main,height=610,width=self.width,bg="white")
        self.bottom_f = Frame(self.main,height=11,width=self.width,bg="white")

        self.HOME_LABELS = ["Ticker", "Price","24h%","7d%", "mkt Cap", "Vol 24h"]
        self.CATERGORIES = ["tech","energy","pharma","finance","auto","retail","watch_list"]
     
        #login card widgets
        self.login_wid = []
        self.login_wid.append(Label(self.login_card_f, text="Login", font=self.MED_FONT2, bg="white"))
        self.login_wid.append(Label(self.login_card_f, text="Username", font=self.SMALL_FONT3, bg="white"))
        self.username = EntryWithPlaceholder(self.login_card_f, " Enter your username  ")
        self.login_wid.append(self.username)
        self.login_wid.append(Label(self.login_card_f, text = "Password", font= self.SMALL_FONT3,bg="white"))
        self.password = EntryWithPlaceholder(self.login_card_f, " Enter password  ", "password","light grey")
        self.login_wid.append(self.password)
        self.login_wid.append(Button(self.login_card_f,text= "Login",command=self.login_verify, bg="#4385F4",fg="white",width=245))
        self.login_wid.append(Button(self.login_card_f,text= "Create an account",command= self.create_acc_screen, bg="#4385F4",fg="white", width=245))
        self.login_error = Label(self.login_card_f, text = "", font= self.SMALL_FONT2,bg="white",fg="red")
        self.login_wid.append(self.login_error)

        #Create an account card widgets
        self.create_acc_wid = []
        self.create_acc_wid.append(Label(self.acc_card_f, text="Create an account", font=self.MED_FONT2, bg="white"))
        self.create_acc_wid.append(Label(self.acc_card_f, text="Already have an account?", font=self.SMALL_FONT2, bg="white"))
        self.create_acc_wid.append(Label(self.acc_card_f, text="Login", font=self.SMALL_FONT4, bg="white",fg="#4385F4"))
        self.create_acc_wid.append(Label(self.acc_card_f, text="Username", font=self.SMALL_FONT3, bg="white"))
        self.create_username = EntryWithPlaceholder(self.acc_card_f, " Enter your username")
        self.create_acc_wid.append(self.create_username)
        self.create_acc_wid.append(Label(self.acc_card_f, text = "Password", font= self.SMALL_FONT3,bg="white"))
        self.create_password = EntryWithPlaceholder(self.acc_card_f, " Enter your password")
        self.create_acc_wid.append(self.create_password)
        self.create_password2 = EntryWithPlaceholder(self.acc_card_f, " Confirm your password")
        self.create_acc_wid.append(self.create_password2)
        self.create_acc_wid.append(Label(self.acc_card_f,text="Password must be: atleast 8 characters, with atleast 1 upper case letter and atleast 1 number",font=self.TINY_FONT,fg="grey"))
        self.create_acc_wid.append(Button(self.acc_card_f,text= "Create an account",command=self.create_verify, bg="#4385F4",fg="white", width=510))
        self.create_acc_error = Label(self.acc_card_f, text = "", font= self.SMALL_FONT2,bg="white",fg="red")
        self.create_acc_wid.append(self.create_acc_error)

        #home screen widgets

        #logout confirmation card widgets
        self.logout_wid = []
        self.logout_wid.append(Label(self.logout_card_f, text="Do you want to logout?", font=self.MED_FONT1))
        self.logout_wid.append(Button(self.logout_card_f,text= "Yes",command=self.login_screen, bg="#4385F4",fg="white",width=245))
        self.logout_wid.append(Button(self.logout_card_f,text= "No",command=self.back, bg="light grey", width=245))

        #navigation bar widgets
        self.nav_wid = []
        self.nav_wid.append(Button(self.top_f,text="Tech",command=lambda screen="tech": self.change_catergory(screen),bg="#EBEBEB",width=100,overbackground='light grey'))
        self.nav_wid.append(Button(self.top_f,text="Energy",command=lambda screen="energy": self.change_catergory(screen),bg="#EBEBEB",width=100,overbackground='light grey'))
        self.nav_wid.append(Button(self.top_f,text="Pharma",command=lambda screen="pharma": self.change_catergory(screen),bg="#EBEBEB",width=100,overbackground='light grey'))
        self.nav_wid.append(Button(self.top_f,text="Financial",command=lambda screen="finance": self.change_catergory(screen),bg="#EBEBEB",width=100,overbackground='light grey'))
        self.nav_wid.append(Button(self.top_f,text="Automakers",command=lambda screen="auto": self.change_catergory(screen),bg="#EBEBEB",width=100,overbackground='light grey'))
        self.nav_wid.append(Button(self.top_f,text="Retail",command=lambda screen="retail": self.change_catergory(screen),bg="#EBEBEB",width=100,overbackground='light grey'))
        self.nav_wid.append(Button(self.top_f,text="Logout",command=self.logout_confirm,bg="#4385F4",fg="white",width=80,overbackground='#1575FF'))
        self.nav_wid.append(Button(self.top_f,text="Watch list",command=lambda screen="watch_list": self.change_catergory(screen),bg="#EBEBEB",width=100,overbackground='light grey'))

        self.add_btn = Button(self.mid_f,text="Add new stocks",command=self.add_stocks_screen,bg="#4385F4",fg="white",width=130)
       
        
        self.back_btn = Button(self.bottom_f,text="<",command=lambda status="back": self.change_page(status),bg="light grey",width=40)
        self.indicator_lbl = Label(self.bottom_f,text="1",width=2)
        self.forward_btn = Button(self.bottom_f,text=">",command=lambda status="forward": self.change_page(status),bg="light grey",width=40)

        self.nav_line = self.getImage_lbl(self.line_f,"white","assets/div_line.png",(988,8))
        self.div_line = self.getImage_lbl(self.mid_f,"white","assets/div_line.png",(988,8))


        self.main.grid(ipadx=200,ipady=50)

        self.login_screen()


    def login_screen(self,event=None): 
        #GUI for the Login screen, griding all the login screen widgets

        self.login_card_f.bind('<Return>', self.login_verify)
        self.username.bind('<Return>', self.login_verify)
        self.password.bind('<Return>', self.login_verify)

        try:
            self.destroy_screen(self.loading)
        except:
            pass

        self.forget_screen(self.acc_card_f)
        self.forget_screen(self.logout_card_f)

        self.loading = Label(self.mid_f, text ='Loading...',fg="red",font=self.SMALL_FONT3)

        self.Data = Data()

        n = Num()
        for i in self.login_wid[0:8]:
            i.grid(row=n.rcall(),columnspan= 2,padx=20,sticky=NSEW)
        for i in [0,1,3,5,7]:
            self.login_wid[i].grid(pady=(20,0),sticky=W)
        for i in [2,4]:
            self.login_wid[i].grid(ipadx=160,ipady=8)
        self.login_wid[0].grid(pady=(20))
        n.reset()
        for i in self.login_wid[5:7]:
            i.grid(row=5, column=n.ccall(), ipady=5, pady=(20,0),columnspan=1)
        for i in [5]:
            self.login_wid[i].grid(sticky=E,padx=(20,10))
        for i in [6]:
            self.login_wid[i].grid(sticky=W,padx=(10,20))
  
        self.login_card_f.grid(ipady=20, padx=240, pady=120)

       
    def create_acc_screen(self): 
        #GUI for the create an account screen, griding all the widgets

        self.forget_screen(self.login_card_f)
        self.acc_card_f.bind('<Return>', self.create_verify)
        self.create_username.bind('<Return>', self.create_verify)
        self.create_password.bind('<Return>', self.create_verify)
        self.create_password2.bind('<Return>', self.create_verify)
        
        n = Num()
        #grids all widgets
        for i in self.create_acc_wid[0:11]:
            i.grid(row=n.rcall(),columnspan=3,padx=20,sticky=W)
        #grids specifics labels
        for i in [0,3,5,10]:
            self.create_acc_wid[i].grid(pady=(20,0))
        #grids specifics entry boxes
        for i in [4,6,7]:
            self.create_acc_wid[i].grid(ipadx=160,ipady=8)
        self.create_acc_wid[9].grid(pady=(20,0),ipady=5)
        n.reset()

        for i in [1,2]:
            self.create_acc_wid[i].grid(row=1, column=n.ccall(),padx=(22,0),pady=(0,20),sticky=W)
        
        for i in [2]:
            self.create_acc_wid[i].grid(padx=15)
            self.create_acc_wid[i].bind('<Button-1>', self.login_screen)

        self.acc_card_f.grid(ipady=40, padx=240, pady=75)
 
    
    def login_verify(self,event=None):
        #get username and password
        self.usern = self.username.get().strip()
        self.passw = self.password.get().strip()

        value = self.Data.username_verify(self.usern,self.passw)

        if value == "success":
            self.home_screen()
            self.username.delete(0,END)
            self.password.delete(0,END)      
            self.login_error.configure(text="")
        
        else:
            self.login_error.configure(text=value)


    def create_verify(self,event=None):
        self.usern = self.create_username.get().strip()
        self.passw = self.create_password.get().strip()
        password_conf = self.create_password2.get().strip()

        value = self.Data.create_verify(self.usern,self.passw,password_conf)

        if value == "success":
            self.home_screen()
            self.create_acc_error.configure(text="")
            self.create_username.delete(0,END)
            self.create_password.delete(0,END)
            self.create_password2.delete(0,END)

        else:
            self.create_acc_error.configure(text=value)


#   -------------------------------- GUI for everything once logged in -----------------------------------------------------

    def home_screen(self):
        n = Num() 
        self.current_screen = ""
        self.screen = ""
        self.forget_screen(self.login_card_f)
        self.forget_screen(self.acc_card_f)
        
        #grid home screen frames
        self.top_f.grid(row=0,column=0,sticky=N)
        self.line_f.grid(row=1,column=0,sticky=N)
        self.mid_f.grid(row=2,column=0)
        self.info_f.grid(row=3,column=0)
        self.bottom_f.grid(row=4,column=0)
        
        #grids nav bar buttons
        for wid in self.nav_wid[0:]:
            wid.grid(row=0, column=n.ccall(),padx=5,pady=(30,2),ipady=2)
       
        self.nav_wid[0].grid(padx=(28,5))
        self.nav_wid[5].grid(padx=(5,68))
        self.nav_wid[6].grid(padx=(70,5))
        self.nav_wid[7].grid(padx=(5,28))

        self.nav_line.grid(padx=20)
        n.reset()

        #grids titles for the stock frames
        self.data_title()
        self.forget_screen(self.add_btn)

        #creating the stock card frames
        self.change_catergory("tech")

        self.back_btn.grid(row=0,column=0,ipady=2,padx=(463,0))
        self.indicator_lbl.grid(row=0,column=1,padx=2,pady=(7,8))
        self.forward_btn.grid(row=0,column=2,ipady=2,padx=(0,464))
          
        #switching screen buttons


    def stock_cards_GUI(self, stocks):
        """creates a list of item cards"""
        self.stock_cards = []
        for stock in stocks:
            self.stock_cards.append(self.item_card(stock))


    #medthod for intitialising and gridding the individual info inside of the stock cards
    def item_card(self, stock):
        # initialising widgets

        n = Num()

        self.stock = stock
        self.card_f = Frame(self.info_f, bg='white', borderwidth=2, relief=GROOVE)
        self.card_f.bind("<Button-1>", lambda event, i=stock: self.show_graph(event, i))

        self.name_f = Frame(self.card_f, bg='white')
        self.name_f.grid(row=0,column=0)
        card_wid = []

        spacer = Button(self.name_f,height=1,font=self.TINY_FONT)
        spacer.grid(row=2,column=0,padx=(0,111))

        card_wid.append(Label(self.name_f, text=stock[0],font=self.SMALL_FONT3))   
        card_wid.append(Label(self.name_f, text=stock[1],font=self.TINY_FONT))
     
        card_wid.append(Label(self.card_f, text=stock[2],font=self.SMALL_FONT3,width=5))

        if "-" in stock[3]:
            card_wid.append(Label(self.card_f, text=f"{stock[3]}%",font=self.SMALL_FONT3,fg="red",width=5))
        else:
            card_wid.append(Label(self.card_f, text=f"{stock[3]}%",font=self.SMALL_FONT3,fg="green",width=5))

        if "-" in stock[4]:
            card_wid.append(Label(self.card_f, text=f"{stock[4]}%",font=self.SMALL_FONT3,fg="red",width=5))
        else: 
            card_wid.append(Label(self.card_f, text=f"{stock[4]}%",font=self.SMALL_FONT3,fg="green",width=5))

        card_wid.append(Label(self.card_f, text=stock[5],font=self.SMALL_FONT3,width=6))
        card_wid.append(Label(self.card_f, text=stock[6],font=self.SMALL_FONT3,width=6))

        for funde_info in(card_wid):
            funde_info.grid(row=0,column=n.ccall(), padx=55,pady=(5),rowspan=2,sticky=E)
            funde_info.bind("<Button-1>", lambda event, i=stock: self.show_graph(event, i))

        card_wid[0].grid(row=0,column=0,pady=(5,0),rowspan=1,padx=(10,0),sticky=W) 
        card_wid[1].grid(row=1,column=0,pady=(0,4),rowspan=1, padx=(10,0),sticky=W)
        card_wid[2].grid(padx=(0,52))
        card_wid[6].grid(padx=(44,30)) 

        return self.card_f


    def logout_confirm(self):
        self.forget_homescreen()
     
        n = Num()

        self.logout_wid[0].grid(row=0,columnspan= 2,padx=20,pady=(120,20),sticky=NSEW)
        
        n.reset()
        for i in self.logout_wid[1:]:
            i.grid(row=1, column=n.ccall(), ipady=5, pady=(20,80))
        for i in [1]:
            self.logout_wid[i].grid(sticky=E,padx=(20,10))
        for i in [2]:
            self.logout_wid[i].grid(sticky=W,padx=(10,20))
  
        self.logout_card_f.grid(ipady=20, padx=240, pady=140)

    
    def split(self, arr, size):
    #splits the whole stock cards list into more lists of 5 items each
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr   = arr[size:]
        arrs.append(arr)
        return arrs


    def change_catergory(self, screen):
        #changes the menu screen
        self.screen = screen
       
        if self.screen != self.current_screen:
            self.destroy_screen(self.info_f)
            self.info_f = Frame(self.main,height=610,width=self.width,bg="white")
            self.info_f.grid(row=3,column=0)

            for catergory in self.CATERGORIES:
                if catergory == self.screen:
                    self.current_screen = catergory
                    value = self.Data.catergories_functionmap(catergory)
                    self.stock_cards_GUI(value())
                        
                    if len(value()) == 0:
                        self.data_title("loading")

                    else:
                        self.data_title()

        #gridding card widgets
        n = Num()
       
        self.all_stock_cards = self.split(self.stock_cards,5)

        self.indicator_lbl.configure(text="1")
        for card in self.all_stock_cards[0]: 
            card.grid(row=n.rcall(), column=0, pady=8,sticky=NSEW, padx=(30,31))


    def change_page(self,status):
        n = Num()
        if status == "forward":
            index = 1
            self.forget_screen(self.all_stock_cards[0])

        else:
            index = 0
            self.forget_screen(self.all_stock_cards[1])
 
        try: 
            for card in self.all_stock_cards[index]: 
                card.grid(row=n.rcall(), column=0, pady=8,sticky=NSEW, padx=(30,31)) 
            self.indicator_lbl.configure(text=index+1)
        except:
            for card in self.all_stock_cards[0]: 
                card.grid(row=n.rcall(), column=0, pady=8,sticky=NSEW, padx=(30,31))


    def data_title(self,status=""):
        n=Num()

        home_wid = []
       
        if self.screen == "watch_list":
            self.add_btn.grid(row=0,column=5,padx=28,sticky=E,ipady=2,pady=(0,60))
            
            if status == "loading":
                self.loading.grid(row=0,column=0,padx=28,sticky=E,ipady=2,pady=(0,60))  
          
        else:
            self.forget_screen(self.add_btn)
            self.forget_screen(self.loading)

            for i in(self.HOME_LABELS):
                labels = Label(self.mid_f, text=i,font=self.SMALL_FONT3,width=6)
                labels.grid(row=0,column=n.ccall(), padx=49,pady=(90,0))
                home_wid.append(labels)

            home_wid[0].grid(padx=(43,52))
            home_wid[5].grid(padx=(48,67))
            self.div_line.grid(row=1,column=0,columnspan=6)

  
    def show_graph(self,event,stock):
        self.forget_homescreen()

        info = self.ALL_STOCKS.info_get(stock[0])
        allcards_info = [stock[5],info[0],[info[1],info[2],stock[6]]]

        #initialising the 2 main frames of this window
        self.full_top_f = Frame(self.main,height=11,width=self.width,bg="white")
        self.full_bottom_f = Frame(self.main,height=11,width=self.width,bg="white")
        self.full_top_f.grid(row=0,column=0)
        self.full_bottom_f.grid(row=1,column=0)

        #initialising the subframes of this window
        title_f = Frame(self.full_top_f,bg='white')
        self.timeline_f = Frame(self.full_top_f, bg='light grey')
        self.fundementals_f = Frame(self.full_top_f, bg='White')

        title_f.grid(row=0,column=1,pady=(60,10),sticky=W)
        self.timeline_f.grid(row=1,column=1,padx=(0,90))
        self.fundementals_f.grid(row=0,column=2,rowspan=2,padx=(0,132),pady=(60,0))

        #back button for going back to the screen they came from
        back_home_btn = self.getImage_lbl(self.full_top_f,'white',"assets/back_btn.png",(50,80))
        back_home_btn.bind('<Button-1>', self.back)
        back_home_btn.grid(row=0,column=0,rowspan=2,padx=(28,80))

        #ticker symbol and full names of the stock
        Label(title_f,text=stock[0],font=self.SMALL_FONT).grid(row=0,column=0)
        Label(title_f,text=stock[1],font=self.SMALL_FONT2).grid(row=0,column=1)

        #timeframes labels that allows user to switch the time frames on the graph
        self.timeline()

        #additional info about the stocks
        self.info_card(allcards_info)

        #displaying that graph
        graph = self.getImage_lbl(self.full_bottom_f,'white',"current_graph.png",(900,500),(0,80,700,470))
        graph.grid(padx=(90,36),pady=(10,0))


    def timeline(self):
        n = Num()
        self.timeline_lts = ["7D","1M","3M","YTD","1Y","2Y","10Y","ALL"]
        self.timeline_wid = []
        self.index_var = IntVar()
        index = -1

        for timeframe in self.timeline_lts:
            index +=1
            labels = Radiobutton(self.timeline_f, text=timeframe, value = index, variable=self.index_var, font=self.SMALL_FONT2,
            bg="light grey", selectcolor="light grey", indicatoron=0, borderwidth=1, command=self.switch_timeframe)
            labels.grid(row=0,column=n.ccall(), padx=2)
            self.timeline_wid.append(labels)

        self.timeline_wid[3].configure(font=self.SMALL_FONT5) 
        self.ALL_STOCKS.graph_get("YTD") #rendering the graph using a method from the Stocks() class


    def switch_timeframe(self):
        self.destroy_screen(self.full_bottom_f)
        self.full_bottom_f = Frame(self.main,height=11,width=self.width,bg="white")
        self.full_bottom_f.grid(row=1,column=0)
        timeline_keys = self.Data.timelines_keys()
        
        for i in self.timeline_wid:
            i.configure(font=self.SMALL_FONT2)

        self.timeline_wid[self.index_var.get()].configure(font=self.SMALL_FONT5)
        self.ALL_STOCKS.graph_get(timeline_keys[self.index_var.get()])
        graph = self.getImage_lbl(self.full_bottom_f,'white',"current_graph.png",(900,500),(0,80,700,470))
        graph.grid(padx=(90,36),pady=(10,0))
  

    def info_card(self, allcards_info):
        self.info_cards = []
        info = self.Data.info_keys(allcards_info[2])
        frames = []
        x = 0
        n = Num()

        for i in range(3):
            frame = Frame(self.fundementals_f,bg='white', borderwidth=2, relief=GROOVE)
            frame.grid(row=0,column=n.ccall(),padx=5,sticky=NSEW)
            frames.append(frame)

        n.reset()

        Label(frames[0],text="Market Cap",font=self.SMALL_FONT3,fg="grey").grid(row=0)
        Label(frames[0],text=allcards_info[0],font=self.SMALL_FONT3).grid(row=1)
        Label(frames[1],text="Dividend",font=self.SMALL_FONT3,fg="grey").grid(row=0)
        Label(frames[1],text=f"{allcards_info[1]}%",font=self.SMALL_FONT3).grid(row=1)

        for i in info:
            line = Label(frames[2],text=i,font=self.SMALL_FONT2)
            x += 1
            if x > 3:
                if x == 4:
                    n.reset()
                line.grid(row=n.rcall(),column=1)
            else:
                line.grid(row=n.rcall(),column=0)

        
    def add_stocks_screen(self): 
        n = Num()
        self.forget_homescreen()
        self.stock_search_data = ""
        self.addstock_card_f.grid(ipady=20, padx=300)
        as_top_f = Frame(self.addstock_card_f)
        self.as_bottom_right_f = Frame(self.addstock_card_f)
        
        try:
            self.destroy_screen(self.as_bottom_f)
            self.as_bottom_f = Frame(self.addstock_card_f)
        except:
            self.as_bottom_f = Frame(self.addstock_card_f)

        as_top_f.grid(row=0,padx=28,columnspan=2)
        self.as_bottom_f.grid(row=1,column=0,padx=(28,0))
        self.as_bottom_right_f.grid(row=1,column=1)

        Button(as_top_f,text="Done",command=self.save_watchlist,bg="light grey",width=80).grid(row=0,column=0,ipady=2,pady=(15,10),sticky=W)
        self.search_entry = EntryWithPlaceholder(as_top_f, " Search Full Tickers Only")
        self.search_entry.grid(row=1,column=0,ipadx=70,ipady=8,pady=(0,10))
        Button(as_top_f,text="Go",command=self.search,bg="#4385F4",fg="white",width=40).grid(row=1,column=1, pady=(0,10), ipady=8) 

        self.watchlist()
        self.mini_stockcards_get()

        self.up_btn = Button(self.as_bottom_right_f,text="▲",command=lambda status="up": self.change_page_mini_stock_cards(status),bg="light grey",width=40)
        self.mini_indicator_lbl = Label(self.as_bottom_right_f,text="1",width=2)
        self.down_btn = Button(self.as_bottom_right_f,text="▼",command=lambda status="down": self.change_page_mini_stock_cards(status),bg="light grey",width=40)

        self.up_btn.grid(row=0,column=0)
        self.mini_indicator_lbl.grid(row=1,column=0)
        self.down_btn.grid(row=2,column=0) 

        self.index = 0

        self.splitted_mini_stock_cards = self.split(self.mini_stock_cards,7)
     
        for card in self.splitted_mini_stock_cards[0]: 
            card.grid(row=n.rcall(), column=0, pady=6,sticky=NSEW, padx=(10,0))


    def change_page_mini_stock_cards(self,status):
        n = Num()

        if status == "down" and self.index < 3:
            self.forget_screen(self.splitted_mini_stock_cards[self.index])
            self.index +=1
                
        elif status == "up" and self.index > 0:
            self.forget_screen(self.splitted_mini_stock_cards[self.index])
            self.index -=1

        else:
            pass
            
        for card in self.splitted_mini_stock_cards[self.index]: 
            card.grid(row=n.rcall(), column=0, pady=6,sticky=NSEW, padx=(10,0))
            self.mini_indicator_lbl.configure(text=self.index+1)
    

    def mini_stockcards_get(self):
        """creates a list of item cards"""
        self.mini_stock_cards = []
        full_lts = self.ALL_STOCKS.tech_get() + self.ALL_STOCKS.finance_get() + self.ALL_STOCKS.pharma_get()
        for stock in full_lts:
            self.mini_stock_cards.append(self.mini_card(stock))


    def mini_stockcards_search_get(self,search_data):
        """creates a list of item cards"""
        self.mini_stock_cards_search = (self.mini_card(search_data))
            
    #medthod for intitialising and gridding the indibidual info inside of the stock cards
    def mini_card(self, stock_info):
        """creates menu item cards"""
        # initialising widgets
        n = Num()
        self.card_wid = []

        self.card_f = Frame(self.as_bottom_f, bg='white', borderwidth=2, relief=GROOVE)

        spacer = Button(self.card_f,height=1,font=self.TINY_FONT)
        spacer.grid(row=2,column=0,padx=(0,150))

        self.card_wid.append(Label(self.card_f, text=stock_info[0],font=self.SMALL_FONT3))
        self.card_wid.append(Label(self.card_f, text=stock_info[1],font=self.TINY_FONT))
        self.card_wid.append(Button(self.card_f, text="Add",command = lambda i=stock_info[0], func = "add": self.stock_modify(i,func),bg="#4385F4",fg="white",width=90))
 
        for funde_info in(self.card_wid):
            funde_info.grid(row=0,column=n.ccall(),rowspan=3,sticky=E)

        self.card_wid[0].grid(pady=(5,0),rowspan=1,padx=(10),sticky=W) 
        self.card_wid[1].grid(row=1,column=0,pady=(0,3),rowspan=1, padx=(10,0),sticky=W)
        self.card_wid[2].grid(padx=(0,10),ipady=2)
        self.check_stocks(stock_info[0])

        return self.card_f


    def search(self):
        self.stock_search_data = self.ALL_STOCKS.stock_search_get(self.search_entry.get())
        self.destroy_screen(self.as_bottom_f)
        self.as_bottom_f = Frame(self.addstock_card_f)
        self.as_bottom_f.grid(row=1,column=0,padx=(28,0))
      
        self.mini_stockcards_search_get(self.stock_search_data)
        n = Num()
        n.reset()
        self.mini_stock_cards_search.grid(row=n.rcall(), column=0, pady=(10,424),sticky=NSEW, padx=10)       
       
    #check if the stock is already added in the watchlist 
    def check_stocks(self,ticker):
        if ticker in self.stocks_info:
            self.card_wid[2].configure(text="remove",bg="#78A0F0",command= lambda i=ticker, func = "remove": self.stock_modify(i,func))

    #appends the existing watchlist into a list for that list to be modify
    def watchlist(self):
        self.stocks_info =[]
        self.stocks_info = self.Data.watchlist_get(self.usern)
           
           
    def stock_modify(self,stock,func):
        n = Num()

        if func == "add":
            self.stocks_info.append(stock)
        else:
            self.stocks_info.remove(stock)

        try:
            self.mini_stockcards_search_get(self.stock_search_data)
            self.mini_stock_cards_search.grid(row=n.rcall(), column=0, pady=(10,424),sticky=NSEW, padx=10) 
        except:         
            self.mini_stockcards_get()
            self.splitted_mini_stock_cards = self.split(self.mini_stock_cards,7)
            for card in self.splitted_mini_stock_cards[self.index]: 
                card.grid(row=n.rcall(), column=0, pady=6,sticky=NSEW, padx=(10,0))


    def save_watchlist(self):
            self.Data.watchlist_save(self.usern,self.passw,self.stocks_info)
            self.back()
#   -------------------------------- Suppporting methods for GUI -----------------------------------------------------

                
    @staticmethod
    def forget_screen(widgets):
        """forgets all the widgets on the window given the list of widgets"""
        try:
            for wid in widgets:
                wid.grid_forget()
        except:
            widgets.grid_forget()


    @staticmethod
    def destroy_screen(widgets):
        """forgets all the widgets on the window given the list of widgets"""
        try:
            for wid in widgets:
                wid.destroy()
        except:
            widgets.destroy()

   
    def getImage_lbl(self,frame, bg, filepath, resize, crop = 0):
        """returns a working image label"""
        image = self.Data.getImage(filepath,resize,crop)
        img_lbl = Label(frame, image=image, bg=bg)
        img_lbl.image = image
        return img_lbl
        

    def back(self,event=None):
        if event == None:
            self.forget_screen(self.logout_card_f)
            self.forget_screen(self.addstock_card_f)
        else:
            self.destroy_screen(self.full_top_f)
            self.destroy_screen(self.full_bottom_f)
        
        self.top_f.grid(row=0,column=0,sticky=N)
        self.line_f.grid(row=1,column=0,sticky=N)
        self.mid_f.grid(row=2,column=0)
        self.info_f.grid(row=3,column=0)
        self.bottom_f.grid(row=4,column=0)


    def forget_homescreen(self):
        self.forget_screen(self.top_f)
        self.forget_screen(self.line_f)
        self.forget_screen(self.mid_f)
        self.forget_screen(self.info_f)
        self.forget_screen(self.bottom_f)


# mainloop
root = Tk()
GUI(root)
root.title("Stock App")
root.resizable(0,0)
root.geometry("1034x646")
root.mainloop()

