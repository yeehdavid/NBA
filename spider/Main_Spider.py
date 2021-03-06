from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pymysql
import datetime
import time
from selenium import webdriver

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='344126509', db='NBA', charset='utf8')
cur = conn.cursor()
HOUR = 100


# --------------------------------------------------------------------------------------------------------------
class sina_spider():
    # 开始登录----------------------------------------------------------------------------------------------
    def __init__(self):
        self.dic = {'lanqiudatu': 2432009827, 'lanqiujiqiaojiaoxue': 2494935602, 'hupulanqiu': 1642292081,
                    'lanqiujiaoxueluntan': 2357832895,'lantianxia':1901333207,
                    'zhibobalanqiu': 3171897472,
                    'lanqiudalishi': 2302617634, 'zhiguanyulanqiu': 5508233899, 'weiguanlanqiu': 5635855696}
        self.driver = webdriver.PhantomJS(executable_path='/home/david/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self.driver.implicitly_wait(30)
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)
        self.driver.get('https://m.weibo.cn/')
        time.sleep(4)
        login_url_btn = self.driver.find_element_by_class_name("btnWhite")
        login_url_btn.click()
        time.sleep(4)

        self.driver.find_element_by_id('loginName').send_keys("344126509@qq.com")

        self.driver.find_element_by_id('loginPassword').send_keys('wo344126509ni')

        self.driver.find_element_by_id('loginAction').click()
        print('weibo spider start success')
        time.sleep(4)

    # 登录结束----------------------------------------------------------------------------------------------


    def get_weibo(self, id):
        try:
            self.driver.get('https://m.weibo.cn/u/' + str(id))
            time.sleep(5)

            card = self.driver.find_elements_by_class_name('weibo-main')[1]  # 得到第一条非置顶微博
            title = card.find_element_by_class_name('weibo-text')

            title.click()
            time.sleep(3)
            # 至此，driver进去第一条微博的页面
        except Exception as e :
            print(e)
            return

        try:

            try:
                article = self.driver.find_element_by_class_name('weibo-rp')
                # 先判断这条微博是不是转发的，如果是，那就pass

            except:

                try:  # 尝试假设这是一条带图片的微博
                    title = self.driver.find_element_by_class_name('weibo-text')
                    title_text = title.text
                    # -----------------------------------------------判断是否已经存在
                    cur.execute("SELECT title FROM MainAPP_zimeiti_article WHERE title=%s", (title_text))
                    if len(cur.fetchall()[0:100]) != 0:
                        return
                    # -----------------------------------------------
                    media = self.driver.find_element_by_class_name('media-b')

                    img_src_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                    img_count = 0
                    for img in media.find_elements_by_tag_name('img'):
                        img_src_list[img_count] = img.get_attribute('src')
                        img_count += 1
                    #--------------------------------------------------
                    user_img = spider.driver.find_element_by_tag_name('img').get_attribute('src')
                    user_name = spider.driver.find_elements_by_class_name('m-text-cut')[0].text
                    #--------------------------------------------------
                    cur.execute(
                        "INSERT INTO MainAPP_zimeiti_article (title,created_time,url,video_url,img_src_1,img_src_2,img_src_3,img_src_4,img_src_5,img_src_6,img_src_7,img_src_8,img_src_9,img_count,user_img,user_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (title_text, datetime.datetime.now(), 0, 0, img_src_list[0], img_src_list[1], img_src_list[2],
                         img_src_list[3], img_src_list[4], img_src_list[5], img_src_list[6], img_src_list[7],
                         img_src_list[8], img_count,user_img,user_name))  # 将这场比赛插入到数据库当中
                    cur.connection.commit()

                    time.sleep(3)

                    # print(driver.current_url)

                except:  # 这是一条视频微博

                    title = self.driver.find_element_by_class_name('weibo-text')
                    title_text = title.text
                    # --------------------------------------------------
                    user_img = spider.driver.find_element_by_tag_name('img').get_attribute('src')
                    user_name = spider.driver.find_elements_by_class_name('m-text-cut')[0].text
                    # --------------------------------------------------
                    url = self.driver.current_url

                    video_start_btn = self.driver.find_element_by_class_name('f-bg-img')  # 找到开始播放视频的按钮

                    background_img_src_style = video_start_btn.get_attribute('style')  # 得到视频的背景缩略图
                    img_src = background_img_src_style[22:][:-2]
                    #print(img_src)
                    video_start_btn.click()  # 点击开始播放视频
                    time.sleep(2)  # 等待视频窗口加载
                    video_window = self.driver.find_element_by_tag_name('video')  # 弹出视频窗口后，找到视频的标签
                    video_url = video_window.get_attribute('src')  # 从这个标签得到视频的原始URL
                    #print(video_url)

                    if 'm3u8' in str(video_url):  # 当视频是m3u8格式的时候，直接跳过
                        return

                    img_src_list = [img_src, 0, 0, 0, 0, 0, 0, 0, 0]
                    img_count = 1

                    cur.execute(
                        "INSERT INTO MainAPP_zimeiti_article (title,created_time,url,video_url,img_src_1,img_src_2,img_src_3,img_src_4,img_src_5,img_src_6,img_src_7,img_src_8,img_src_9,img_count,user_img,user_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (title_text, datetime.datetime.now(), url, video_url, img_src_list[0], img_src_list[1],
                         img_src_list[2],
                         img_src_list[3], img_src_list[4], img_src_list[5], img_src_list[6], img_src_list[7],
                         img_src_list[8], img_count,user_img,user_name))  # 将这场比赛插入到数据库当中
                    cur.connection.commit()

        except Exception as e0:
            print(e0)

    def get_a_video_url(self, url):
        try:
            self.driver.get(url)

            time.sleep(5)
            title = self.driver.find_element_by_tag_name('title').text
            if '出错啦' in str(title):
                cur.execute("DELETE FROM MainAPP_zimeiti_article WHERE url=%s",url)
                cur.connection.commit()
                return False
            video_start_btn = self.driver.find_element_by_class_name('f-bg-img')  # 找到开始播放视频的按钮

            video_start_btn.click()  # 点击开始播放视频
            time.sleep(2)  # 等待视频窗口加载
            video_window = self.driver.find_element_by_tag_name('video')  # 弹出视频窗口后，找到视频的标签
            video_url = video_window.get_attribute('src')  # 从这个标签得到视频的原始URL
            return video_url
        except:
            return False

    def update_video_url(self):

        cur.execute("SELECT url FROM MainAPP_zimeiti_article WHERE url<>'0' ORDER BY -id")
        L = cur.fetchall()[0:30]

        for l in L:
            try:
                time.sleep(10)
                print(l[0])
                #print(selenium_get_bsobj(l[0]))
                new_video_url = self.get_a_video_url(l[0])
                if new_video_url == False:
                    print('can not open :',l[0])

                    continue
                cur.execute("UPDATE MainAPP_zimeiti_article SET video_url=%s WHERE url=%s",
                            (new_video_url, l[0]))
                cur.connection.commit()
            except Exception as e:
                # cur.execute("DELETE * FROM MainAPP_zimeiti_article WHERE url=%s")
                print(e)


# --------------------------------------------------------------------------------------------------------------
def selenium_get_bsobj(url):
    try:
        driver = webdriver.PhantomJS(executable_path='/home/david/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        driver.set_page_load_timeout(40)  # 设置页面最长加载时间为40s
        driver.get(url)
        time.sleep(3)
        # print(driver.find_element_by_id('body').text)

        # driver.get_screenshot_as_file('01.png')  # 保存网页截图
        sou = driver.page_source

        # b  = BeautifulSoup(sou)
        # print(driver.find_element_by_class_name('game-item'))
        driver.quit()

        return BeautifulSoup(sou, 'lxml')
    except:
        driver.quit()


# --------------------------------------------------------------------------------------------------------------
def Hoop_Latest_News():
    url = 'https://voice.hupu.com/nba'

    try:
        ht = urlopen(url, timeout=10)
        bsobj = BeautifulSoup(ht.read(), 'lxml')
    except:
        print('cant get the hoop html')
        return

    try:

        for i in bsobj.find_all('a', href=re.compile('https://voice.hupu.com/nba/')):  # 获取最新动态
            if 'target' not in i.attrs:
                continue

            else:

                try:
                    cur.execute("SELECT id FROM MainAPP_hoop_latest_news WHERE title = %s", (i.string))
                    The_ID = cur.fetchone()[0]

                    # 如果这条新闻不在set当中那就进行存储操作
                    # 此处代码将新闻主要信息存入数据库中
                    # print(i.attrs['href'],i.string)
                except:
                    print('can`t get hoopnew,it is a new ,i will insert into my table')
                    cur.execute("INSERT INTO MainAPP_hoop_latest_news (title,url,created_time) VALUES (%s,%s,%s)",
                                (i.string, i.attrs['href'], datetime.datetime.now()))
                    cur.connection.commit()
                    print('insert success')
                    #
                    # print(time.time())
                # print('插入数据完毕：', datetime.datetime.now())
                break
    except Exception as e:
        print(e)


# --------------------------------------------------------------------------------------------------------------
def NBA_Official_News():
    url = 'http://china.nba.com/news/'
    try:
        ht = urlopen(url, timeout=10)
        bsobj = BeautifulSoup(ht, 'lxml', from_encoding="gb18030")
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
                    print('can`t get NBA`Boardnew,it is a new,i will insert into my table')
                    cur.execute("INSERT INTO MainAPP_board_news (title,url,img_src,created_time) VALUES (%s,%s,%s,%s)",
                                (i.span.string, i.attrs['href'], i.img.attrs['src'], datetime.datetime.now()))
                    cur.connection.commit()
                    print('insert success')
                break

        for i in bsobj.findAll('a', href=re.compile('http://nbachina.qq.com/a/')):
            if i.span is not None and len(i.attrs) == 2:
                try:
                    cur.execute("SELECT id FROM MainAPP_latest_news WHERE title = %s",
                                (i.span.next_sibling.next_sibling.string))
                    The_ID = cur.fetchone()[0]
                except:
                    print('can`t get latestnew,it is a new,i will insert')
                    cur.execute("INSERT INTO MainAPP_latest_news (title,url,created_time) VALUES (%s,%s,%s)",
                                (i.span.next_sibling.next_sibling.string, i.attrs['href'], datetime.datetime.now()))
                    cur.connection.commit()
                    print('insert success')
                break


    except Exception as e:

        print(e)


# --------------------------------------------------------------------------------------------------------------
def Videos_98():
    url = 'http://www.nba98.com/nbalx/'
    try:

        bsobj = selenium_get_bsobj(url)

    except:

        print('cant get 98nba html')
        return

    try:

        for i in bsobj.findAll('a', href=re.compile('/nbalx/')):

            if len(i.attrs) == 2 and i.strong is None:  # 筛选出最近一场比赛的URL链接，并且插入到数据库
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
                        if re.match('http://www.', j['href']) or re.match('http://changyan.kuaizhan.com/', j['href']):
                            continue
                        else:

                            cur.execute(
                                "INSERT INTO MainAPP_lx_part (title,url,Belong_id,created_time) VALUES (%s,%s,%s,%s)",
                                (j.string, j['href'], The_ID, datetime.datetime.now()))  # 将这场比赛的每节比赛插入到数据库当中
                            cur.connection.commit()

                            # print(j.string,j['href'],The_ID)
                break
                # ---------------------------------------------
    except Exception as e:
        print(e)


# --------------------------------------------------------------------------------------------------------------
def jrs_zhibo():
    global HOUR
    now_hour = str(datetime.datetime.now())[11:13]
    if now_hour == HOUR:
        return
    HOUR = now_hour
    url = 'http://nba.tmiaoo.com/body.html'
    # try:
    try:
        bsobj = selenium_get_bsobj(url)
        cur.execute("TRUNCATE TABLE MainAPP_jrs;")
        cur.connection.commit()
        for i in bsobj.findAll('a'):
            # print(i['href'])#比赛链接
            # print(i.div.font.string)#比赛类型
            # print(i.div.next_sibling.string) #比赛时间
            # print(i.img['src'])#一队的标志
            # print(i.span.string )#一队的名字
            # print(i.div.next_sibling.next_sibling.next_sibling.next_sibling.span.string)#二队名字
            # print(i.div.next_sibling.next_sibling.next_sibling.next_sibling.img['src'])#二队标志

            cur.execute(
                "INSERT INTO MainAPP_jrs (url,game_tag,game_time,first_team_logo,first_team_name,second_team_name,second_team_logo,created_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (i['href'], i.div.font.string, str(i.div.next_sibling.string).strip(), i.img['src'], i.span.string,
                 i.div.next_sibling.next_sibling.next_sibling.next_sibling.span.string,
                 i.div.next_sibling.next_sibling.next_sibling.next_sibling.img['src'],
                 datetime.datetime.now()))  # 将这场比赛插入到数据库当中
            cur.connection.commit()


    except Exception as e:

        print(e)


# ----------------------------------------------------------------------------------------------


while True:


    try:
        spider = sina_spider()
        spider.update_video_url()
        for k, value in spider.dic.items():
            time.sleep(20)
            print('try:',value)
            spider.get_weibo(value)
        spider.driver.quit()
    except Exception as e:
        print('spider can not login')
        print(e)
        pass


    time.sleep(20)

    Hoop_Latest_News()
    time.sleep(25)

    NBA_Official_News()
    time.sleep(25)

    Videos_98()
    time.sleep(25)
    jrs_zhibo()
