#Tyler Eck 
#410821337 
#Data Science Final Project
#TheRightiPhone

from concurrent.futures import BrokenExecutor
import requests 
import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time 
from selenium.webdriver.common.keys import Keys

driverPath = 'chromedriver.exe'

location = [] 
prices = [] 
link = []
name_on_web = [] 


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

def get_real_lists(n,p,l,name,model,memory): 
    names = [] 
    price = []
    links = []
    memory =str(int(memory[:len(memory)-2]))  #Take out "GB"

    if model != "Regular": 
        for i in range(len(n)): 
            if name in n[i] and model in n[i] and memory in n[i]: #checks if name, model,and memory are in the title 
                if model == "Pro": #filers out the pro max 
                    if "Max" not in n[i] and "max" not in n[i] and "MAX" not in n[i]:
                        names.append(n[i])
                        price.append(p[i])
                        links.append(l[i])
                else:
                    names.append(n[i])
                    price.append(p[i])
                    links.append(l[i]) 


    else:
        #list of values that should NOT be in the title if its Regular
        #I tried to consider all forms of the words, but there is a little room for error -NOTED FOR SUBMISSION
        nots = ["Pro", "pro","PRO","Pro Max","pro Max", "Pro max", "pro max","PRO MAX", "Mini","mini", "MINI"]
        for i in range(len(n)): 
            if name in n[i] and memory in n[i]: #checks if name, model,and memory are in the title 
                flag = 1
                for j in nots: 
                    if j in n[i]: #if any of the words are in n[i] then we WILL NOT ADD to list
                        flag = 0
                        break
                if flag: 
                    names.append(n[i])
                    price.append(p[i])
                    links.append(l[i]) 

    return names,price,links

def fix_price(p): 
    num ="1234567890" 
    l = ""
    for i in range(len(p)):
        if p[i] in num:
            l+=p[i]
    
    return int(l)


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
        url = browser.current_url
        
        p = fix_price(price.text) 

        prices.append(p)

        link.append(url)
        location.append("Apple")

        if t == "Regular": #without any addition 
            keyword = n+" "+m
        else:  #needs to include the model 
            keyword = n+" "+t+" "+m

        name_on_web.append(keyword)


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
        url = browser.current_url
        
        p = fix_price(price.text) 

        prices.append(p)
        link.append(url)
        location.append("Apple")

        if t == "Regular": #without any addition 
            keyword = n+" "+m
        else:  #needs to include the model 
            keyword = n+" "+t+" "+m

        name_on_web.append(keyword)
    
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

        #Extract the Price and URL 
        price = browser.find_element_by_xpath("//span[@data-autom='full-price']")
        url = browser.current_url
        
        p = fix_price(price.text) 

        prices.append(p)
        link.append(url)
        location.append("Apple")
        
        if t == "Regular": #without any addition 
            keyword = n+" "+m
        else:  #needs to include the model 
            keyword = n+" "+t+" "+m

        name_on_web.append(keyword)

    else: 
        print("None")

def search_pchome(name,model,memory): 

    #Search PCHome
    url = "https://shopping.pchome.com.tw/"

    #opens browser to the weather 
    browser = webdriver.Chrome(executable_path = driverPath)
    browser.get(url)
    time.sleep(1)

    t_mem = memory 
    if memory != "1TB": #for TB we leave the "TB" at the end 
        t_mem = memory[0:len(memory)-2] #formats memory to leave out "gb" to get more results in search
    if model == "Regular": #without any addition 
        keyword = name+" "+t_mem
    else:  #needs to include the model 
        keyword = name+" "+model+" "+t_mem


    inputElement = browser.find_element_by_id("keyword")
    inputElement.send_keys(keyword) 
    select = browser.find_element_by_xpath("//span[@class='ico ico_search']")
    select.click() 
    time.sleep(4)

    #Page dynamically generates items from search as you scroll down more. Therefore
    #I will need to scroll all the way to the bottom of the page before crawling occurs


    SCROLL_PAUSE_TIME = 0.5
    # used to get scroll height 
    p_h = browser.execute_script("return document.body.scrollHeight") #previous height of document 

    while True:
        #scrolls down by "height" amount (one entire height)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #time to load the newly generated items on the page
        time.sleep(SCROLL_PAUSE_TIME)

        #get the new height 
        n_h= browser.execute_script("return document.body.scrollHeight") #CURRENT height of document 
        
        if n_h == p_h: #if we reach the bottom then we stop 
            break
        p_h = n_h #let previous height equal new height (continously scrolls until we hit bottom)

        
    url = browser.current_url

    names = browser.find_elements_by_xpath("//h5[@class='prod_name']")
    price_l = browser.find_elements_by_xpath("//ul[@class='price_box']")
    links = browser.find_elements_by_css_selector(".prod_name [href]")
    
    str_names = [i.text for i in names]
    str_prices = [i.text for i in price_l] 
    links = [l.get_attribute('href') for l in links]

    P_L = [] 
    for i in str_prices:
        P_L.append(fix_price(i))
    

    
    time.sleep(4)

    #The filtering on PChome is not so great, therefore I will need to manually check 
    #items in order to see if it matches with requested iphone specs
    real_names, real_prices,real_links = get_real_lists(str_names,P_L,links,name,model,memory)


    for i in range(len(real_names)):
        name_on_web.append(real_names[i])
        prices.append(real_prices[i])
        link.append(real_links[i])
        location.append("PCHome")


def search_studioA(name,model,memory): 
    
    #search Studio A - short iphone section because it is limited
    url = "https://www.studioa.com.tw/categories/iphone?sort_by=lowest_price&order_by=desc"

    #opens browser to the weather 
    browser = webdriver.Chrome(executable_path = driverPath)
    browser.get(url)
    time.sleep(4)

    names = browser.find_elements_by_xpath("//div[@class='title text-primary-color title-container ellipsis ']")
    price_l = browser.find_elements_by_xpath("//div[@class='quick-cart-price']")
    links = browser.find_elements_by_xpath("//a[@class='quick-cart-item']")
    

    str_names = [i.text for i in names]
    links = [l.get_attribute('href') for l in links]

    #SOME ITEMS have a sale price and some just have a regular price, therefore
    #I need to get the smaller prices for the two prices recieved 
    price_real = [] 
    for i in range(len(names)):
        l= price_l[i].text
        l = l.split("\n")
        if len(l) == 2: 
            price_real.append(fix_price(l[1]))
        else: 
            price_real.append(fix_price(l[0]))
    
    #The filtering on Studio A includes extra data, therefore I will need to manually check 
    #items in order to see if it matches with requested iphone specs
    real_names, real_prices,real_links = get_real_lists(str_names,price_real,links,name,model,memory)


    for i in range(len(real_names)):
        name_on_web.append(real_names[i])
        prices.append(real_prices[i])
        link.append(real_links[i])
        location.append("Studio A")
    
        

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
search_pchome(name,model, memory)
search_studioA(name,model,memory)



dict = { 
    "Name on Web":name_on_web,
    "Location":location, 
    "Price":prices,
    "Link":link
}

df = pd.DataFrame(dict) 

df = df.sort_values(by=['Price'])
df2 = df.reset_index(drop=True)
print(df2)

