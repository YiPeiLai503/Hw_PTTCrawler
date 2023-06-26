# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 08:58:44 2023

@author: L
"""

"""
程式說明:
    使用程式爬取PTT表特版前一天的所有文章，並記錄以下資訊:
        1. 作者帳號
        2. 文章標題
        3. 發文時間
        4. 發文IP
        5. 文章中第一張圖片網址
        6. 該文章推數
        7. 該文章噓數
    假如文章中不存在圖片，則不紀錄，最後將以上資訊以及爬取時間以文字檔方式儲存，格式為.csv
"""
import os
import re
import requests
import csv
import datetime
from requests_html import HTML
from bs4 import BeautifulSoup

#設定爬蟲爬的日期，預設為爬昨天的文章
#getValue 可用來查詢現在設定的值為何
#setValue 可用來更改私有設定的值
#setValue 傳入之第一個值為起始時間，0代表從今天開始，1代表昨天，以此列推
#setValue 傳入之第二個值為結束時間，2代表前天，因此會只爬取昨天一天的文章
#crawerTime 回傳與PTT版上相同之時間格式，EX: 6/14
class crawlerTimeSet:
    def __init__(self):
        self.__startValue = 1
        self.__stopValue = 2
        
    def getValue(self):
        return (self.__startValue, self.__stopValue)
    
    def setValue(self, start, stop):
        self.__startValue = start
        self.__stopValue = stop
        
    def crawlerTime(self):
        startTime = datetime.date.today() - datetime.timedelta(self.__startValue)
        stopTime = datetime.date.today() - datetime.timedelta(self.__stopValue)
        pttFormatStart = str(startTime.month) + "/" +str(startTime.day)
        pttFormatStop = str(stopTime.month) + "/" + str(stopTime.day)
        return (pttFormatStart, pttFormatStop)


#爬蟲相關方法
#__init__內為目標網站、網址前綴、迴圈執行之flag
#setWeb用來更改目標網站
#getCertified為取得ptt 18禁認證，回傳為取得認證後之網頁
#getSoup為利用beautifulSoup取得網頁資訊，回傳值為網頁之html碼
#getNextPage用來取得上一頁，回傳值為上一頁之網址
#getArticaleUrl用來取得所有符合條件之文章連結，回傳值為存有所有網址的list
class crawlerWeb:
    def __init__(self):
        self.__targetWeb = 'https://www.ptt.cc/bbs/Beauty/index.html'
        self.__prefixUrl = 'https://www.ptt.cc'
        self.__flag = -1
        
    def setWeb(self, web):
        self.__targetWeb = web
        
    def getCertified(self):
        response = requests.get(self.__targetWeb)
        response = requests.get(self.__targetWeb, cookies = {'over18':'1'})
        return response
    
    def getSoup(self):
        resp = crawlerWeb.getCertified(self)
        return BeautifulSoup(resp.text, 'html.parser')
    
    def getNextPage(self, soup):
        btn = soup.select('div.btn-group > a')
        upPageHref = btn[3]['href']
        nextPageUrl = self.__prefixUrl + upPageHref
        return nextPageUrl
    
    def getArticleUrl(self, startTime, stopTime):
        articleLink = list()
        soup = crawlerWeb.getSoup(self)
        while self.__flag!=0:
            articleDate = soup.select('div.date')
            articleContent = soup.select('div.title')
            
            for i in range(len(articleDate)):
                if (str(articleDate[i]).find(startTime) != -1 and articleContent[i].select_one('a')!=None):
                    articleUrl = self.__prefixUrl + articleContent[i].select_one('a').get('href')
                    articleLink.append(articleUrl)
                elif (str(articleDate[i]).find(stopTime)!=-1):
                    self.__flag = 0
            
            crawlerWeb.setWeb(self, crawlerWeb.getNextPage(self, soup))
            soup = crawlerWeb.getSoup(self)
        return articleLink

#走訪儲存的文章連結list，並從文章擷取爬取目標
#regularNum用於正則表示法，IP寫法為 數字.數字.數字.數字，藉此規律來篩選出符合的目標
#regularURL用於正則表示法，圖片的網址表達方式是規律的，藉此來篩選出符合的目標
#author、title、date都存在於html語法中mainInform 底下
#author、title、date的值在html語法中mainValue底下
#ip在span.f2底下
#推 和 噓/-> 在span底下，他們的class分別為 hl push-tag 和 f1 hl push-tag
#getIP、getPIC 回傳值分別為取得IP值和圖片網址
#count 回傳值為推和噓的數量
#retrieveMain 用於統整所有爬取資料，並以list形式回傳
class retrieveInformation:
    def __init__(self):
        self.__regularNum = "\d\.?\d*"
        self.__regularURL = r'^https?://(i.)?(m.)?imgur.com'
        self.__mainInform = "div.article-metaline"
        self.__mainValue = "span.article-meta-value"
        self.__ip = "span.f2"
        self.__push = ['span', 'hl push-tag']
        self.__shh = ['span', 'f1 hl push-tag']
        
    def getIP(self, soup):
        ipList = re.findall(self.__regularNum, str(soup.select(self.__ip)[0].string))
        return '.'.join(ipList)
    
    def getPIC(self, soup):       
        for i in soup.find(id='main-content').findAll('a'):
            if re.match(self.__regularURL, i['href']):
                return i['href']
    
    def count(self, soup):
        push = len(soup.find_all(self.__push[0], class_=self.__push[1]))
        down = soup.find_all(self.__shh[0], class_=self.__shh[1])
        allDown = list()
        for i in down:
            allDown.append(str(i.string).strip())
        shh = allDown.count("噓")
        return (push, shh)
    
    def retrieveMain(self, soup):
        crawler_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
        picURL = retrieveInformation.getPIC(self, soup)
        getInform = soup.select(self.__mainInform)
        if(picURL != None and len(getInform)!=0):
            author = getInform[0].select(self.__mainValue)[0].string
            title = getInform[1].select(self.__mainValue)[0].string
            date = getInform[2].select(self.__mainValue)[0].string
            ip = retrieveInformation.getIP(self, soup)
            push, shh = retrieveInformation.count(self, soup)
            return [crawler_time, author, title, date, ip, picURL, push, shh]
           


#建立crawlerTime物件，取得爬取的時間
#建立crawlerWeb物件，取得文章連結list
#建立retrieveInformation物件，用於處理爬取所有文章及相關內容
#allInform用來儲存從retrieveMain回傳之list，使其形成二維陣列，方便之後寫入csv
#設定檔案儲存位置與檔名
#因在爬取過程中不知為何出現None值，因此先透過filter篩去None再寫入csv
if __name__ == '__main__':
    crawlerTime = crawlerTimeSet()    
    crawler = crawlerWeb()
    retrieve = retrieveInformation()
    allInform = list()
    filePath = 'D:/crawlerResult/' + str(datetime.date.today()) + "_crawlerResult.csv"
    
    start, stop = crawlerTime.crawlerTime()
    articleLink = crawler.getArticleUrl(start, stop)
    
    for link in articleLink:
        crawler.setWeb(link)
        soup = crawler.getSoup()
        allInform.append(retrieve.retrieveMain(soup))
    
    allInform = list(filter(lambda element: element is not None, allInform))
    
    with open(filePath, 'w', newline='', encoding = 'utf_8_sig') as csvfile:
        writer = csv.writer(csvfile) 
        writer.writerow(['爬取時間','作者','標題','發文時間','發文IP','第一張圖片網址','推數','噓數'])
        writer.writerows(allInform)