from bs4 import BeautifulSoup
from urllib.request import urlopen
import threading
import re
import pymysql
import datetime
import time

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='344126509', db='NBA', charset='utf8')
cur=conn.cursor()

BOARD = str()#board he latest分别保存当前最新的一条新闻
LATEST = str()
HOOP_S = str()
Videos98 = str()
#--------------------------------------------------------------------------------------------------------------
try:
    cur.execute("SELECT title from MainAPP_lx where id/created_time=(select max(id/created_time) from MainAPP_lx)")
    Videos98 = cur.fetchone()[0]
except:
    pass

try:
    cur.execute("SELECT title from MainAPP_hoop_latest_news where id/created_time=(select max(id/created_time) from MainAPP_hoop_latest_news)")
    HOOP_S = cur.fetchone()[0]
except:
    pass

try:
    cur.execute("SELECT title from MainAPP_board_news where id/created_time=(select max(id/created_time) from MainAPP_board_news)")
    BOARD = cur.fetchone()[0]
except:
    pass

try:
    cur.execute("SELECT title from MainAPP_latest_news where id/created_time=(select max(id/created_time) from MainAPP_latest_news)")
    LATEST = cur.fetchone()[0]
except:
    pass
#--------------------------------------------------------------------------------------------------------------
def Hoop_Latest_News():

    url = 'https://voice.hupu.com/nba'
    global HOOP_S


    try:
        #print('开始URLopen：',datetime.datetime.now())
        ht = urlopen(url)
        #print('URLopen完毕：', datetime.datetime.now())
        #print('开始Beautiful：', datetime.datetime.now())
        bsobj = BeautifulSoup(ht.read(),'lxml')
        #print('Beautiful完毕：', datetime.datetime.now())


        for i in bsobj.find_all('a' ,href = re.compile('https://voice.hupu.com/nba/')):#获取最新动态
            if 'target' not in i.attrs:
                continue

            else:
                if i.string != HOOP_S:#如果这条新闻不在set当中那就进行存储操作
                    HOOP_S = i.string
                    #此处代码将新闻主要信息存入数据库中
                    #print(i.attrs['href'],i.string)
                    cur.execute("INSERT INTO MainAPP_hoop_latest_news (title,url,created_time) VALUES (%s,%s,%s)",
                                (HOOP_S, i.attrs['href'], datetime.datetime.now()))
                    cur.connection.commit()
                    #
                    #print(time.time())
                #print('插入数据完毕：', datetime.datetime.now())
                break
    except:
        pass

    time.sleep(10)



def NBA_Official_News():

    global BOARD
    global LATEST

    url = 'http://china.nba.com/news/'


    try:
        ht = urlopen(url)
        bsobj = BeautifulSoup(ht, 'lxml')
        print('ok')
        for i in bsobj.findAll('a', href=re.compile("http://china.nba.com/a/")):  # 获取Board
            if 'target' in i.attrs and len(i.attrs) == 2 and i.span is not None:
                if BOARD!=i.span.string:#如果当前保存的最新新闻和网页中的第一条新闻不一样，说明有新内容
                    BOARD = i.span.string#将要保存的内容放入
                    print(i.attrs['href'], i.img.attrs['src'], BOARD)
                    cur.execute("INSERT INTO MainAPP_board_news (title,url,img_src,created_time) VALUES (%s,%s,%s,%s)",
                                (BOARD, i.attrs['href'], i.img.attrs['src'], datetime.datetime.now()))
                    cur.connection.commit()
                break

        for i in bsobj.findAll('a', href=re.compile('http://nbachina.qq.com/a/')):
            if i.span is not None and len(i.attrs) == 2:
                if LATEST!=i.span.next_sibling.next_sibling.string:
                    LATEST = i.span.next_sibling.next_sibling.string
                    print(i.attrs['href'], LATEST)
                    cur.execute("INSERT INTO MainAPP_latest_news (title,url,created_time) VALUES (%s,%s,%s)",
                        (LATEST, i.attrs['href'], datetime.datetime.now()))
                    cur.connection.commit()
                break

    except:
        print('bu')
        time.sleep(5)

    time.sleep(10)



def Videos_98():

    url = 'http://www.nba98.com/nbalx/'
    global Videos98

    try:
        ht = urlopen(url)
        bsobj = BeautifulSoup(ht,'lxml')

        for i in bsobj.findAll('a',href = re.compile('/nbalx/')):

            if len(i.attrs) == 2 and i.strong is None:#筛选出最近一场比赛的URL链接，并且插入到数据库
                try:
                    cur.execute("SELECT id FROM MainAPP_lx WHERE title = %s", (i.string))  # 获取获取的比赛的id，出错说明数据库不存在
                    The_ID = cur.fetchone()[0]
                except:

                    # print(i.string,i['href'])
                    cur.execute("INSERT INTO MainAPP_lx (title,created_time) VALUES (%s,%s)",
                                (i.string, datetime.datetime.now()))  # 将这场比赛插入到数据库当中
                    cur.connection.commit()
                    cur.execute("SELECT id FROM MainAPP_lx WHERE title = %s", (i.string))  # 获取刚刚插入的比赛的id
                    The_ID = cur.fetchone()[0]
                    # --------------------------------------------以下代码的作用是打开某场比赛的链接，看到这场比赛的每节比赛的链接
                    h = urlopen('http://www.nba98.com' + i['href'])
                    bs = BeautifulSoup(h, 'lxml')
                    for j in bs.findAll('a', href=re.compile('http')):
                        if re.match('http://www.', j['href']):
                            continue
                        else:
                            cur.execute(
                                "INSERT INTO MainAPP_lx_part (title,url,Belong_id,created_time) VALUES (%s,%s,%s,%s)",
                                (j.string, j['href'], The_ID, datetime.datetime.now()))  # 将这场比赛的每节比赛插入到数据库当中
                            cur.connection.commit()

                            # print(j.string,j['href'],The_ID)
                break
                #---------------------------------------------
    except:
        pass
    finally:
        time.sleep(10)
        pass


while True:
    print(datetime.datetime.now())
    Hoop_Latest_News()
    time.sleep(15)
    NBA_Official_News()
    time.sleep(15)
    Videos_98()
    print(datetime.datetime.now())
    time.sleep(15)
