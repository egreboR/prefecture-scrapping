#!/usr/bin/env python
# -*- coding: utf-8 -*- 



from selenium import webdriver
import time, datetime, random, codecs


### need configuration file
i = 0
jit_s = 2
s = 15
jit_l = 10
l = 30
links = ["www.essonne.gouv.fr/booking/create/23014/0"]
NTRIAL = 5

dir = "/home/data/"
# dir = "./"

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

    timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

    driver.set_window_size(view['width'], view['height'])
    driver.get(linkWithProtocol)
    time.sleep(l+random_number_gen(jit_l))
    page_1 = "Cliquez la case pour accepter les conditions d'utilisation avant de continuer le processus de prise de rendez-vous."
    page_2 = "Choix de la nature du rendez-vous"

    while True:



        timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        print(timestamp)

        time.sleep(l+random_number_gen(jit_l))
        driver.set_window_size(view['width'], view['height'])
        try:
            driver.get(linkWithProtocol)
        except:
            continue

        time.sleep(l+random_number_gen(jit_l))
        ### test if we are in the page

        isloaded = False
        trial = 0
        while trial < NTRIAL :

            trial+=1
            time.sleep(s+random_number_gen(jit_s))
            try:
                condition = driver.find_element_by_id("condition")
                nextButton = driver.find_element_by_name("nextButton")
            except:
                if not isloaded:
                    condition = None
                    nextButton = None
                    continue
                break

            if not condition and not nextButton:
                if not isloaded:
                    continue
                break

            if not condition.get_attribute("title") == page_1:
                if not isloaded:
                    continue
                break

            try:
                condition.click()
                nextButton.click()
                isloaded = True
            except:
                driver.save_screenshot(view["output"] + "page_01_error_01" + timestamp + '.png')
                

        if trial >= NTRIAL:
            driver.save_screenshot(view["output"] + "page_01_error_02" + timestamp + '.png')
            continue

        isloaded = False
        trial = 0
        while trial < NTRIAL :

            trial+=1
            time.sleep(s+random_number_gen(jit_s))
            try:
                headline = driver.find_element_by_id("inner_Booking")
                guichet_list = driver.find_elements_by_class_name("radio")
                nextButton = driver.find_element_by_name("nextButton")
            except:
                if not isloaded:
                    headline = None
                    guichet_list = None
                    nextButton = None
                    continue
                break

            if not guichet_list or not nextButton or not headline :
                if not isloaded:
                    continue
                break

            if not  page_2 in headline.text:
                if not isloaded:
                    continue
                break             

            try:
                guichet_list[i].click()
                nextButton.click()
                isloaded=True
            except:
                driver.save_screenshot(view["output"] + "page_02_error_01" + timestamp + '.png')
                
        if trial >= NTRIAL:
            driver.save_screenshot(view["output"] + "page_02_error_02" + timestamp + '.png')
            continue
            



        try:
            form = driver.find_elements_by_xpath("//form[@id='FormBookingCreate']")
        except:
            form = None

        if not form:
            driver.save_screenshot(view["output"] + "newwebpagewithoutform" + timestamp + '.png')
            with codecs.open(view["output"] + "newwebpagewithoutform" + timestamp + '.html','w+',"utf-8") as fid:
                fid.write(driver.page_source)
            continue


        if form[0].text == "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement.":
            continue
  
        driver.save_screenshot(view["output"] + "newwebpagewithform" + timestamp + '.png')

        with codecs.open(view["output"] + "newwebpagewithform" + timestamp + '.html','w+',"utf-8") as fid:
            fid.write(driver.page_source)

        i = (i+1)%5
