#Tyler Eck 
#410821337 
#Data Science Final Project
#TheRightiPhone


#TKINTER 
import tkinter as tk
from tkinter import Frame, PhotoImage, ttk
from tkinter import messagebox
import threading
from PIL import Image,ImageTk

#Scraping
import requests 
import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time 
from selenium.webdriver.common.keys import Keys

#driver path of the chromedriver
driverPath = 'chromedriver.exe'


#Main arrays used globally throughout the code 
location = [] 
prices = [] 
link = []
name_on_web = [] 
menu_flow = []

#Holds the previous values when user presses the back button 
SEARCH_NAME = ""
n_v = 0
SEARCH_MODEL = "" 
s_v = (0,0)
SEARCH_STORAGE = ""
st_v = 0

#recieved flags to indicate when the values are available for writing into tkinter
global R1 
R1 = 0 
global R2 
R2 = 0 
global R3
R3 = 0 

#Main iphone types
n = ["iPhone 11", "iPhone 12", "iPhone 13","iPhone SE"]

#Model index for each type ex. iPhone 11 - 3 (Regular,Pro,Pro Max)
t_for_n = [3,4,4,1]

#Models of iphones 
m = ["Regular","Pro","Pro Max","Mini"]

#Memory for iphones (each iphone type AND model has different memory combinations)
mem = ["64GB", "128GB","256GB","512GB","1TB"]

#Starting and finishing indexes for memory options based on name and model 
m_for_mem = [ 
[(0,2),(0,4),(0,4),(0,0)], 
[(0,3),(1,4),(1,4),(0,3)], 
[(1,4),(1,5),(1,5),(1,4)],
[(0,3),(0,0),(0,0),(0,0)]
]

#used to get lists of actual data for our global arrays by using scraped data
def get_real_lists(n,p,l,name,model,memory): 
    names = [] 
    price = []
    links = []
    memory =str(int(memory[:len(memory)-2]))  #Take out "GB"

    if model != "Regular": #Regular model will not check for name "Regular" in it
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

#remove the $ sign and commas from number prices 
def fix_price(p): 
    num ="1234567890" 
    l = ""
    for i in range(len(p)):
        if p[i] in num:
            l+=p[i]
    
    return int(l)

#used to start searching apple website with name, model, amd memory 
def search_apple(n,t,m):
    global location 
    global prices 
    global link
    global name_on_web
    global R1 

    #Format the string for search in the url
    name = n.split(" ")
    s = ""
    for i in name: 
        s+=i.lower()+"-"
    s = s[0:len(s)-1] 

    #Search Apple with name that we formated above
    url = "https://www.apple.com/tw/shop/buy-iphone/"+s

    #for pro models we need to include the "pro" name in the url search
    if n == "iPhone 13" and (t == "Pro" or t == "Pro Max"): 
        url+="-pro"
    
    #For Iphone 11 and SE, order is color selection->memory->no 
    #For others, order is model -> color selection ->memory ->no 
    #Select the year
    if (n == "iPhone 11" and t!= "Pro" and t!="Pro Max") or n == "iPhone SE":

        #opens browser to apple website
        browser = webdriver.Chrome(executable_path = driverPath)
        browser.get(url)
        time.sleep(1)

        #selects the Color
        select =browser.find_element_by_xpath("//div[@class='rc-dimension-multiple form-selector-swatch column large-6 small-6 form-selector']")
        select.click()
        time.sleep(1)

        #selects the Memory 
        mem_p = "//input[@data-autom='dimensionCapacity"+m.lower()+"']"
        select =browser.find_element_by_xpath(mem_p)
        select.click() 
        time.sleep(1)

        #Presses "No"
        select =browser.find_element_by_xpath("//input[@data-autom='choose-noTradeIn']")
        select.click() 
        time.sleep(3)
        
        #retrieves the price 
        price = browser.find_element_by_xpath("//span[@data-autom='full-price']")
        #retrieves the url 
        url = browser.current_url
        
        #formats the string price 
        p = fix_price(price.text) 

        #formats the keyword/name on the website to not include "Regular" 
        if t == "Regular": #without any addition 
            keyword = n+" "+m
        else:  #needs to include the model 
            keyword = n+" "+t+" "+m

        #Appends information to global arrays
        prices.append(p)
        link.append(url)
        location.append("Apple")
        name_on_web.append(keyword)

        #quit browser and sets flag R1 to 1 to indicate data is gotten
        browser.quit()
        R1 = 1

    elif (n == "iPhone 12" and t!="Pro" and t!= "Pro Max") or (n=="iPhone 13" and t!="Pro" and t!="Pro Max"): 
        #opens browser to apple website  
        browser = webdriver.Chrome(executable_path = driverPath)
        browser.get(url)
        time.sleep(1)

        #if the model is regular or mini, select seperate buttons
        if t == "Regular": 
            select =browser.find_element_by_xpath("//input[@data-autom='dimensionScreensize6_1inch']")
            select.click() 
            time.sleep(1)
        
        else:  #Mini 
            select =browser.find_element_by_xpath("//input[@data-autom='dimensionScreensize5_4inch']")
            select.click() 
            time.sleep(1)

        #Press the color
        select =browser.find_element_by_xpath("//div[@class='rc-dimension-multiple form-selector-swatch column large-6 small-6 form-selector']")
        select.click()
        time.sleep(1)   

        #Select the memory 
        mem_p = "//input[@data-autom='dimensionCapacity"+m.lower()+"']"
        select =browser.find_element_by_xpath(mem_p)
        select.click() 
        time.sleep(1)

        #Press "no"
        select =browser.find_element_by_xpath("//input[@data-autom='choose-noTradeIn']")
        select.click() 
        time.sleep(3)

        #gets price and formats it
        price = browser.find_element_by_xpath("//span[@data-autom='full-price']")
        p = fix_price(price.text)

        #gets url 
        url = browser.current_url
        
        #if Regular we dont add the word "Regular"
        if t == "Regular": #without any addition 
            keyword = n+" "+m
        else:  #needs to include the model 
            keyword = n+" "+t+" "+m


        #Appends information to global arrays
        prices.append(p)
        link.append(url)
        location.append("Apple")
        name_on_web.append(keyword)

        #quit browser and sets flag R1 to 1 to indicate data is gotten
        browser.quit()
        R1 = 1
    
    elif n=="iPhone 13" and (t == "Pro" or t=="Pro Max"):
        #opens browser to apple website
        browser = webdriver.Chrome(executable_path = driverPath)
        browser.get(url)
        time.sleep(1)

        #if the model is pro or max, select seperate buttons
        if t == "Pro": 
            select =browser.find_element_by_xpath("//input[@data-autom='dimensionScreensize6_1inch']")
            select.click() 
            time.sleep(1)
        
        else:  #MAX
            select =browser.find_element_by_xpath("//input[@data-autom='dimensionScreensize6_7inch']")
            select.click() 
            time.sleep(1)
        
        #select the color
        select =browser.find_element_by_xpath("//div[@class='rc-dimension-multiple form-selector-swatch column large-6 small-6 form-selector']")
        select.click()
        time.sleep(1)

        #selects the memory 
        mem_p = "//input[@data-autom='dimensionCapacity"+m.lower()+"']"
        select =browser.find_element_by_xpath(mem_p)
        select.click() 
        time.sleep(1)

        #Presses "no"
        select =browser.find_element_by_xpath("//input[@data-autom='choose-noTradeIn']")
        select.click() 
        time.sleep(3)

        #Extract the Price and URL 
        price = browser.find_element_by_xpath("//span[@data-autom='full-price']")
        p = fix_price(price.text) 
        url = browser.current_url
        
        
        if t == "Regular": #without any addition 
            keyword = n+" "+m
        else:  #needs to include the model 
            keyword = n+" "+t+" "+m

        #Appends information to global arrays
        prices.append(p)
        link.append(url)
        location.append("Apple")
        name_on_web.append(keyword)

        #quit browser and sets flag R1 to 1 to indicate data is gotten
        browser.quit()
        R1 = 1

    else: 
        #some models ex. iPhone 11 Pro is NOT on apple so we just pass
        print("None")
        R1 = 1


#used to start searching PCHome website with name, model, amd memory 
def search_pchome(name,model,memory): 

    global location 
    global prices 
    global link
    global name_on_web
    global R2 

    #Search PCHome
    url = "https://shopping.pchome.com.tw/"
    
    #Pop up window sometimes comes up, so we disable notifications
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")

    #goes to PCHome URL
    browser = webdriver.Chrome(executable_path = driverPath,chrome_options=chrome_options)
    browser.get(url)
    time.sleep(1)

    #format the keyword used to search
    t_mem = memory 
    if memory != "1TB": #for TB we leave the "TB" at the end 
        t_mem = memory[0:len(memory)-2] #formats memory to leave out "gb" to get more results in search
    if model == "Regular": #without any addition 
        keyword = name+" "+t_mem
    else:  #needs to include the model 
        keyword = name+" "+model+" "+t_mem

    #Search the keyword and clicks enter
    inputElement = browser.find_element_by_id("keyword")
    inputElement.send_keys(keyword) 
    select = browser.find_element_by_xpath("//span[@class='ico ico_search']")
    select.click() 
    time.sleep(2)

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

    #gets the current url     
    url = browser.current_url

    #gets the names,price, and link list 
    names = browser.find_elements_by_xpath("//h5[@class='prod_name']")
    price_l = browser.find_elements_by_xpath("//ul[@class='price_box']")
    links = browser.find_elements_by_css_selector(".prod_name [href]")
    
    #gets the specific string names, prices, and links for extracted data 
    str_names = [i.text for i in names]
    str_prices = [i.text for i in price_l] 
    links = [l.get_attribute('href') for l in links]

    P_L = [] 
    for i in str_prices:
        P_L.append(fix_price(i))
    
    #closes window
    browser.quit()
    

    #The filtering on PChome is not so great, therefore I will need to manually check 
    #items in order to see if it matches with requested iphone specs
    real_names, real_prices,real_links = get_real_lists(str_names,P_L,links,name,model,memory)

    #Add the multiple items from search results in the global arrays
    for i in range(len(real_names)):
        name_on_web.append(real_names[i])
        prices.append(real_prices[i])
        link.append(real_links[i])
        location.append("PCHome")

    #set R2 data flag to 1
    R2 = 1


#used to start searching Studio A website with name, model, amd memory 
def search_studioA(name,model,memory): 

    global location 
    global prices 
    global link
    global name_on_web
    global R3 
    
    #search Studio A - short iphone section because it is limited
    url = "https://www.studioa.com.tw/products?query=iphone&sort_by=lowest_price&order_by=desc"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(executable_path = driverPath,chrome_options=chrome_options)
    browser.get(url)
    time.sleep(2)

    #gets the names,price, and link list 
    names = browser.find_elements_by_xpath("//div[@class='title text-primary-color title-container ellipsis ']")
    price_l = browser.find_elements_by_xpath("//div[@class='quick-cart-price']")
    links = browser.find_elements_by_xpath("//a[@class='quick-cart-item']")

    str_names = [] 
    test_link = []
    for i in names:
        str_names.append(i.text)
        
    for i in links: 
        test_link.append(i.get_attribute('href'))

    #SLOWER FOR SOME REASON??? 
    # str_names = [i.text for i in names]
    # links = [l.get_attribute('href') for l in links]

    
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
    
    #closes window
    browser.quit()
    

    #The filtering on Studio A includes extra data, therefore I will need to manually check 
    #items in order to see if it matches with requested iphone specs
    real_names, real_prices,real_links = get_real_lists(str_names,price_real,test_link,name,model,memory)

    #Add the multiple items from search results in the global arrays
    for i in range(len(real_names)):
        name_on_web.append(real_names[i])
        prices.append(real_prices[i])
        link.append(real_links[i])
        location.append("Studio A")

    #sets R3 data flag to 1
    R3 = 1    

############### USED FOR THE OLD VERSION  - CLI VERSION ####################

# #used to go to model selection page with the iphone type
# def model_select(n):
#     MODELS = []
#     num = t_for_n[n-1]
#     for i in range(num): 
#         MODELS.append(m[i])
#     return MODELS

# #used to go to memory selection page based on iphone type and model
# def memory_select(name,model): 
#     name = name - 1 
#     model = model - 1
#     start,finish = m_for_mem[name][model]
#     STORAGE = [] 
#     for i in range(start,finish): 
#         STORAGE.append(mem[i])
#     return STORAGE

# def iphone_select(): 
#     print('iPhone Best Price Finder')
#     print("Select iPhone") 
#     print("1 - iPhone 11")
#     print("2 - iPhone 12") 
#     print("3 - iPhone 13")
#     print("4 - iPhone SE")
#     name = int(input())
#     while(name<1 or name>4): 
#         print("Invalid Number, enter another")
#         name = int(input())
#     return name 


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
#     "Location
# ":location, 
#     "Price":prices,
#     "Link":link
# }

# df = pd.DataFrame(dict) 

# df = df.sort_values(by=['Price'])
# df2 = df.reset_index(drop=True)
# print(df2)

############### USED FOR THE NEW VERSION  - GUI VERSION ####################

#Manually changes the model page based on name
def go_to_model(name):
    global SEARCH_NAME
    global n_v
    n_v = name
    show_frame(ModelSelection)
    if name == 1: 
        show_frame(iPhone11_MODEL_FRAME) #1 refers to iphone 11 
        SEARCH_NAME = n[0]
        print(SEARCH_NAME)
    elif name == 2:
        show_frame(iPhone12_MODEL_FRAME) #2 refers to iphone 12
        SEARCH_NAME = n[1]
        print(SEARCH_NAME)
    elif name == 3:
        show_frame(iPhone13_MODEL_FRAME) #3 refers to iphone 13
        SEARCH_NAME = n[2]
        print(SEARCH_NAME)
    elif name == 4:
        show_frame(iPhoneSE_MODEL_FRAME) #4 refers to iphone SE
        SEARCH_NAME = n[3]
        print(SEARCH_NAME)

#Manually changes the storage page based on selected model and type
def go_to_storage(SEL_MODEL, s):
    show_frame(StorageSelection)
    global s_v 
    global SEARCH_NAME
    s_v = (SEL_MODEL, s)
    
    #gets the search model 
    global SEARCH_MODEL
    SEARCH_MODEL = m[SEL_MODEL-1]

    #gets the start and finish indexes for mem
    model = SEL_MODEL-1
    name = n.index(SEARCH_NAME) 
    start,finish = m_for_mem[name][model]
    print(start,finish)

    #prints out storage for that specific type and model
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

#used to compile information on the instruction/confirmation page before search starts
def search(l): 
    global SEARCH_NAME
    global SEARCH_MODEL
    global SEARCH_STORAGE
    global st_v
    st_v = l

    if l == 1: 
        SEARCH_STORAGE = "1TB"
    else: 
        SEARCH_STORAGE = str(l)+"GB"
    
    Search_Label.config(text = SEARCH_NAME+" "+SEARCH_MODEL+" "+SEARCH_STORAGE)
    NAME_Label.config(text = SEARCH_NAME)
    MODEL_Label.config(text = SEARCH_MODEL)
    STORAGE_Label.config(text = SEARCH_STORAGE)
    show_frame(InstructionScreen)

#used ot start thread searches when user presses search button
def start_search(): 
    CD = threading.Thread(target = check_data,daemon=True) 
    CD.start()

    t3 = threading.Thread(target = search_studioA, args =(SEARCH_NAME,SEARCH_MODEL,SEARCH_STORAGE),daemon=True) 
    t3.start()

    t1 = threading.Thread(target = search_apple, args =(SEARCH_NAME,SEARCH_MODEL,SEARCH_STORAGE),daemon=True) 
    t1.start()

    t2 = threading.Thread(target = search_pchome, args =(SEARCH_NAME,SEARCH_MODEL,SEARCH_STORAGE),daemon=True) 
    t2.start()


#Function to switch between frames 
def show_frame(frame): 
    frame.tkraise()


#this thread starts to check when all data is available and scraping is done 
#when finished, a dataframe will be formed to compile all the data together 
#that will be used for the end table
def check_data(): 
    global R1,R2,R3 
    while True:
        if R1 == 1 and R2 == 1 and R3 == 1: #if all data flags are true
            show_frame(DataScreen)
            R1 = 0 
            R2 = 0 
            R3 = 0 

            dict = { 
                "Name on Web":name_on_web,
                "Location":location,
                "Price":prices,
                "Link":link
            }
            AC = 0 #Apple Count 
            PCC = 0 #PCHome Count
            SAC = 0 #Studio A Count

            #creates dataframe from the dict
            df = pd.DataFrame(dict) 

            #counts the number of each search result for each website
            for i in range(len(dict["Name on Web"])): 
                if dict["Location"][i] == "Apple": 
                    AC+=1 
                elif dict["Location"][i] == "PCHome": 
                    PCC+=1
                else: 
                    SAC+=1
            
            #show the search info by configure labels defined below
            Apple_Label_D.config(text = str(AC))
            PCHome_Label_D.config(text = str(PCC))
            SA_Label_D.config(text = str(SAC))
            Total_Label_C.config(text = str(AC+PCC+SAC))
            Search_Label2.config(text = SEARCH_NAME+" "+SEARCH_MODEL+" "+SEARCH_STORAGE)

            #sorts table based on price and drops the index
            df = df.sort_values(by=['Price'])
            df2 = df.reset_index(drop=True)
            print(df2)

            #formats the columns and headings
            tv1["column"] = list(df2.columns)
            tv1["show"] = "headings"

            tv1.heading(tv1["column"][0], text = tv1["column"][0])
            tv1.column(tv1["column"][0], stretch = True, width = 400)

            tv1.heading(tv1["column"][1], text = tv1["column"][1])
            tv1.column(tv1["column"][1],stretch = True, width = 100)

            tv1.heading(tv1["column"][2], text = tv1["column"][2])
            tv1.column(tv1["column"][2], stretch = True, width = 100)

            tv1.heading(tv1["column"][3], text = tv1["column"][3])
            tv1.column(tv1["column"][3], stretch = True, width = 400)

            #adds the rows of data to the table
            df_rows = df.to_numpy().tolist()
            for row in df_rows: 
                tv1.insert("","end",values=row)

            #binds the items so that user can click on the selected item and the website will pop up 
            tv1.bind('<<TreeviewSelect>>', item_selected)
            break

#if item from table is selected, a webpage with the link will pop up 
def item_selected(event):
    link = ""
    for selected_item in tv1.selection():
        item = tv1.item(selected_item)
        record = item['values']
        link = record[3]
    #pops up window for users to view website page
    browser = webdriver.Chrome(executable_path = driverPath)
    browser.get(link)

#go back function allows for users to go back to previous page in case a mistake is made
def goback(i):
    global n_v 
    global s_v
    global st_v

    global SEARCH_NAME
    global SEARCH_MODEL
    global SEARCH_STORAGE

    if i == 1: #switching back to iphone selection screen
        print(n_v)
        n_v = 0
        SEARCH_NAME = ""
        show_frame(iPhoneSelection)
    elif i == 2: #switching back to model selection screen 
        print(s_v)
        s_v = (0,0)
        SEARCH_MODEL = ""
        go_to_model(n_v)
    elif i == 3: #switching back to storage selection screen 
        print(st_v)
        st_v = 0
        x,y = s_v
        SEARCH_STORAGE = ""
        go_to_storage(x,y)


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

########################  GUI Specifications and Setup  ###########################

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

Instructions = resize_image('Pictures/Instructions.png',900,300)
Instructions2 = resize_image('Pictures/Instructions2.png',750,150)

mem1 = resize_image('Pictures/64GB.png',250,350)
mem2 = resize_image('Pictures/128GB.png',250,350)
mem3 = resize_image('Pictures/256GB.png',250,350)
mem4 = resize_image('Pictures/512GB.png',250,350)
mem5 = resize_image('Pictures/1TB.png',250,350)

#Making the different screens so that we can go through selections 

#FRAME 1 - IPHONE SELECTION PAGE
iPhoneSelection = tk.Frame(root,width = 1200, height = 700)
iPhoneSelection.place(x = 0, y = 0)

#FRAME 2 - MODEL SELECTION PAGE
ModelSelection = tk.Frame(root,width = 1200, height = 700)
ModelSelection.place(x = 0, y = 0)

#FRAME 3 - STORAGE SELECTION PAGE
StorageSelection = tk.Frame(root,width = 1200, height = 700)
StorageSelection.place(x = 0, y = 0)

InstructionScreen = tk.Frame(root,width = 1200, height = 700)
InstructionScreen.place(x = 0, y = 0)

DataScreen = tk.Frame(root,width = 1200, height = 700)
DataScreen.place(x = 0, y = 0)

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

Selection_Label = tk.Label(iPhoneSelection, text = "Select iPhone ",font = ("Arial", 50))
Selection_Label.place(x = 380, y = 30)


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

Model_Label = tk.Label(iPhone11_MODEL_FRAME, text = "Select Model ",font = ("Arial", 50))
Model_Label.place(x = 380, y = 10)
Model_Label = tk.Label(iPhone12_MODEL_FRAME, text = "Select Model ",font = ("Arial", 50))
Model_Label.place(x = 380, y = 10)
Model_Label = tk.Label(iPhone13_MODEL_FRAME, text = "Select Model ",font = ("Arial", 50))
Model_Label.place(x = 380, y = 10)
Model_Label = tk.Label(iPhoneSE_MODEL_FRAME, text = "Select Model ",font = ("Arial", 50))
Model_Label.place(x = 380, y = 10)

Back_Button = ttk.Button(iPhone11_MODEL_FRAME, text = "Back", style = "Accentbutton",command = lambda:goback(1))
Back_Button.place(x = 1110, y = 10)
Back_Button = ttk.Button(iPhone12_MODEL_FRAME, text = "Back", style = "Accentbutton",command = lambda:goback(1))
Back_Button.place(x = 1110, y = 10)
Back_Button = ttk.Button(iPhone13_MODEL_FRAME, text = "Back", style = "Accentbutton",command = lambda:goback(1))
Back_Button.place(x = 1110, y = 10)
Back_Button = ttk.Button(iPhoneSE_MODEL_FRAME, text = "Back", style = "Accentbutton",command = lambda:goback(1))
Back_Button.place(x = 1110, y = 10)


px1 = 60
px2 = 20
px3 = 20
px4 = 450
#Frames for iPhone 11 Models 
ip11m1 = tk.Button(iPhone11_MODEL_FRAME,image = iPhone11_Regular, command = lambda:go_to_storage(1,1))
ip11m1.place(x = 0+px1, y = 110)
ip11m1.bind("<Enter>",lambda event: hovered_over(event, "iPhone11_Regular", ip11m1, px1-10, 100,280,380)) 
ip11m1.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone11_Regular", ip11m1, 0+px1, 110,250,350))
ip11m1_L = tk.Label(iPhone11_MODEL_FRAME, text = "Regular ",font = ("Arial", 40))
ip11m1_L.place(x = 0+px1+32, y = 500)
ip11m1_L2 = tk.Label(iPhone11_MODEL_FRAME, text = "6.1\" ",font = ("Arial", 30))
ip11m1_L2.place(x = 0+px1+90, y = 580)
ip11m1_L3 = tk.Label(iPhone11_MODEL_FRAME, text = "Liquid Retina HD display",font = ("Arial", 15))
ip11m1_L3.place(x = 0+px1+15, y = 625)


ip11m2 = tk.Button (iPhone11_MODEL_FRAME, image = iPhone11_Pro, command = lambda:go_to_storage(2,3))
ip11m2.place(x = 400+px1, y = 110)
ip11m2.bind("<Enter>",lambda event: hovered_over(event, "iPhone11_Pro", ip11m2, 400+px1-10, 100,280,380)) 
ip11m2.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone11_Pro", ip11m2, 400+px1, 110,250,350))
ip11m2_L = tk.Label(iPhone11_MODEL_FRAME, text = "Pro ",font = ("Arial", 40))
ip11m2_L.place(x = 400+px1+80, y = 500)
ip11m2_L2 = tk.Label(iPhone11_MODEL_FRAME, text = "5.8\" ",font = ("Arial", 30))
ip11m2_L2.place(x = 400+px1+90, y = 580)
ip11m2_L3 = tk.Label(iPhone11_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip11m2_L3.place(x = 400+px1+10, y = 625)


ip11m3 = tk.Button(iPhone11_MODEL_FRAME,image = iPhone11_Pro_Max, command = lambda:go_to_storage(3,3))
ip11m3.place(x = 800+px1, y = 90)
ip11m3.bind("<Enter>",lambda event: hovered_over(event, "iPhone11_Pro_Max", ip11m3, 800+px1-10, 100,300,400)) 
ip11m3.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone11_Pro_Max", ip11m3, 800+px1, 90,270,370))
ip11m3_L = tk.Label(iPhone11_MODEL_FRAME, text = "Pro Max ",font = ("Arial", 40))
ip11m3_L.place(x = 800+px1+32, y = 500)
ip11m3_L2 = tk.Label(iPhone11_MODEL_FRAME, text = "6.5\" ",font = ("Arial", 30))
ip11m3_L2.place(x = 800+px1+105, y = 580)
ip11m3_L3 = tk.Label(iPhone11_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip11m3_L3.place(x = 800+px1+25, y = 625)



#Frames for iPhone 12 Models 
ip12m1 = tk.Button(iPhone12_MODEL_FRAME,image = iPhone12_Regular, command = lambda:go_to_storage(1,2))
ip12m1.place(x = 0+px2, y = 110)
ip12m1.bind("<Enter>",lambda event: hovered_over(event, "iPhone12_Regular", ip12m1, px2-10, 100,280,380)) 
ip12m1.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12_Regular", ip12m1, 0+px2, 110,250,350))
ip12m1_L = tk.Label(iPhone12_MODEL_FRAME, text = "Regular ",font = ("Arial", 40))
ip12m1_L.place(x = 0+px2+35, y = 500)
ip12m1_L2 = tk.Label(iPhone12_MODEL_FRAME, text = "6.1\" ",font = ("Arial", 30))
ip12m1_L2.place(x = 0+px2+90, y = 580)
ip12m1_L3 = tk.Label(iPhone12_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip12m1_L3.place(x = 0+px2+10, y = 625)


ip12m2 = tk.Button (iPhone12_MODEL_FRAME, image = iPhone12_Pro, command = lambda:go_to_storage(2,4))
ip12m2.place(x = 300+px2, y = 110)
ip12m2.bind("<Enter>",lambda event: hovered_over(event, "iPhone12_Pro", ip12m2, 300+px2-10, 100,280,380)) 
ip12m2.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12_Pro", ip12m2, 300+px2, 110,250,350))
ip12m2_L = tk.Label(iPhone12_MODEL_FRAME, text = "Pro ",font = ("Arial", 40))
ip12m2_L.place(x = 300+px2+80, y = 500)
ip12m2_L2 = tk.Label(iPhone12_MODEL_FRAME, text = "6.1\" ",font = ("Arial", 30))
ip12m2_L2.place(x = 300+px2+90, y = 580)
ip12m2_L3 = tk.Label(iPhone12_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip12m2_L3.place(x = 300+px2+10, y = 625)

ip12m3 = tk.Button(iPhone12_MODEL_FRAME,image = iPhone12_Pro_Max, command = lambda:go_to_storage(3,4))
ip12m3.place(x = 600+px2, y = 90)
ip12m3.bind("<Enter>",lambda event: hovered_over(event, "iPhone12_Pro_Max", ip12m3, 600+px2-10, 100,300,400))
ip12m3.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12_Pro_Max", ip12m3, 600+px2, 90,270,370))
ip12m3_L = tk.Label(iPhone12_MODEL_FRAME, text = "Pro Max ",font = ("Arial", 40))
ip12m3_L.place(x = 600+px2+35, y = 500)
ip12m3_L2 = tk.Label(iPhone12_MODEL_FRAME, text = "6.7\" ",font = ("Arial", 30))
ip12m3_L2.place(x = 600+px2+100, y = 580)
ip12m3_L3 = tk.Label(iPhone12_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip12m3_L3.place(x = 600+px2+25, y = 625)

ip12m4 = tk.Button(iPhone12_MODEL_FRAME,image = iPhone12_Mini, command = lambda:go_to_storage(4,2))
ip12m4.place(x = 900+px2+20, y = 140)
ip12m4.bind("<Enter>",lambda event: hovered_over(event, "iPhone12_Mini", ip12m4, 900+px2-10+20, 130,250,350)) 
ip12m4.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone12_Mini", ip12m4, 900+px2+20, 140,220,320))
ip12m4_L = tk.Label(iPhone12_MODEL_FRAME, text = "Mini ",font = ("Arial", 40))
ip12m4_L.place(x = 900+px2+85, y = 500)
ip12m4_L2 = tk.Label(iPhone12_MODEL_FRAME, text = "5.4\" ",font = ("Arial", 30))
ip12m4_L2.place(x = 900+px2+100, y = 580)
ip12m4_L3 = tk.Label(iPhone12_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip12m4_L3.place(x = 900+px2+25, y = 625)



#Frames for iPhone 13 Models 
ip13m1 = tk.Button(iPhone13_MODEL_FRAME,image = iPhone13_Regular, command = lambda:go_to_storage(1,4))
ip13m1.place(x = 0+px3, y = 110)
ip13m1.bind("<Enter>",lambda event: hovered_over(event, "iPhone13_Regular", ip13m1, px3-10, 100,280,380)) 
ip13m1.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13_Regular", ip13m1, 0+px3, 110,250,350))
ip13m1_L = tk.Label(iPhone13_MODEL_FRAME, text = "Regular ",font = ("Arial", 40))
ip13m1_L.place(x = 0+px3+35, y = 500)
ip13m1_L2 = tk.Label(iPhone13_MODEL_FRAME, text = "6.1\" ",font = ("Arial", 30))
ip13m1_L2.place(x = 0+px3+90, y = 580)
ip13m1_L3 = tk.Label(iPhone13_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip13m1_L3.place(x = 0+px3+10, y = 625)


ip13m2 = tk.Button (iPhone13_MODEL_FRAME, image = iPhone13_Pro, command = lambda:go_to_storage(2,5))
ip13m2.place(x = 300+px3, y = 110)
ip13m2.bind("<Enter>",lambda event: hovered_over(event, "iPhone13_Pro", ip13m2, 300+px3-10, 100,280,380)) 
ip13m2.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13_Pro", ip13m2, 300+px3, 110,250,350))
ip13m2_L = tk.Label(iPhone13_MODEL_FRAME, text = "Pro ",font = ("Arial", 40))
ip13m2_L.place(x = 300+px3+80, y = 500)
ip13m2_L2 = tk.Label(iPhone13_MODEL_FRAME, text = "6.1\" ",font = ("Arial", 30))
ip13m2_L2.place(x = 300+px3+90, y = 580)
ip13m2_L3 = tk.Label(iPhone13_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip13m2_L3.place(x = 300+px3+10, y = 625)
ip13m2_L4 = tk.Label(iPhone13_MODEL_FRAME, text = "with Pro Motion",font = ("Arial", 15))
ip13m2_L4.place(x = 300+px3+50, y = 650)

ip13m3 = tk.Button(iPhone13_MODEL_FRAME,image = iPhone13_Pro_Max, command = lambda:go_to_storage(3,5))
ip13m3.place(x = 600+px3, y = 90)
ip13m3.bind("<Enter>",lambda event: hovered_over(event, "iPhone13_Pro_Max", ip13m3, 600+px2-10, 100,300,400))
ip13m3.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13_Pro_Max", ip13m3, 600+px2, 90,270,370))
ip13m3_L = tk.Label(iPhone13_MODEL_FRAME, text = "Pro Max ",font = ("Arial", 40))
ip13m3_L.place(x = 600+px3+35, y = 500)
ip13m3_L2 = tk.Label(iPhone13_MODEL_FRAME, text = "6.7\" ",font = ("Arial", 30))
ip13m3_L2.place(x = 600+px3+100, y = 580)
ip13m3_L3 = tk.Label(iPhone13_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip13m3_L3.place(x = 600+px3+25, y = 625)
ip13m3_L4 = tk.Label(iPhone13_MODEL_FRAME, text = "with Pro Motion",font = ("Arial", 15))
ip13m3_L4.place(x = 600+px3+65, y = 650)

ip13m4 = tk.Button(iPhone13_MODEL_FRAME,image = iPhone13_Mini, command = lambda:go_to_storage(4,4))
ip13m4.place(x = 900+px3+20, y = 140)
ip13m4.bind("<Enter>",lambda event: hovered_over(event, "iPhone13_Mini", ip13m4, 900+px2-10+20, 130,250,350)) 
ip13m4.bind("<Leave>",lambda event: not_hovered_over(event, "iPhone13_Mini", ip13m4, 900+px2+20, 140,220,320))
ip13m4_L = tk.Label(iPhone13_MODEL_FRAME, text = "Mini",font = ("Arial", 40))
ip13m4_L.place(x = 900+px3+85, y = 500)
ip13m4_L2 = tk.Label(iPhone13_MODEL_FRAME, text = "5.4\" ",font = ("Arial", 30))
ip13m4_L2.place(x = 900+px3+100, y = 580)
ip13m4_L3 = tk.Label(iPhone13_MODEL_FRAME, text = "Super Retina XDR display",font = ("Arial", 15))
ip13m4_L3.place(x = 900+px3+25, y = 625)


#Frames for iPhone SE Models 
ipsem1 = tk.Button(iPhoneSE_MODEL_FRAME,image = iPhoneSE_Regular, command = lambda:go_to_storage(1,2))
ipsem1.place(x = 0+px4, y = 110)
ipsem1.bind("<Enter>",lambda event: hovered_over(event, "iPhoneSE_Regular", ipsem1, px4-10, 100,280,380)) 
ipsem1.bind("<Leave>",lambda event: not_hovered_over(event, "iPhoneSE_Regular", ipsem1, 0+px4, 110,250,350))
ipsem1_L = tk.Label(iPhoneSE_MODEL_FRAME, text = "Regular",font = ("Arial", 40))
ipsem1_L.place(x = px4+32, y = 500)
ipsem1_L2 = tk.Label(iPhoneSE_MODEL_FRAME, text = "4.7\" ",font = ("Arial", 30))
ipsem1_L2.place(x = px4+90, y = 580)
ipsem1_L3 = tk.Label(iPhoneSE_MODEL_FRAME, text = "Retina HD Display",font = ("Arial", 15))
ipsem1_L3.place(x = px4+42, y = 625)

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

Back_Button = ttk.Button(MEMPG1, text = "Back", style = "Accentbutton",command = lambda:goback(2))
Back_Button.place(x = 1110, y = 10)
Back_Button = ttk.Button(MEMPG2, text = "Back", style = "Accentbutton",command = lambda:goback(2))
Back_Button.place(x = 1110, y = 10)
Back_Button = ttk.Button(MEMPG3, text = "Back", style = "Accentbutton",command = lambda:goback(2))
Back_Button.place(x = 1110, y = 10)
Back_Button = ttk.Button(MEMPG4, text = "Back", style = "Accentbutton",command = lambda:goback(2))
Back_Button.place(x = 1110, y = 10)
Back_Button = ttk.Button(MEMPG5, text = "Back", style = "Accentbutton",command = lambda:goback(2))
Back_Button.place(x = 1110, y = 10)

Storage_Label = tk.Label(MEMPG1, text = "Select Storage ",font = ("Arial", 50))
Storage_Label.place(x = 380, y = 30)
Storage_Label = tk.Label(MEMPG2, text = "Select Storage ",font = ("Arial", 50))
Storage_Label.place(x = 380, y = 30)
Storage_Label = tk.Label(MEMPG3, text = "Select Storage ",font = ("Arial", 50))
Storage_Label.place(x = 380, y = 30)
Storage_Label = tk.Label(MEMPG4, text = "Select Storage ",font = ("Arial", 50))
Storage_Label.place(x = 380, y = 30)
Storage_Label = tk.Label(MEMPG5, text = "Select Storage ",font = ("Arial", 50))
Storage_Label.place(x = 380, y = 30)

#used to change height of the storage buttons
yx = 150

#(0,2)
M1B1 = tk.Button(MEMPG1,image = mem1, command = lambda:search(64))
M1B1.place(x = 200+px1, y = yx)
M1B1.bind("<Enter>",lambda event: hovered_over(event, "64GB", M1B1, 200+px1-10, yx-10,280,380)) 
M1B1.bind("<Leave>",lambda event: not_hovered_over(event, "64GB", M1B1, 200+px1, yx,250,350))

M1B2 = tk.Button(MEMPG1,image = mem2, command = lambda:search(128))
M1B2.place(x = 600+px1, y = yx)
M1B2.bind("<Enter>",lambda event: hovered_over(event, "128GB", M1B2, 600+px1-10, yx-10,280,380)) 
M1B2.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M1B2, 600+px1, yx,250,350))


#(0,3)
M2B1 = tk.Button(MEMPG2,image = mem1, command = lambda:search(64))
M2B1.place(x = 0+px1, y = yx)
M2B1.bind("<Enter>",lambda event: hovered_over(event, "64GB", M2B1, px1-10, yx-10,280,380)) 
M2B1.bind("<Leave>",lambda event: not_hovered_over(event, "64GB", M2B1, 0+px1, yx,250,350))

M2B2 = tk.Button(MEMPG2,image = mem2, command = lambda:search(128))
M2B2.place(x = 400+px1, y = yx)
M2B2.bind("<Enter>",lambda event: hovered_over(event, "128GB", M2B2, 400+px1-10, yx-10,280,380)) 
M2B2.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M2B2, 400+px1, yx,250,350))

M2B3 = tk.Button(MEMPG2,image = mem3, command = lambda:search(256))
M2B3.place(x = 800+px1, y = yx)
M2B3.bind("<Enter>",lambda event: hovered_over(event, "256GB", M2B3, 800+px1-10, yx-10,280,380)) 
M2B3.bind("<Leave>",lambda event: not_hovered_over(event, "256GB", M2B3,800+px1, yx,250,350))

#(0,4)
M3B1 = tk.Button(MEMPG3,image = mem1, command = lambda:search(64))
M3B1.place(x = 0+px3, y = yx)
M3B1.bind("<Enter>",lambda event: hovered_over(event, "64GB", M3B1, px3-10, yx-10,280,380)) 
M3B1.bind("<Leave>",lambda event: not_hovered_over(event, "64GB", M3B1, 0+px3, yx,250,350))

M3B2 = tk.Button(MEMPG3,image = mem2, command = lambda:search(128))
M3B2.place(x = 300+px3, y = yx)
M3B2.bind("<Enter>",lambda event: hovered_over(event, "128GB", M3B2, 300+px3-10, yx-10,280,380)) 
M3B2.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M3B2, 300+px3, yx,250,350))

M3B3 = tk.Button(MEMPG3,image = mem3, command = lambda:search(256))
M3B3.place(x = 600+px3, y = yx)
M3B3.bind("<Enter>",lambda event: hovered_over(event, "256GB", M3B3, 600+px3-10, yx-10,280,380)) 
M3B3.bind("<Leave>",lambda event: not_hovered_over(event, "256GB", M3B3, 600+px3, yx,250,350))

M3B4 = tk.Button(MEMPG3,image = mem4, command = lambda:search(512))
M3B4.place(x = 900+px3, y = yx)
M3B4.bind("<Enter>",lambda event: hovered_over(event, "512GB", M3B4, 900+px3-10, yx-10,280,380)) 
M3B4.bind("<Leave>",lambda event: not_hovered_over(event, "512GB", M3B4, 900+px3, yx,250,350))


#(1,4)
M4B1 = tk.Button(MEMPG4,image = mem2, command = lambda:search(128))
M4B1.place(x = 0+px1, y = yx)
M4B1.bind("<Enter>",lambda event: hovered_over(event, "128GB", M4B1, px1-10, yx-10,280,380)) 
M4B1.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M4B1, 0+px1, yx,250,350))

M4B2 = tk.Button(MEMPG4,image = mem3, command = lambda:search(256))
M4B2.place(x = 400+px1, y = yx)
M4B2.bind("<Enter>",lambda event: hovered_over(event, "256GB", M4B2, 400+px1-10, yx-10,280,380)) 
M4B2.bind("<Leave>",lambda event: not_hovered_over(event, "256GB", M4B2, 400+px1, yx,250,350))

M4B3 = tk.Button(MEMPG4,image = mem4, command = lambda:search(512))
M4B3.place(x = 800+px1, y = yx)
M4B3.bind("<Enter>",lambda event: hovered_over(event, "512GB", M4B3, 800+px1-10, yx-10,280,380)) 
M4B3.bind("<Leave>",lambda event: not_hovered_over(event, "512GB", M4B3,800+px1, yx,250,350))


#(1,5)
M5B1 = tk.Button(MEMPG5,image = mem2, command = lambda:search(128))
M5B1.place(x = 0+px3, y = yx)
M5B1.bind("<Enter>",lambda event: hovered_over(event, "128GB", M5B1, px3-10, yx-10,280,380)) 
M5B1.bind("<Leave>",lambda event: not_hovered_over(event, "128GB", M5B1, 0+px3, yx,250,350))

M5B2 = tk.Button(MEMPG5,image = mem3, command = lambda:search(256))
M5B2.place(x = 300+px3, y = yx)
M5B2.bind("<Enter>",lambda event: hovered_over(event, "256GB", M5B2, 300+px3-10, yx-10,280,380)) 
M5B2.bind("<Leave>",lambda event: not_hovered_over(event, "256GB", M5B2, 300+px3, yx,250,350))

M5B3 = tk.Button(MEMPG5,image = mem4, command = lambda:search(512))
M5B3.place(x = 600+px3, y = yx)
M5B3.bind("<Enter>",lambda event: hovered_over(event, "512GB", M5B3, 600+px3-10, yx-10,280,380)) 
M5B3.bind("<Leave>",lambda event: not_hovered_over(event, "512GB", M5B3, 600+px3, yx,250,350))

M5B4 = tk.Button(MEMPG5,image = mem5, command = lambda:search(1))
M5B4.place(x = 900+px3, y = yx)
M5B4.bind("<Enter>",lambda event: hovered_over(event, "1TB", M5B4, 900+px3-10, yx-10,280,380)) 
M5B4.bind("<Leave>",lambda event: not_hovered_over(event, "1TB", M5B4, 900+px3, yx,250,350))


###################### FOURTH PAGE - INSTRUCTIONS SCREEN ########################
s = SEARCH_NAME+SEARCH_MODEL+SEARCH_STORAGE 
Instruction_Label = tk.Label(InstructionScreen, text = "Instructions ",font = ("Arial", 50))
Instruction_Label.place(x = 420, y = 30)

Instructions_L = tk.Label(InstructionScreen, image = Instructions)
Instructions_L.place(x = 150, y = 350)

yy = 140
xx = 100
L1 = tk.Label(InstructionScreen, text = "iPhone Name:", font = ("Arial", 20))
L1.place(x = 300+xx, y = 0+yy)
NAME_Label = tk.Label(InstructionScreen, text = SEARCH_NAME , font = ("Arial", 20))
NAME_Label.place(x = 550+xx , y = 0+yy)

L2 = tk.Label(InstructionScreen, text = "iPhone Model:", font = ("Arial", 20))
L2.place(x = 300+xx, y = 50+yy)
MODEL_Label = tk.Label(InstructionScreen, text = SEARCH_MODEL , font = ("Arial", 20))
MODEL_Label.place(x = 550+xx , y = 50+yy)

L3 = tk.Label(InstructionScreen, text = "iPhone Storage:", font = ("Arial", 20))
L3.place(x = 280+xx, y = 100+yy)
STORAGE_Label = tk.Label(InstructionScreen, text = SEARCH_STORAGE , font = ("Arial", 20))
STORAGE_Label.place(x = 550+xx , y = 100+yy)

L4 = tk.Label(InstructionScreen, text = "Search Text:", font = ("Arial", 20))
L4.place(x = 320+xx, y = 150+yy)
Search_Label = tk.Label(InstructionScreen, text = s, font = ("Arial", 20))
Search_Label.place(x = 550+xx, y = 150+yy)


Back_Button = ttk.Button(InstructionScreen, text = "Back", style = "Accentbutton",command = lambda:goback(3))
Back_Button.place(x = 1110, y = 10)

Search = ttk.Button(InstructionScreen,text="Search", style = "Accentbutton",command = start_search) 
Search.place(x = 950, y = 600)


###################### FIFTH PAGE - DATA SCREEN ########################
Results_Label = tk.Label(DataScreen, text = "Search Results",font = ("Arial 50 underline"))
Results_Label.place(x = 360, y = 30)

Search_Label1 =  tk.Label(DataScreen, text="Searched:", font = ("Arial", 20))
Search_Label1.place(x = 100, y = 150)

Search_Label2 = tk.Label(DataScreen, font = ("Arial", 20))
Search_Label2.place(x = 250, y = 150)

XX1 = -200
YY1 = 55
Apple_Label = tk.Label(DataScreen, text = "Apple:",font = ("Arial", 20))
Apple_Label.place(x = 300+XX1, y = 150+YY1)
Apple_Label_D = tk.Label(DataScreen, text = "0",font = ("Arial", 20))
Apple_Label_D.place(x = 380+XX1, y = 151+YY1)

PCHome_Label = tk.Label(DataScreen, text = "PCHome:",font = ("Arial", 20))
PCHome_Label.place(x = 450+XX1, y = 150+YY1)
PCHome_Label_D = tk.Label(DataScreen, text = "0",font = ("Arial", 20))
PCHome_Label_D.place(x = 570+XX1, y = 151+YY1)

SA_Label = tk.Label(DataScreen, text = "Studio A:",font = ("Arial", 20))
SA_Label.place(x = 640+XX1, y = 150+YY1)
SA_Label_D = tk.Label(DataScreen, text = "0",font = ("Arial", 20))
SA_Label_D.place(x = 760+XX1, y = 151+YY1)

Total_Label = tk.Label(DataScreen, text = "Total:",font = ("Arial", 20))
Total_Label.place(x = 990, y = 150+YY1)
Total_Label_C = tk.Label(DataScreen, text = "0",font = ("Arial", 20))
Total_Label_C.place(x = 1070, y = 151+YY1)


DATA_VIEW = tk.LabelFrame(DataScreen,text = "Data")
DATA_VIEW.place(x = 100, y = 240, height = 300, width = 1000)
tv1 = ttk.Treeview(DATA_VIEW,height = 10)
tv1.place(relheight=1, relwidth=1)

treescrolly = tk.Scrollbar(DATA_VIEW, orient = "vertical", command = tv1.yview)
treescrollx = tk.Scrollbar(DATA_VIEW, orient = "horizontal", command = tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side= "bottom", fill = "x") 
treescrolly.pack(side = "right", fill ="y")


Instructions2_L = tk.Label(DataScreen, image = Instructions2)
Instructions2_L.place(x = 230, y = 550)
            
######################## MAIN FUNCTION - MAIN TKINTER LOOP #######################
def main():

    root.mainloop()

if __name__ == "__main__": 
    main()