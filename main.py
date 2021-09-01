#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from selenium import webdriver
import time, datetime, random, codecs, os, logging



if os.getenv('ISK8S'):
    dir = "/home/data/"
else:
    dir = "./"


logging.basicConfig(filename=os.path.join(dir,'prefecture-scrapping.log'), level=logging.DEBUG)

### need configuration file
BUFFER_JIT = 2
BUFFER = 15
NTRIAL = 5


def random_number_gen(n):
    return random.random()*n - n/2



class WebCrawler():

    def __init__(self,driver,options):
        self.driver = driver
        self.ntrial = options['NTRIAL']
        self.buffer = options['BUFFER']
        self.jit = options['BUFFER_JIT']
        self.crawlpath = []

    def Main(self):
        while True:
            time.sleep(self.buffer + self.jit)
            self.timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            print(self.timestamp)
            self.Crawl()

    def Crawl(self):

        for interaction in self.crawlpath:
            trial = self.InteractWPage(interaction)
            if trial >= self.ntrial:
                break

    def InteractWPage(self,func):
        logging.info(f"interacting with {func.__name__}")
        isloaded = False
        trial = 0            
        while trial < self.ntrial and not isloaded:
            trial+=1
            time.sleep(self.buffer + self.jit)      
            try:
                isloaded = func()
            except:
                continue
        return trial


class PalaiseauCrawler(WebCrawler):
    def __init__(self,driver,options):
        super().__init__(driver,options)
        self.crawlpath = [self.GetPageZero,self.GetPageOne,self.GetPageTwo,self.GetPageThree,self.GetSnapShot]    


    def GetPageZero(self):
        
        link = 'https://' + "www.essonne.gouv.fr/booking/create/23014/0"
        self.driver.get(link)
        return True

    def GetPageOne(self):
        
        page_1 = "Cliquez la case pour accepter les conditions d'utilisation avant de continuer le processus de prise de rendez-vous."
        condition = self.driver.find_element_by_id("condition")
        nextButton = self.driver.find_element_by_name("nextButton") 

        if not condition.get_attribute("title") == page_1:
            return False

        condition.click()
        nextButton.click()
        return True

    def GetPageTwo(self):
        
        page_2 = "Choix de la nature du rendez-vous"
        i = random.randint(0,4)
        headline = self.driver.find_element_by_id("inner_Booking")
        guichet_list = self.driver.find_elements_by_class_name("radio")
        nextButton = self.driver.find_element_by_name("nextButton")

        if not page_2 in headline.text:
            return False

        guichet_list[i].click()
        nextButton.click()

        return True

    def GetPageThree(self):
        
        page_3 = "Description de la nature du rendez-vous"
        nextButton = self.driver.find_element_by_name("nextButton")
        headline = self.driver.find_element_by_id("inner_Booking")

        if not page_3 in headline.text:
            return False

        nextButton.click()

        return True  

    def GetSnapShot(self):
        
        self.driver.save_screenshot("newwebpage" + self.timestamp + '.png')

        with codecs.open("newwebpage" + self.timestamp + '.html','w+',"utf-8") as fid:
            fid.write(self.driver.page_source)

        return True  

if __name__ == "__main__":


    view = {'output': dir + "prefecture_" ,
                'width': 1000,
                'height': 800}

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_headless() 
    driver = webdriver.Firefox(firefox_options=firefox_options)
    driver.set_window_size(view['width'], view['height'])    

    options = {"NTRIAL" : NTRIAL,
                "BUFFER" : BUFFER,
                "BUFFER_JIT":BUFFER_JIT}


    crawler = PalaiseauCrawler(driver,options)
    crawler.Main()



