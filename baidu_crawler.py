from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import requests
#gittest

class Content:
    def __init__(self,url,title,body,image,dt,dd):
        self.url=url
        self.title=title
        self.body=body
        self.image=image
        self.dt=dt
        self.dd=dd

def getPage(url):
    req=requests.get(url)
    return BeautifulSoup(req.text,'html.parser')

def searchTPI(url):
    bs=getPage(url)
    title=bs.find("h1").text
    target_div1=bs.body.find("div",{"class":"lemmaSummary_oJtZ8 J-summary"})
    #class_='lemmaSummary_oJtZ8 J-summary'
    if target_div1:
        introduction=target_div1.find_all('span', class_='text_dt0NV')  
        body= ''.join(span.get_text()for span in introduction)
    else:
        print('未找到简介')
        body = ''

    target_div2 = bs.body.find_all('div', class_='abstractAlbum_CftjG')
    #.find_all('div', class_='abstractAlbum_CftjG')
    #概述图的div在class_='abstractAlbum_CftjG'里，但不知道为什么提取不出来，在body里找所有img最后只输出了百度百科的logo
    if target_div2:
        target_img = target_div2.find('img', src=True)
        if target_img:
            image = target_img['src']  
        else:
            print('未找到概述图')
            image = ''  
    else:
        print('div2不存在')
        image = ''  

    target_div3 = bs.body.find('div',class_='basicInfo_XhoZ7 J-basic-info')
    if target_div3:
        dt_tag=target_div3.find_all('dt', class_='basicInfoItem_SJQkr itemName_GjVei')  
        dd_tag=target_div3.find_all('dd', class_='basicInfoItem_SJQkr itemValue_qYGbJ') 
        dt='\n'.join(dt.get_text(strip=True)for dt in dt_tag)  
        dd='\n'.join(dd.get_text(strip=True)for dd in dd_tag) 
    return Content(url,title,body,image,dt,dd)


url='https://baike.baidu.com/item/%E6%BC%AB%E5%A8%81?fromModule=lemma_search-box'
content=searchTPI(url)
print('title:{}'.format(content.title))
print('URL: {}\n'.format(content.url))
print('简介:{}'.format(content.body))
print('概述图:{}'.format(content.image))
print(f"{content.dt}: {content.dd}")
