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
#--------------------------------------------------------------------------------------------------------------

def selenium_get_bsobj(url):

    driver = webdriver.PhantomJS(executable_path='/home/david/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.set_page_load_timeout(180)  # 设置页面最长加载时间为40s
    driver.get(url)
    time.sleep(1)
    #print(driver.find_element_by_id('body').text)

    #driver.get_screenshot_as_file('01.png')  # 保存网页截图
    sou = driver.page_source

    #b  = BeautifulSoup(sou)
    #print(driver.find_element_by_class_name('game-item'))
    driver.quit()

    return BeautifulSoup(sou,'lxml')

def selenium_get_source(url):

    driver = webdriver.PhantomJS(executable_path='/home/david/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.set_page_load_timeout(40)  # 设置页面最长加载时间为40s
    print('start get')
    driver.get(url)
    time.sleep(1)
    print('sleep')
    #print(driver.find_element_by_id('body').text)

    #driver.get_screenshot_as_file('01.png')  # 保存网页截图
    sou = driver.page_source

    #b  = BeautifulSoup(sou)
    #print(driver.find_element_by_class_name('game-item'))
    driver.quit()

    return sou

#--------------------------------------------------------------------------------------------------------------
def Hoop_Latest_News():

    url = 'https://voice.hupu.com/nba'

    try:
        ht = urlopen(url)
        bsobj = BeautifulSoup(ht.read(), 'lxml')
    except:
        print('cant get the hoop html')
        return

    try:



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
    except:
        print('hoop_latest_news caozuo shibai')





def NBA_Official_News():



    url = 'http://china.nba.com/news/'
    try:
        ht = urlopen(url)
        bsobj = BeautifulSoup(ht, 'lxml',fromEncoding="gb18030")
    except:
        print('cant get the NBA offical html')
        return
    try:


        for i in bsobj.findAll('a', href=re.compile("http://china.nba.com/a/")):  # 获取Board
            if 'target' in i.attrs and len(i.attrs) == 2 and i.span is not None:
                try:
                    cur.execute("SELECT id FROM MainAPP_board_news WHERE title = %s", (i.span.string))
                    The_ID = cur.fetchone()[0]
                except:
                    print('can`t get NBA`Board——new,it is a new,i will insert into my table')
                    cur.execute("INSERT INTO MainAPP_board_news (title,url,img_src,created_time) VALUES (%s,%s,%s,%s)",
                                (i.span.string, i.attrs['href'], i.img.attrs['src'], datetime.datetime.now()))
                    cur.connection.commit()
                    print('insert success')
                break

        for i in bsobj.findAll('a', href=re.compile('http://nbachina.qq.com/a/')):
            if i.span is not None and len(i.attrs) == 2:
                try:
                    cur.execute("SELECT id FROM MainAPP_latest_news WHERE title = %s", (i.span.next_sibling.next_sibling.string))
                    The_ID = cur.fetchone()[0]
                except:
                    print('can`t get latest——new,it is a new,i will insert')
                    cur.execute("INSERT INTO MainAPP_latest_news (title,url,created_time) VALUES (%s,%s,%s)",
                        (i.span.next_sibling.next_sibling.string, i.attrs['href'], datetime.datetime.now()))
                    cur.connection.commit()
                    print('insert success')
                break

    except:
        print('cant caozuo shuju ')






def Videos_98():

    url = 'http://www.nba98.com/nbalx/'
    try:

        bsobj = selenium_get_bsobj(url)

    except:

        print('cant get 98nba html')
        return


    try:


        for i in bsobj.findAll('a',href = re.compile('/nbalx/')):

            if len(i.attrs) == 2 and i.strong is None:#筛选出最近一场比赛的URL链接，并且插入到数据库
                try:
                    cur.execute("SELECT id FROM MainAPP_lx WHERE title = %s", (i.string))  # 获取获取的比赛的id，出错说明数据库不存在
                    The_ID = cur.fetchone()[0]
                except:
                    print('can`t get lx ,it is a new ,i will insert')
                    # print(i.string,i['href'])
                    cur.execute("INSERT INTO MainAPP_lx (title,created_time) VALUES (%s,%s)",
                                (i.string, datetime.datetime.now()))  # 将这场比赛插入到数据库当中
                    cur.connection.commit()
                    print('insert success')
                    cur.execute("SELECT id FROM MainAPP_lx WHERE title = %s", (i.string))  # 获取刚刚插入的比赛的id
                    The_ID = cur.fetchone()[0]
                    # --------------------------------------------以下代码的作用是打开某场比赛的链接，看到这场比赛的每节比赛的链接
                    print('open the game html')

                    bs = selenium_get_bsobj('http://www.nba98.com' + i['href'])
                    print('open success')
                    for j in bs.findAll('a', href=re.compile('http')):
                        if re.match('http://www.', j['href']) or re.match('http://changyan.kuaizhan.com/',j['href']):
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
        print('98nba caozuo shibai')


def jrs_zhibo():
    global HOUR
    now_hour = str(datetime.datetime.now())[11:13]
    if now_hour ==  HOUR:
        return
    HOUR=now_hour
    url='http://nba.tmiaoo.com/body.html'
    #try:
    try:
        bsobj = selenium_get_bsobj(url)
        cur.execute("TRUNCATE TABLE MainAPP_jrs;")
        cur.connection.commit()
        for i in bsobj.findAll('a'):

            #print(i['href'])#比赛链接
            #print(i.div.font.string)#比赛类型
            #print(i.div.next_sibling.string) #比赛时间
            #print(i.img['src'])#一队的标志
            #print(i.span.string )#一队的名字
            #print(i.div.next_sibling.next_sibling.next_sibling.next_sibling.span.string)#二队名字
            #print(i.div.next_sibling.next_sibling.next_sibling.next_sibling.img['src'])#二队标志

            cur.execute("INSERT INTO MainAPP_jrs (url,game_tag,game_time,first_team_logo,first_team_name,second_team_name,second_team_logo,created_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                        (i['href'],i.div.font.string,str(i.div.next_sibling.string).strip(),i.img['src'],i.span.string,
                         i.div.next_sibling.next_sibling.next_sibling.next_sibling.span.string,
                         i.div.next_sibling.next_sibling.next_sibling.next_sibling.img['src'],
                         datetime.datetime.now()))  # 将这场比赛插入到数据库当中
            cur.connection.commit()

    except :
        print('cant get jrs bsobj')


while True:

    Hoop_Latest_News()
    time.sleep(35)

    NBA_Official_News()
    time.sleep(35)

    Videos_98()
    time.sleep(35)
    jrs_zhibo()