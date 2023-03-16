#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from selenium import webdriver
import time, datetime, random, codecs, os, logging
from WebCrawler import WebCrawler


if os.getenv('ISK8S'):
    dir = "/home/data/"
else:
    dir = "./"


logging.basicConfig(filename=os.path.join(dir,'prefecture-scrapping.log'), level=logging.DEBUG)

### need configuration file
BUFFER_JIT = 30
BUFFER = 60
NTRIAL = 5


def random_number_gen(n):
    return random.random()*n - n/2



class PalaiseauCrawler(WebCrawler):
    def __init__(self,driver,options):
        super().__init__(driver,options)
        self.crawlpath = [self.GetPageZero,self.GetPageOne,self.GetPageTwo,self.GetPageThree,self.GetSnapShot]  
          
        self.logging = logging
        self.logging.basicConfig(filename=f"{dir}palaiseau_log.txt",level=logging.INFO)
        self.logging = logging.getLogger("palaiseau_scrapper")

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
        i = random.randint(0,1)
        headline = self.driver.find_element_by_id("inner_Booking")
        guichet_list = self.driver.find_elements_by_class_name("radio")
        nextButton = self.driver.find_element_by_name("nextButton")

        if not page_2 in headline.text:
            return False

        guichet_list[i].click()
        nextButton.click()

        return True

    def GetPageThree(self):


        headline = self.driver.find_element_by_id("FormBookingCreate")
        page_3 = "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement."



        if page_3 == headline.text:
            print(headline.text)
            return False

        self.driver.save_screenshot(dir + "page3_" + self.timestamp + '.png')

        with codecs.open(dir + "page3_" + self.timestamp + '.html','w+',"utf-8") as fid:
            fid.write(self.driver.page_source)

        page_3 = "Description de la nature du rendez-vous"
        nextButton = self.driver.find_element_by_name("nextButton")
        headline = self.driver.find_element_by_id("inner_Booking")



        if not page_3 in headline.text:
            return False


        nextButton.click()

        return True  

    def GetSnapShot(self):
        
        self.driver.save_screenshot(dir + "newwebpage" + self.timestamp + '.png')

        with codecs.open(dir + "newwebpage" + self.timestamp + '.html','w+',"utf-8") as fid:
            fid.write(self.driver.page_source)

        ### send email to address

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

