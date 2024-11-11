import requests
import pandas as pd
from bs4 import BeautifulSoup

#---GLOBALS---

DEBUG = False

#---FUNCTIONS---

def getURL(item): #Passing in an item name will add that item to the standard osrs wiki header and return that url
    base_url = 'https://oldschool.runescape.wiki/w/'
    if type(item) == type(base_url):
        url = base_url+item
        if DEBUG: print (url)
        return(url)
    else:
        print("Invalid item passed into getURL method")
        return 'https://oldschool.runescape.wiki/w/'

def getPrice(url): #Passing in an item's osrs wiki url will search for the exchange price
    #Create the Soup object to be processed
    itemName = url[35:]
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    price_element = soup.find('span',class_='infobox-quantity')
    if price_element:
        exchange_price = price_element['data-val-each']
        return exchange_price

    else:
        print("Exchange price not found: " + itemName)
        return -1

def validateURL(url): #Check if URL is valid by examining the response from the requests.get function
    response = requests.get(url)
    if response.status_code >= 300:
        if DEBUG: print(url + ": " + response.status_code)
        return False
    elif response.status_code <300:
        return True


def Raw(item):#Simply add "Raw_" to the string passed in. Includes type check
    raw = 'Raw_'
    if type(item) == type (raw):
        return raw+item
    else:
        print("Invalid item passed into Raw method")


#---MAIN---

items = ['Shrimp','Sardine','Herring','Anchovies','Mackerel','Trout','Cod','Pike','Salmon','Tuna','Rainbow_Fish','Lobster','Bass','Swordfish','Monkfish','Karambwan','Shark','Sea_Turtle','Manta_Ray','Anglerfish','Dark_Crab'] #Define items here
prices = {} #{'Item': [Raw_Price, Cooked Price, CookedPrice-Raw_Price]}
for item in items:
    if type(item) == type(items[0]): 
        if validateURL(getURL(Raw(item))):
            prices[item] = {}
            prices[item]['raw'] = getPrice(getURL(Raw(item)))

        if validateURL(getURL(item)):   
            prices[item]['cooked'] = getPrice(getURL(item))
            prices[item]['profit'] =  int(prices[item]['cooked']) - int(prices[item]['raw'])
        else:
            prices[item]['cooked'] = "N/A"
            prices[item]['profit'] = "N/A"

    else:
        print("Type Error for: " + item)



df = pd.DataFrame(prices).T.reset_index()
df.columns = ['Fish','raw','cooked','profit']

df_sorted = df.sort_values('profit',ascending=False)

print (df_sorted)




