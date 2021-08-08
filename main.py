#!/usr/bin/env python
# -*- coding: utf-8 -*- 



from selenium import webdriver
import time, datetime, random, codecs


### need configuration file
i = 0
s = 20
jit = 10
links = ["www.essonne.gouv.fr/booking/create/23014/0"]


dir = "/home/data/"


for link in links :
    view = {'output': dir + "prefecture_" ,
                'width': 1000,
                'height': 800}
    linkWithProtocol = 'https://' + str(link)

firefox_options = webdriver.FirefoxOptions()
firefox_options.set_headless() 


def random_number_gen(n):
    return random.random()*n - n/2

with webdriver.Firefox(firefox_options=firefox_options) as driver:

    while True:

        timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

        
        driver.set_window_size(view['width'], view['height'])
        driver.get(linkWithProtocol)
        time.sleep(s+random_number_gen(jit))

        try:
            condition = driver.find_element_by_id("condition")
            nextButton = driver.find_element_by_name("nextButton")
        except:
            condition = None
            nextButton = None

        if not condition or not nextButton:
            continue

        condition.click()
        nextButton.click()
        time.sleep(s+random_number_gen(jit))


        try :
            guichet_list = driver.find_elements_by_class_name("radio")
            nextButton = driver.find_element_by_name("nextButton")
        except:
            guichet_list = None
            nextButton = None

        if not guichet_list or not nextButton:
            continue

        guichet_list[i].click()
        nextButton.click()
        time.sleep(s+random_number_gen(jit))

        try:
            form = driver.find_elements_by_xpath("//form[@id='FormBookingCreate']")
        except:
            form = None
            
        if not form:
            driver.save_screenshot(view['output'] + timestamp + '.png')
            continue

        if form[0].text == "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement.":
            continue
  
        with codecs.open(view['output'] + timestamp + '.html') as fid:
            fid.write(driver.page_source)

        driver.save_screenshot(view['output'] + timestamp + '.png')

        i = (i+1)%5
