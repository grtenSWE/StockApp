import os
from PIL import Image,ImageTk
import json
from Stock_Class.Stock_Class import Stocks
from threading import Timer




class Data:  
    def __init__(self):
        #The method listdir() returns a list containing the names of the entries in the directory given by path.
        self.list_of_files = os.listdir() 
        self.ALL_STOCKS = Stocks()

    def username_verify(self,username,password):
        value = ""

        if "{}.json".format(username) in self.list_of_files:
            with open("{}.json".format(username), "r") as file:   # open the file in read mode
                verify = json.load(file)
             
            if password == verify["Password"]:
                value = "success"
                t = Timer(0.1,lambda user=username: self.create(user))
                t.start()
            else:
                value = "The password is incorrect"
        else:
            value = "This user doesn't exist"

        return value

    def create(self,user):
        self.ALL_STOCKS.create_watch_list(user)

    def create_verify(self,username,password,password_conf):
        value = ""
        upper_case = [l for l in password if l.isupper()]

        if "{}.json".format(username) in self.list_of_files:
           value = "This username already exist"

        elif username != " Enter your username" and password != " Enter your password" and password_conf != " Confirm your password":
            
            if password != password_conf:
                value = "Please fill out the same password in both entry box"

            elif len(password) < 8:
                value = "Only {} characters are entered. Ensure password has at least 8 characters".format(len(password))

            elif len(password) > 16:
                value = "{} characters are entered. Ensure password has less than 16 characters".format(len(password))

            elif password.isalpha() == True:
                value = "Please make sure your password has atleast 1 number"

            elif len(upper_case) == 0:
                value = "Please make sure your password has atleast 1 upper case letter"

            else:
                value = "success"
                entry = {'Username': username,'Password':password,'Watch_list':[]}

                with open("{}.json".format(username), "w") as file:
                    json.dump(entry, file)
        else:
            value = "Please fill out all entry boxes"

        return value

    #appends the existing watchlist into a list for that list to be modify
    def watchlist_get(self,username):
        self.stocks_info =[]

        with open("{}.json".format(username), "r") as file:   
            user_data = json.load(file)
            for i in user_data["Watch_list"]:
                self.stocks_info.append(i)

        return self.stocks_info
        

    def watchlist_save(self,username,password,watchlist):
        entry = {'Username': username,'Password':password,'Watch_list':watchlist}
        with open("{}.json".format(username), "w") as file:
            json.dump(entry, file)


    def getImage(self, filepath, resize, crop = 0):
        """returns an image """
        IMG = Image.open(filepath)
        try:
            image = IMG.crop((crop))
            image = ImageTk.PhotoImage(image.resize(resize))
        except:
            image = ImageTk.PhotoImage(IMG.resize(resize))
    
        return image

    def catergories_functionmap(self,method):
       
        map = {
        'tech': self.ALL_STOCKS.tech_get, 'energy': self.ALL_STOCKS.energy_get, 'pharma': self.ALL_STOCKS.pharma_get, 'finance': self.ALL_STOCKS.finance_get, 'auto': self.ALL_STOCKS.auto_get, 'retail': self.ALL_STOCKS.retail_get, 'watch_list': self.ALL_STOCKS.watch_list_get
        }
        value = map[method]
        return value
    
    def timelines_keys(self):
        return ["7D","1mo","3mo","YTD","1Y","2Y","10Y","max"]

    def info_keys(self,allcards_info):
        return ["P/E","Vol","Avg. Vol",allcards_info[0],allcards_info[1],allcards_info[2]]
       
        








  