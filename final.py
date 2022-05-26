
import requests 
import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time 

driverPath = 'chromedriver.exe'


n = ["iPhone 11", "iPhone 12", "iPhone 13","iPhone SE"]
t_for_n = [3,4,4,1]
m = ["Regular","Pro","Pro Max","Mini"]
mem = ["64GB", "128GB","256GB","512GB","1TB"]

#Starting and finishing indexes for memory options based on name and model 
m_for_mem = [ 
[(0,2),(0,4),(0,4),(0,0)], 
[(0,3),(1,4),(1,4),(0,3)], 
[(1,4),(1,5),(1,5),(1,4)],
[(0,3),(0,0),(0,0),(0,0)]
]
    
def search_apple(n,t,m): 
    #Format the string for search in the url
    name = n.split(" ")
    s = ""
    for i in name: 
        s+=i.lower()+"-"
    s = s[0:len(s)-1]

    #Search Apple 
    url = "https://www.apple.com/tw/shop/buy-iphone/"+s

    if n == "iPhone 13" and (t == "Pro" or t == "Pro Max"): 
        url+="-pro"
    
    #For Iphone 11 and SE, order is color selection->memory->no 
    #For others, order is model -> color selection ->memeory ->no 
    #Select the year
    if (n == "iPhone 11" and t!= "Pro" and t!="Pro Max") or n == "iPhone SE":
        #opens browser to the weather 
        browser = webdriver.Chrome(executable_path = driverPath)
        browser.get(url)
        time.sleep(1)

        select =browser.find_element_by_xpath("//div[@class='rc-dimension-multiple form-selector-swatch column large-6 small-6 form-selector']")
        select.click()
        time.sleep(1)

        mem_p = "//input[@data-autom='dimensionCapacity"+m.lower()+"']"
        select =browser.find_element_by_xpath(mem_p)
        select.click() 
        time.sleep(1)

        select =browser.find_element_by_xpath("//input[@data-autom='choose-noTradeIn']")
        select.click() 
        time.sleep(3)

        price = browser.find_element_by_xpath("//span[@data-autom='full-price']")
        print(price.text)


    elif (n == "iPhone 12" and t!="Pro" and t!= "Pro Max") or (n=="iPhone 13" and t!="Pro" and t!="Pro Max"): 
        #opens browser to the weather 
        browser = webdriver.Chrome(executable_path = driverPath)
        browser.get(url)
        time.sleep(1)

        if t == "Regular": 
            select =browser.find_element_by_xpath("//input[@data-autom='dimensionScreensize6_1inch']")
            select.click() 
            time.sleep(1)
        
        else:  #Mini 
            select =browser.find_element_by_xpath("//input[@data-autom='dimensionScreensize5_4inch']")
            select.click() 
            time.sleep(1)
        
        select =browser.find_element_by_xpath("//div[@class='rc-dimension-multiple form-selector-swatch column large-6 small-6 form-selector']")
        select.click()
        time.sleep(1)

        mem_p = "//input[@data-autom='dimensionCapacity"+m.lower()+"']"
        select =browser.find_element_by_xpath(mem_p)
        select.click() 
        time.sleep(1)

        select =browser.find_element_by_xpath("//input[@data-autom='choose-noTradeIn']")
        select.click() 
        time.sleep(3)

        price = browser.find_element_by_xpath("//span[@data-autom='full-price']")
        print(price.text)
    
    elif n=="iPhone 13" and (t == "Pro" or t=="Pro Max"):
        #opens browser to the weather 
        browser = webdriver.Chrome(executable_path = driverPath)
        browser.get(url)
        time.sleep(1)

        if t == "Pro": 
            select =browser.find_element_by_xpath("//input[@data-autom='dimensionScreensize6_1inch']")
            select.click() 
            time.sleep(1)
        
        else:  #MAX
            select =browser.find_element_by_xpath("//input[@data-autom='dimensionScreensize6_7inch']")
            select.click() 
            time.sleep(1)
        
        select =browser.find_element_by_xpath("//div[@class='rc-dimension-multiple form-selector-swatch column large-6 small-6 form-selector']")
        select.click()
        time.sleep(1)

        mem_p = "//input[@data-autom='dimensionCapacity"+m.lower()+"']"
        select =browser.find_element_by_xpath(mem_p)
        select.click() 
        time.sleep(1)

        select =browser.find_element_by_xpath("//input[@data-autom='choose-noTradeIn']")
        select.click() 
        time.sleep(3)

        price = browser.find_element_by_xpath("//span[@data-autom='full-price']")
        print(price.text)
    else: 
        print("None")

      


def model_select(n):
    num = t_for_n[n-1]
    for i in range(num): 
        print(str(i+1)+"-"+m[i])
    model = int(input())
    while(model<1 or model>num): 
        print("Invalid Number, enter another")
        model = int(input())
    
    return model
    
def memory_select(name,model): 
    name = name - 1 
    model = model - 1
    start,finish = m_for_mem[name][model]
    for i in range(start,finish): 
        print(str(i)+"-"+mem[i]) 
    memory = int(input())
    while(memory<start or memory>=finish): 
        print("Invalid Number, enter another")
        memory = int(input())
    
    return memory

def iphone_select(): 
    print('iPhone Best Price Finder')
    print("Select iPhone") 
    print("1 - iPhone 11")
    print("2 - iPhone 12") 
    print("3 - iPhone 13")
    print("4 - iPhone SE")
    name = int(input())
    while(name<1 or name>4): 
        print("Invalid Number, enter another")
        name = int(input())
    return name 

name = iphone_select()
model = model_select(name)
memory = memory_select(name, model)

name = n[name-1]
model = m[model-1]
memory = mem[memory]
print(name+" "+model+" "+memory)



search_apple(name,model,memory)







# #opens browser to the weather website
# browser.get(url)
# time.sleep(1)

# #requests the page and then extracts the div of the titles 
# html = requests.get(url) 
# html.encoding="utf-8"
# sp = bs(html.text, 'html.parser')
# a0 = sp.find_all("div",class_= "cbp-item")