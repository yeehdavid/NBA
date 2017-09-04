from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pymysql
import datetime
import time
from selenium import webdriver

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='344126509', db='NBA', charset='utf8')
cur=conn.cursor()
HOUR = 100


def Hoop_Latest_News():

    url = 'https://voice.hupu.com/nba'


    ht = urlopen(url)
    bsobj = BeautifulSoup(ht.read(), 'lxml')







    for i in bsobj.find_all('a' ,href = re.compile('https://voice.hupu.com/nba/')):#获取最新动态
        if 'target' not in i.attrs:
            continue

        else:

            try:
                cur.execute("SELECT id FROM MainAPP_hoop_latest_news WHERE title = %s", (i.string))
                The_ID = cur.fetchone()[0]

                #如果这条新闻不在set当中那就进行存储操作
                #此处代码将新闻主要信息存入数据库中
                #print(i.attrs['href'],i.string)
            except:
                print('can`t get hoop——new,it is a new ,i will insert into my table')
                cur.execute("INSERT INTO MainAPP_hoop_latest_news (title,url,created_time) VALUES (%s,%s,%s)",
                            (i.string, i.attrs['href'], datetime.datetime.now()))
                cur.connection.commit()
                print('insert success')
                #
                #print(time.time())
            #print('插入数据完毕：', datetime.datetime.now())
            break


Hoop_Latest_News()