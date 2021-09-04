import string
import pymongo
from os import path,getenv
import yfinance as yf
from json import dumps
from time import sleep
import logging
from WebCrawler import WebCrawler



if getenv('ISK8S'):
    dir = "/home/data/"
else:
    dir = "./"


### need configuration file
BUFFER_JIT = 0
BUFFER = 1
NTRIAL = 5


class combination_generator():

    def __init__(self,n_char=0):

        self.old_state = 0
        self.tmp_state = f"{dir}old_state.txt"
        if path.exists(self.tmp_state):
            with open(self.tmp_state,"r") as fid:
                self.old_state = int(fid.read())
        
        print(self.old_state)
        self.char_space = f"{string.digits}{string.ascii_uppercase}{string.punctuation}"
        self.char_space_length = len(self.char_space)
        self.limit = pow(self.char_space_length,n_char)
        self.index_gen = (i for i in range(self.old_state,self.limit))
        
        self.save_rate = 1

    def __toList__(self,n):
        if n < self.char_space_length:
            return self.char_space[n]

        else:
            return self.__toList__(n//self.char_space_length) + self.char_space[n%self.char_space_length] 


    def create_all_combination(self,n):

        symbol_list = [self.__toList__(i) for i in self.index_gen]
    
        return symbol_list

    
    def next_combination(self):

        self.old_state = self.index_gen.__next__()
        
        if self.old_state%self.save_rate == 0:
            with open(self.tmp_state,"w+") as fid:
                fid.write(str(self.old_state))

        return self.__toList__(self.old_state)

    def get_limit(self):
        return self.limit

    def get_state(self):
        return self.old_state


class YahooMongoDb():

    def __init__(self,config_file):

        config_file =  f"{dir}yahoo_config_file.txt"

        with open(config_file) as fid:
            url = fid.read()

        self.mongoclient = self.pymongo.MongoClient(url)   
        actual_db = self.mongoclient.list_database_names()
        mydb = self.mongoclient["yahoo"]
        self.mycol = mydb["symbols"]

        if "yahoo" not in actual_db:
            self.mydb.mycol.create_index('index')

    def insert(self,data):
        return self.mycol.insert_one(data)

class YahooCrawler(WebCrawler):

    def __init__(self,driver,options):
        super().__init__(driver,options)
        self.crawlpath = [self.GenerateStockSymbol,self.GetSymbol]        

        self.logging = logging
        self.logging.basicConfig(filename=f"{dir}yahoo_log.txt",level=logging.INFO)
        self.logging = logging.getLogger("yahoo_scrapper")

        self.combination_generator = combination_generator(10)

    def GenerateStockSymbol(self):  
        self.ticker_name = self.combination_generator.next_combination()
        return True


    def GetSymbol(self):
        
        ticker = self.driver.Ticker(self.ticker_name)
        data = {"index":self.ticker_name,"data" : ticker.info}
        with open(f"{dir}yahoo_response.txt",'a') as fid:
            fid.write(f"{dumps(data)}\n")

        # if not page_3 in headline.text:
        #     return False


        return True


if __name__ == "__main__":

    
    options = {"NTRIAL" : NTRIAL,
                "BUFFER" : BUFFER,
                "BUFFER_JIT":BUFFER_JIT}    



    crawler = YahooCrawler(yf,options)
    crawler.Main()    

    rate = 1.8

    for i in range(cg.get_state(),cg.get_limit()):

        ticker_name = cg.next_combination()
        trial = 0
        while trial < 5:
            try:
                ticker = yf.Ticker(ticker_name)
                doc = dumps(ticker.info)
                print(ticker.info)
                if len(doc)>44:
                    print(mycol.insert_one(ticker.info))
                break
            except:
                trial=+1
            sleep(3)
            
        if trial == 5:
            logger.warning(f'{ticker_name} could not be fetch into the database')


        sleep(rate)
