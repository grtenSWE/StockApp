import yfinance as yf
from plotly.graph_objects import Layout
import plotly.graph_objects as go
from numerize import numerize
import json
from datetime import date


class Stocks:
    """a data class that compiles the information of each stocks"""
    def __init__(self):
        # all stocks 
        STOCKS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA","META","ORCL","NVDA",
        "XOM","CVX","SHEL","TTE","2222.SR","COP","EQNR","BP","DUK","EOG",
        "JNJ","LLY","PFE","ABBV","NVO","MRK","AZN","NVS","BMY","CVS",
        "V","JPM","MA","BAC","WFC","MS","SCHW","RY","AXP","GS",
        "TM","002594.SZ","VOW3.DE","MBG.DE","F","GM","BMW.DE","HMC","RACE",
        "WMT","HD","BABA","COST","LOW","JD","TGT","TJX"]
        today = str(date.today())
        self.hum_num = numerize.numerize
        self.KEYS = ['shortName','currentPrice','marketCap','regularMarketVolume']
        self.watch_list_keys = ['symbol','shortName','currentPrice','dayChange','weekChange','marketCap','regularMarketVolume']
        self.user_stocks = []

        with open("{}.json".format("stocks_data"), "r") as file:
            data = json.load(file)
            if today == data["Date"]:
                   # categorised menus
                self.tech_page = data["Tech"]
                self.energy_page = data["Energy"]
                self.pharma_page = data["Pharma"]
                self.finance_page = data["Finance"]
                self.auto_page = data["Auto"]
                self.retail_page = data["Retail"]
            else:
                self.new_data(STOCKS,today)
    

    def new_data(self,STOCKS,today):
        
        funde_info = {}
        final_info ={}
        for ticker in STOCKS:
            ticker_obj = yf.Ticker(ticker)
            new_key = f"{ticker}_symbol"
            funde_info[new_key] = ticker
            #print(ticker)
            
         
            for key in self.KEYS:
                stock_info = ticker_obj.info[key]
                
                new_key = "{}_{}".format(ticker,key)
                if key == "currentPrice": 
                    dChange = self.get_daychange(ticker_obj,stock_info)
                    wChange = self.get_weekchange(ticker_obj,stock_info)
                    new_key_d = "{}_dayChange".format(ticker)
                    new_key_w = "{}_weekChange".format(ticker)
                    funde_info[new_key_d] = dChange
                    funde_info[new_key_w] = wChange
                    funde_info[new_key] = format(stock_info,".2f")
                    
                elif type(stock_info) == int or type(stock_info) == float:
                    funde_info[new_key] = self.hum_num(stock_info)
                elif key == "shortName":
                    if stock_info.isupper() == False: 
                        if len(stock_info) > 24:
                            stock_info = stock_info[:24]
                            funde_info[new_key] = f"{stock_info}..."
                        else:
                            funde_info[new_key] = stock_info
                    elif len(stock_info) > 18:
                        stock_info = stock_info[:18]
                        funde_info[new_key] = f"{stock_info}..."
                    else:
                        funde_info[new_key] = stock_info
                else:
                    funde_info[new_key] = stock_info
       
        for ticker in STOCKS:
            each_stock_info = []
            for key in self.watch_list_keys:
                new_info = funde_info[f"{ticker}_{key}"]
                each_stock_info.append(new_info)
            final_info[ticker] =  each_stock_info

        # categorised menus
        self.tech_page = [final_info['AAPL'], final_info['MSFT'], final_info['GOOG'], final_info['AMZN'], final_info['TSLA'], final_info['META'], final_info['V'], final_info['ORCL'], final_info['NVDA'], final_info['BABA']]
        self.energy_page = [final_info['XOM'], final_info['CVX'], final_info['SHEL'], final_info['TTE'], final_info["2222.SR"], final_info['COP'], final_info['EQNR'], final_info['BP'], final_info['EOG'], final_info['DUK']]
        self.pharma_page = [final_info['JNJ'], final_info['LLY'], final_info['PFE'], final_info['ABBV'], final_info['NVO'], final_info['MRK'], final_info['AZN'], final_info['NVS'], final_info['BMY'], final_info['CVS']]
        self.finance_page = [final_info['V'], final_info['JPM'], final_info['MA'], final_info['BAC'], final_info['WFC'], final_info['MS'], final_info['SCHW'], final_info['RY'], final_info['AXP'], final_info['GS']]
        self.auto_page = [final_info['TSLA'], final_info['TM'],final_info['002594.SZ'], final_info['VOW3.DE'], final_info['MBG.DE'], final_info['F'], final_info['GM'], final_info['BMW.DE'], final_info['HMC'], final_info['RACE']]
        self.retail_page = [final_info['AMZN'], final_info['WMT'], final_info['HD'], final_info['BABA'], final_info['COST'], final_info['CVS'], final_info['LOW'], final_info['JD'], final_info['TGT'], final_info['TJX']]

        entry = {'Date': today,'Tech':self.tech_page,'Energy':self.energy_page,'Pharma':self.pharma_page,'Finance':self.finance_page,'Auto':self.auto_page,'Retail':self.retail_page}
        with open("{}.json".format("stocks_data"), "w") as file:
            json.dump(entry, file)
            
     
    # categorised menu returning methods
    def tech_get(self):
        return self.tech_page.copy()

    def energy_get(self):
        return self.energy_page.copy()

    def pharma_get(self):
        return self.pharma_page.copy()

    def finance_get(self):
        return self.finance_page.copy()

    def auto_get(self):
        return self.auto_page.copy()

    def retail_get(self):
        return self.retail_page.copy()

    def watch_list_get(self):
        return self.watch_list.copy()

    def get_weekchange(self,ticker_obj,current_price):
        infod = []
        hist = ticker_obj.history(period='1wk')

        for i in hist['Open']:
            infod.append(i)

        weekchange = 100 * (1 - (infod[0]/current_price))
        return format(weekchange,".2f") 
        
        
    def get_daychange(self,ticker_obj,current_price):
        daychange = 100 * (1 - (ticker_obj.info['previousClose']/current_price))
        return format(daychange,".2f")

    def stock_search_get(self,ticker):
        ticker = ticker.upper()
        ticker_obj = yf.Ticker(ticker)
        stock_search_data = []
        stock_search_data.append(ticker)
        stock_search_data.append(ticker_obj.info['shortName'])

        return stock_search_data
          

    def create_watch_list(self,username):
        watch_list_dict = {}
        self.watch_list = []
        self.user_stocks= []

        with open("{}.json".format(username), "r") as file:   # open the file in read mode
            user_file = json.load(file)
            self.user_stocks.append(user_file["Watch_list"])
        
        for list in self.user_stocks:
            for ticker in list:
                ticker_obj = yf.Ticker(ticker)
                new_key = f"{ticker}_symbol"
                watch_list_dict[new_key] = ticker

                for key in self.KEYS:
                    stock_info = ticker_obj.info[key]
                    new_key = "{}_{}".format(ticker,key)
                    if key == "currentPrice": 
                        wChange = self.get_weekchange(ticker_obj,stock_info)
                        new_key_w = "{}_weekChange".format(ticker)
                        watch_list_dict[new_key_w] = wChange

                        watch_list_dict[new_key] = format(stock_info,".2f")
                    elif type(stock_info) == int or type(stock_info) == float:
                        watch_list_dict[new_key] = self.hum_num(stock_info)


                    elif key == "shortName":
                        #limiting the amount of characters for Shortnames
                        if len(stock_info) > 24:
                            stock_info = stock_info[:24]
                            watch_list_dict[new_key]  = f"{stock_info}..."
                        else:
                            watch_list_dict[new_key]  = stock_info
                    else:
                        watch_list_dict[new_key] = stock_info
     

        for list in self.user_stocks:
            for ticker in list:
                each_stock_info = []
                for key in self.watch_list_keys:
                    new_info = watch_list_dict[f"{ticker}_{key}"]
                    each_stock_info.append(new_info)
                self.watch_list.append(each_stock_info)


    def info_get(self,ticker):
        additional_info = []
        volume_d = []

        self.ticker_info = yf.Ticker(ticker)
        vol = self.ticker_info.history(period='1d')

        for i in vol['Volume']:
            volume_d.append(i)
       
        try:
            dividend = self.ticker_info.info['trailingAnnualDividendYield'] * 100
            dividend = format(dividend,".2f")
        except:
            dividend = "0.00"

        try:
            pe = format(self.ticker_info.info['trailingPE'],".2f")
        except:
            pe = format(int(self.ticker_info.info['forwardPE']),".2f")

        additional_info.append(dividend)
        additional_info.append(pe)
        additional_info.append(self.hum_num(volume_d[0]))

        return additional_info

    def graph_get(self,timeframe):
        range = []

        name = "current_graph.png"
        hist = self.ticker_info.history(period=timeframe)

        for price in hist['Close']:
            range.append(price)

        if range[0] < range[-1]:
            chart_color = "#35C759"
        else:
            chart_color = "#D10000"


        layout = Layout(plot_bgcolor='white')
        fig = go.Figure(layout=layout,data= go.Scatter(x=hist.index,y=hist['Close'], mode='lines',line=dict(color=chart_color)))
        # Change grid color and axis colors
        fig.update_xaxes(showline=True, linewidth=2, linecolor='grey', gridcolor='grey')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='grey', gridcolor='grey')
        fig.write_image(name)


                
                
