# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:19:21 2020

@author: ksaldanh
"""


import scrapy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
import re
import time
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

no_pages = 400

def get_data(pageNo):
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"} 
    r = requests.get('https://www.amazon.in/s?rh=n%3A976419031%2Cn%3A%21976420031%2Cn%3A1389401031&page='+str(pageNo)+'&qid=1597993224&ref=lp_1389401031_pg_'+str(pageNo), headers=headers)#, proxies=proxies)    content = r.content
    content = r.content
    soup = BeautifulSoup(content)
    alls= []
    
    brands_list = ['Samsung', 'OnePlus', 'Redmi', 'Oppo', 'Nokia', 'Mi']
    for d in soup.findAll('div', attrs={'class':'s-include-content-margin s-border-bottom s-latency-cf-section'}):
        #print(d)
        name = d.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'})
        rating= d.find('span', attrs={'class':'a-icon-alt'})
        price_before_discount = d.find('span', attrs={'class':'a-price a-text-price'})
        price_current = d.find('span', attrs={'class':'a-price-whole'})
        all1=[]
        if name is not None:
             brand=name.text
             all1.append(name.text)
           
        else:
             all1.append("unknown-product")
        all1.append(brand.split()[0])     
        if rating is not None:
             all1.append(rating.text)
        else:
             all1.append('-1')
        
        if price_before_discount is not None:
             all1.append(price_before_discount.text[(int(len(price_before_discount.text)/2))+1:len(price_before_discount.text)])
        #elif price_before_discount is None:
             #price_before_discount = d.find('span', attrs={'class':'a-size-base'})
        else:     
             all1.append('NA')
        if price_current is not None:
             all1.append(price_current.text)
        #elif price_before_discount is None:
             #price_before_discount = d.find('span', attrs={'class':'a-size-base'})
        else:     
             all1.append('NA')     
        alls.append(all1)     
    return alls

results = []
for i in range(1, no_pages+1):
    results.append(get_data(i))

flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=['Phone Name', 'Brand','Ratings', 'Price Before Discount', 'Current Price'])
df.to_csv('phone_products.csv', index=False, encoding='utf-8')       