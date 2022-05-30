#Tyler Eck 
#410821337 
#Data Science Final Project
#TheRightiPhone


#TKINTER 
from ast import Mod
from ctypes import resize
from operator import mod
from telnetlib import IP
import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import messagebox
import threading
from PIL import Image,ImageTk

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

SEARCH_NAME = ""
SEARCH_MODEL = "" 
SEARCH_STORAGE = ""


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
    MODELS = []
    num = t_for_n[n-1]
    for i in range(num): 
        MODELS.append(m[i])
    return MODELS
    
def memory_select(name,model): 
    name = name - 1 
    model = model - 1
    start,finish = m_for_mem[name][model]
    STORAGE = [] 
    for i in range(start,finish): 
        STORAGE.append(mem[i])
    return STORAGE

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

#resizing the image so they are all the same size (smaller)
def resize_image(loc,w,h): 
    iphone = Image.open(loc)
    iphone = iphone.resize((w,h))
    img = ImageTk.PhotoImage(iphone)
    return img 

#When the specific image is hovered over, the image size will change to a larger size 
def hovered_over(e,imgname, but,locx,locy,hovx,hovy):
    bigger_img = resize_image('Pictures/'+imgname+'.png',hovx,hovy)
    but.config(image = bigger_img)
    but.image = bigger_img
    but.place(x=locx, y = locy)

#When cursor is not over the image, the image size will change back to normal 
def not_hovered_over(e,imgname, but,locx,locy,hovx,hovy):
    normal_img = resize_image('Pictures/'+imgname+'.png',hovx,hovy)
    but.config(image = normal_img)
    but.image = normal_img
    but.place(x=locx, y = locy) 

def go_to_model(name):
    global SEARCH_NAME
    show_frame(ModelSelection)
    if name == 1: 
        show_frame(iPhone11_MODEL_FRAME)
        SEARCH_NAME = n[0]
        print(SEARCH_NAME)
    elif name == 2:
        show_frame(iPhone12_MODEL_FRAME)
        SEARCH_NAME = n[1]
        print(SEARCH_NAME)
    elif name == 3:
        show_frame(iPhone13_MODEL_FRAME)
        SEARCH_NAME = n[2]
        print(SEARCH_NAME)
    elif name == 4:
        show_frame(iPhoneSE_MODEL_FRAME)
        SEARCH_NAME = n[3]
        print(SEARCH_NAME)

def go_to_storage(SEL_MODEL, s):
    show_frame(StorageSelection)

    global SEARCH_NAME
    global SEARCH_MODEL
    SEARCH_MODEL = m[SEL_MODEL-1]
    model = SEL_MODEL-1
    name = n.index(SEARCH_NAME) 
    start,finish = m_for_mem[name][model]
    print(start,finish)
    MEMORY = [] 
    for i in range(start, finish): 
        MEMORY.append(mem[i])
    
    print(SEARCH_NAME+SEARCH_MODEL)
    print(MEMORY)
    
    if s == 1: #(0,2)
        show_frame(MEMPG1)
    
    elif s == 2: #(0,3)
        show_frame(MEMPG2)
    
    elif s == 3: #(0,4) 
        show_frame(MEMPG3)
    
    elif s == 4: #(1,4) 
        show_frame(MEMPG4)
    
    elif s == 5: #(1,5)
        show_frame(MEMPG5)

def search(l): 
    global SEARCH_NAME
    global SEARCH_MODEL
    print(SEARCH_NAME+" "+ SEARCH_MODEL+" "+str(l))

#Function to switch between frames 
def show_frame(frame): 
    frame.tkraise()

#MAINN
# name = iphone_select()
# model = model_select(name)
# memory = memory_select(name, model)

# name = n[name-1]
# model = m[model-1]
# memory = mem[memory]
# print(name+" "+model+" "+memory)



# search_apple(name,model,memory)
# search_pchome(name,model, memory)
# search_studioA(name,model,memory)



# dict = { 
#     "Name on Web":name_on_web,
#     "Location":location, 
#     "Price":prices,
#     "Link":link
# }

# df = pd.DataFrame(dict) 

# df = df.sort_values(by=['Price'])
# df2 = df.reset_index(drop=True)
# print(df2)

#GUI Specifications and Setup 
root = tk.Tk()
root.title('The Right iPhone')

window_height = 700
window_width = 1200

#Window and Design Setup 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
style = ttk.Style(root)
root.tk.call('source', 'GUI_Design/azure dark.tcl')
style.theme_use('azure')



# Importing the Pictures used in the program as visual aid and resizing them to be the same size
TITLE = resize_image('Pictures/TITLE.png',1200,90)
iPhone11 = resize_image('Pictures/iPhone11.png',250,350)
iPhone12 = resize_image('Pictures/iPhone12.png',250,350)
iPhone13 = resize_image('Pictures/iPhone13.png',250,350)
iPhoneSE = resize_image('Pictures/iPhoneSE.png',250,350)

iPhone11_Regular = resize_image('Pictures/iPhone11_Regular.png',250,350)
iPhone11_Pro = resize_image('Pictures/iPhone11_Pro.png',250,350)
iPhone11_Pro_Max = resize_image('Pictures/iPhone11_Pro_Max.png',280,380)

iPhone12_Regular = resize_image('Pictures/iPhone12_Regular.png',250,350)
iPhone12_Pro = resize_image('Pictures/iPhone12_Pro.png',250,350)
iPhone12_Pro_Max = resize_image('Pictures/iPhone12_Pro_Max.png',270,370)
iPhone12_Mini = resize_image('Pictures/iPhone12_Mini.png',220,320)

iPhone13_Regular = resize_image('Pictures/iPhone13_Regular.png',250,350)
iPhone13_Pro = resize_image('Pictures/iPhone13_Pro.png',250,350)
iPhone13_Pro_Max = resize_image('Pictures/iPhone13_Pro_Max.png',280,380)
iPhone13_Mini = resize_image('Pictures/iPhone13_Mini.png',220,320)

iPhoneSE_Regular = resize_image('Pictures/iPhoneSE_Regular.png',250,350)

mem1 = resize_image('Pictures/64GB.png',250,350)
mem2 = resize_image('Pictures/128GB.png',250,350)
mem3 = resize_image('Pictures/256GB.png',250,350)
mem4 = resize_image('Pictures/512GB.png',250,350)
mem5 = resize_image('Pictures/1TB.png',250,350)

#Making the different screens so that we can go through selections 

#FRAME 1 - IPHONE SELECTION PAGE
iPhoneSelection = tk.Frame(root,width = 1200, height = 700)
iPhoneSelection.place(x = 0, y = 0)


TITLE = tk.Label(iPhoneSelection, image = TITLE) 
TITLE.place(x = 0, y = 0)

#FRAME 2 - MODEL SELECTION PAGE
ModelSelection = tk.Frame(root,width = 1200, height = 700)
ModelSelection.place(x = 0, y = 0)

#FRAME 3 - STORAGE SELECTION PAGE
StorageSelection = tk.Frame(root,width = 1200, height = 700)
StorageSelection.place(x = 0, y = 0)

#when we start the program, the iPhoneSelection Screen should show first
show_frame(iPhoneSelection)


###################### FIRST PAGE - IPHONE SELECTION SCREEN ########################

#Frames for each iphone 
ip11 = tk.Frame(iPhoneSelection, width = 300, height = 600)
ip12 = tk.Frame(iPhoneSelection, width = 300, height = 600)
ip13 = tk.Frame(iPhoneSelection, width = 300, height = 600)
ipse = tk.Frame(iPhoneSelection, width = 300, height = 600)
ip11.place(x = 0, y = 110)
ip12.place(x = 300, y = 110)
ip13.place(x = 600, y = 110)
ipse.place(x = 900, y = 110)

#Placing the images in their respective frames and binding the hovering option to them 
iphone11 = tk.Button(ip11, image = iPhone11, command = lambda:go_to_model(1)) 
iphone11.place(x = 20, y = 60)
iphone11.bind("<Enter>",lambda event: hovered_over(event, "iPhone11", iphone11,10,50,280,380)) 
iphone11.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone11", iphone11,20,60,250,350))

iphone12 = tk.Button(ip12, image = iPhone12, command = lambda:go_to_model(2)) 
iphone12.place(x = 20, y = 60)
iphone12.bind("<Enter>",lambda event: hovered_over(event, "iPhone12", iphone12,10,50,280,380)) 
iphone12.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12", iphone12,20,60,250,350))

iphone13 = tk.Button(ip13, image = iPhone13, command = lambda:go_to_model(3)) 
iphone13.place(x = 20, y = 60)
iphone13.bind("<Enter>",lambda event: hovered_over(event, "iPhone13", iphone13,10,50,280,380)) 
iphone13.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13", iphone13,20,60,250,350))

iphonese = tk.Button(ipse, image = iPhoneSE, command = lambda:go_to_model(4)) 
iphonese.place(x = 20, y = 60)
iphonese.bind("<Enter>",lambda event: hovered_over(event, "iPhoneSE", iphonese,10,50,280,380)) 
iphonese.bind("<Leave>",lambda event: not_hovered_over(event, "iPhoneSE", iphonese,20,60,250,350))

###################### SECOND PAGE - MODEL SELECTION SCREEN ########################


iPhone11_MODEL_FRAME = tk.Frame(ModelSelection, width = 1200, height = 700)
iPhone12_MODEL_FRAME = tk.Frame(ModelSelection, width = 1200, height = 700)
iPhone13_MODEL_FRAME = tk.Frame(ModelSelection, width = 1200, height = 700)
iPhoneSE_MODEL_FRAME = tk.Frame(ModelSelection, width = 1200, height = 700)
iPhone11_MODEL_FRAME.place(x = 0, y = 0)
iPhone12_MODEL_FRAME.place(x = 0, y = 0)
iPhone13_MODEL_FRAME.place(x = 0, y = 0)
iPhoneSE_MODEL_FRAME.place(x = 0, y = 0)

px1 = 60
px2 = 20
px3 = 20
px4 = 450
#Frames for iPhone 11 Models 
ip11m1 = tk.Button(iPhone11_MODEL_FRAME,image = iPhone11_Regular, command = lambda:go_to_storage(1,1))
ip11m1.place(x = 0+px1, y = 110)
ip11m1.bind("<Enter>",lambda event: hovered_over(event, "iPhone11_Regular", ip11m1, px1-10, 100,280,380)) 
ip11m1.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone11_Regular", ip11m1, 0+px1, 110,250,350))


ip11m2 = tk.Button (iPhone11_MODEL_FRAME, image = iPhone11_Pro, command = lambda:go_to_storage(2,3))
ip11m2.place(x = 400+px1, y = 110)
ip11m2.bind("<Enter>",lambda event: hovered_over(event, "iPhone11_Pro", ip11m2, 400+px1-10, 100,280,380)) 
ip11m2.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone11_Pro", ip11m2, 400+px1, 110,250,350))


ip11m3 = tk.Button(iPhone11_MODEL_FRAME,image = iPhone11_Pro_Max, command = lambda:go_to_storage(3,3))
ip11m3.place(x = 800+px1, y = 90)
ip11m3.bind("<Enter>",lambda event: hovered_over(event, "iPhone11_Pro_Max", ip11m3, 800+px1-10, 100,300,400)) 
ip11m3.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone11_Pro_Max", ip11m3, 800+px1, 90,270,370))


#Frames for iPhone 12 Models 
ip12m1 = tk.Button(iPhone12_MODEL_FRAME,image = iPhone12_Regular, command = lambda:go_to_storage(1,2))
ip12m1.place(x = 0+px2, y = 110)
ip12m1.bind("<Enter>",lambda event: hovered_over(event, "iPhone12_Regular", ip12m1, px2-10, 100,280,380)) 
ip12m1.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12_Regular", ip12m1, 0+px2, 110,250,350))

ip12m2 = tk.Button (iPhone12_MODEL_FRAME, image = iPhone12_Pro, command = lambda:go_to_storage(2,4))
ip12m2.place(x = 300+px2, y = 110)
ip12m2.bind("<Enter>",lambda event: hovered_over(event, "iPhone12_Pro", ip12m2, 300+px2-10, 100,280,380)) 
ip12m2.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12_Pro", ip12m2, 300+px2, 110,250,350))

ip12m3 = tk.Button(iPhone12_MODEL_FRAME,image = iPhone12_Pro_Max, command = lambda:go_to_storage(3,4))
ip12m3.place(x = 600+px2, y = 90)
ip12m3.bind("<Enter>",lambda event: hovered_over(event, "iPhone12_Pro_Max", ip12m3, 600+px2-10, 100,300,400))
ip12m3.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12_Pro_Max", ip12m3, 600+px2, 90,270,370))


ip12m4 = tk.Button(iPhone12_MODEL_FRAME,image = iPhone12_Mini, command = lambda:go_to_storage(4,2))
ip12m4.place(x = 900+px2, y = 140)
ip12m4.bind("<Enter>",lambda event: hovered_over(event, "iPhone12_Mini", ip12m4, 900+px2-10, 130,250,350)) 
ip12m4.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12_Mini", ip12m4, 900+px2, 140,220,320))


#Frames for iPhone 13 Models 
ip13m1 = tk.Button(iPhone13_MODEL_FRAME,image = iPhone13_Regular, command = lambda:go_to_storage(1,4))
ip13m1.place(x = 0+px3, y = 110)
ip13m1.bind("<Enter>",lambda event: hovered_over(event, "iPhone13_Regular", ip13m1, px3-10, 100,280,380)) 
ip13m1.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13_Regular", ip13m1, 0+px3, 110,250,350))

ip13m2 = tk.Button (iPhone13_MODEL_FRAME, image = iPhone13_Pro, command = lambda:go_to_storage(2,5))
ip13m2.place(x = 300+px3, y = 110)
ip13m2.bind("<Enter>",lambda event: hovered_over(event, "iPhone13_Pro", ip13m2, 300+px3-10, 100,280,380)) 
ip13m2.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13_Pro", ip13m2, 300+px3, 110,250,350))

ip13m3 = tk.Button(iPhone13_MODEL_FRAME,image = iPhone13_Pro_Max, command = lambda:go_to_storage(3,5))
ip13m3.place(x = 600+px3, y = 90)
ip13m3.bind("<Enter>",lambda event: hovered_over(event, "iPhone13_Pro_Max", ip13m3, 600+px2-10, 100,300,400))
ip13m3.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13_Pro_Max", ip13m3, 600+px2, 90,270,370))

ip13m4 = tk.Button(iPhone13_MODEL_FRAME,image = iPhone13_Mini, command = lambda:go_to_storage(4,4))
ip13m4.place(x = 900+px3, y = 140)
ip13m4.bind("<Enter>",lambda event: hovered_over(event, "iPhone13_Mini", ip13m4, 900+px2-10, 130,250,350)) 
ip13m4.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13_Mini", ip13m4, 900+px2, 140,220,320))

#Frames for iPhone SE Models 
ipsem1 = tk.Button(iPhoneSE_MODEL_FRAME,image = iPhoneSE_Regular, command = lambda:go_to_storage(1,2))
ipsem1.place(x = 0+px4, y = 110)
ipsem1.bind("<Enter>",lambda event: hovered_over(event, "iPhoneSE_Regular", ipsem1, px4-10, 100,280,380)) 
ipsem1.bind("<Leave>",lambda event: not_hovered_over(event, "iPhoneSE_Regular", ipsem1, 0+px4, 110,250,350))

###################### THIRD PAGE - STORAGE SELECTION SCREEN ########################

MEMPG1 = tk.Frame(StorageSelection, width = 1200, height = 700) #(0,2)
MEMPG2 = tk.Frame(StorageSelection, width = 1200, height = 700)
MEMPG3 = tk.Frame(StorageSelection, width = 1200, height = 700)
MEMPG4 = tk.Frame(StorageSelection, width = 1200, height = 700)
MEMPG5 = tk.Frame(StorageSelection, width = 1200, height = 700)
MEMPG1.place(x = 0, y = 0)
MEMPG2.place(x = 0, y = 0)
MEMPG3.place(x = 0, y = 0)
MEMPG4.place(x = 0, y = 0)
MEMPG5.place(x = 0, y = 0)


#(0,2)
M1B1 = tk.Button(MEMPG1,image = mem1, command = lambda:search(64))
M1B1.place(x = 200+px1, y = 110)
M1B1.bind("<Enter>",lambda event: hovered_over(event, "64GB", M1B1, 200+px1-10, 100,280,380)) 
M1B1.bind("<Leave>",lambda event: not_hovered_over(event, "64GB", M1B1, 200+px1, 110,250,350))

M1B2 = tk.Button(MEMPG1,image = mem2, command = lambda:search(128))
M1B2.place(x = 600+px1, y = 110)
M1B2.bind("<Enter>",lambda event: hovered_over(event, "128GB", M1B2, 600+px1-10, 100,280,380)) 
M1B2.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M1B2, 600+px1, 110,250,350))


#(0,3)
M2B1 = tk.Button(MEMPG2,image = mem1, command = lambda:search(64))
M2B1.place(x = 0+px1, y = 110)
M2B1.bind("<Enter>",lambda event: hovered_over(event, "64GB", M2B1, px1-10, 100,280,380)) 
M2B1.bind("<Leave>",lambda event: not_hovered_over(event, "64GB", M2B1, 0+px1, 110,250,350))

M2B2 = tk.Button(MEMPG2,image = mem2, command = lambda:search(128))
M2B2.place(x = 400+px1, y = 110)
M2B2.bind("<Enter>",lambda event: hovered_over(event, "128GB", M2B2, 400+px1-10, 100,280,380)) 
M2B2.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M2B2, 400+px1, 110,250,350))

M2B3 = tk.Button(MEMPG2,image = mem3, command = lambda:search(256))
M2B3.place(x = 800+px1, y = 110)
M2B3.bind("<Enter>",lambda event: hovered_over(event, "256GB", M2B3, 800+px1-10, 100,280,380)) 
M2B3.bind("<Leave>",lambda event: not_hovered_over(event, "256GB", M2B3,800+px1, 110,250,350))

#(0,4)
M3B1 = tk.Button(MEMPG3,image = mem1, command = lambda:search(64))
M3B1.place(x = 0+px3, y = 110)
M3B1.bind("<Enter>",lambda event: hovered_over(event, "64GB", M3B1, px3-10, 100,280,380)) 
M3B1.bind("<Leave>",lambda event: not_hovered_over(event, "64GB", M3B1, 0+px3, 110,250,350))

M3B2 = tk.Button(MEMPG3,image = mem2, command = lambda:search(128))
M3B2.place(x = 300+px3, y = 110)
M3B2.bind("<Enter>",lambda event: hovered_over(event, "128GB", M3B2, 300+px3-10, 100,280,380)) 
M3B2.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M3B2, 300+px3, 110,250,350))

M3B3 = tk.Button(MEMPG3,image = mem3, command = lambda:search(256))
M3B3.place(x = 600+px3, y = 110)
M3B3.bind("<Enter>",lambda event: hovered_over(event, "256GB", M3B3, 600+px3-10, 100,280,380)) 
M3B3.bind("<Leave>",lambda event: not_hovered_over(event, "256GB", M3B3, 600+px3, 110,250,350))

M3B4 = tk.Button(MEMPG3,image = mem4, command = lambda:search(512))
M3B4.place(x = 900+px3, y = 110)
M3B4.bind("<Enter>",lambda event: hovered_over(event, "512GB", M3B4, 900+px3-10, 100,280,380)) 
M3B4.bind("<Leave>",lambda event: not_hovered_over(event, "512GB", M3B4, 900+px3, 110,250,350))


#(1,4)
M4B1 = tk.Button(MEMPG4,image = mem2, command = lambda:search(128))
M4B1.place(x = 0+px1, y = 110)
M4B1.bind("<Enter>",lambda event: hovered_over(event, "128GB", M4B1, px1-10, 100,280,380)) 
M4B1.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M4B1, 0+px1, 110,250,350))

M4B2 = tk.Button(MEMPG4,image = mem3, command = lambda:search(256))
M4B2.place(x = 400+px1, y = 110)
M4B2.bind("<Enter>",lambda event: hovered_over(event, "256GB", M4B2, 400+px1-10, 100,280,380)) 
M4B2.bind("<Leave>",lambda event: not_hovered_over(event, "256GB", M4B2, 400+px1, 110,250,350))

M4B3 = tk.Button(MEMPG4,image = mem4, command = lambda:search(512))
M4B3.place(x = 800+px1, y = 110)
M4B3.bind("<Enter>",lambda event: hovered_over(event, "512GB", M4B3, 800+px1-10, 100,280,380)) 
M4B3.bind("<Leave>",lambda event: not_hovered_over(event, "512GB", M4B3,800+px1, 110,250,350))


#(1,5)
M5B1 = tk.Button(MEMPG5,image = mem2, command = lambda:search(128))
M5B1.place(x = 0+px3, y = 110)
M5B1.bind("<Enter>",lambda event: hovered_over(event, "128GB", M5B1, px3-10, 100,280,380)) 
M5B1.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M5B1, 0+px3, 110,250,350))

M5B2 = tk.Button(MEMPG5,image = mem3, command = lambda:search(256))
M5B2.place(x = 300+px3, y = 110)
M5B2.bind("<Enter>",lambda event: hovered_over(event, "256GB", M5B2, 300+px3-10, 100,280,380)) 
M5B2.bind("<Leave>",lambda event: not_hovered_over(event, "256GB", M5B2, 300+px3, 110,250,350))

M5B3 = tk.Button(MEMPG5,image = mem4, command = lambda:search(512))
M5B3.place(x = 600+px3, y = 110)
M5B3.bind("<Enter>",lambda event: hovered_over(event, "512GB", M5B3, 600+px3-10, 100,280,380)) 
M5B3.bind("<Leave>",lambda event: not_hovered_over(event, "512GB", M5B3, 600+px3, 110,250,350))

M5B4 = tk.Button(MEMPG5,image = mem5, command = lambda:search(1))
M5B4.place(x = 900+px3, y = 110)
M5B4.bind("<Enter>",lambda event: hovered_over(event, "1TB", M5B4, 900+px3-10, 100,280,380)) 
M5B4.bind("<Leave>",lambda event: not_hovered_over(event, "1TB", M5B4, 900+px3, 110,250,350))





def main():

     root.mainloop()

if __name__ == "__main__": 
    main()