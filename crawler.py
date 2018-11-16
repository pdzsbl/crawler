#encoding:utf-8
from time import sleep
import wx
import re
import urllib.request
import urllib
import time
from threading import *
from wx.lib.pubsub import pub

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import selenium
class TestThread(Thread):
     def __init__(self,bp,ep,k,id,pw):
          #线程实例化时立即启动
          Thread.__init__(self)
          self.bp=bp
          self.ep = ep
          self.k = k
          self.id = id
          self.pw =pw
          self.start()
     def run(self):
          #线程执行的代码
          crawler(self.bp,self.ep,self.k,self.id,self.pw)

class Crawlerframe(wx.Frame):
    def __init__(self, parent, id, fname):
        wx.Frame.__init__(self, parent, id,fname , size=(400, 300))

        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour(wx.WHITE)
        """button"""

        self.close = wx.Button(mainPanel, id+1787,  "开始查询",pos=(5,90),size = (70,30))
        self.Bind(wx.EVT_BUTTON, self.OnButtonBeginCrawl, self.close)
        self.beginp = wx.TextCtrl(mainPanel, 8000, "", (250, 15), size=(100, 30), style=wx.TE_PROCESS_ENTER)
        self.endp = wx.TextCtrl(mainPanel, 9000, "", (250, 45), size=(100, 30), style=wx.TE_PROCESS_ENTER)
        self.serachkeyword = wx.TextCtrl(mainPanel, 10000, "", (250, 75), size=(100, 30), style=wx.TE_PROCESS_ENTER)
        self.yourid = wx.TextCtrl(mainPanel, 11000, "", (250, 105), size=(100, 30), style=wx.TE_PROCESS_ENTER)
        self.yourpw = wx.TextCtrl(mainPanel, 12000, "", (250, 135), size=(100, 30), style=wx.TE_PROCESS_ENTER)
        self.result = wx.TextCtrl(mainPanel, 900, "", (5, 20), size=(150, 60), style=wx.TE_PROCESS_ENTER)
        self.bp = wx.StaticText(mainPanel, 901, "开始页数", (180, 20))
        self.ep = wx.StaticText(mainPanel, 902, "结束页数", (180, 50))
        self.sk = wx.StaticText(mainPanel, 903, "英文搜索词", (180, 80))
        self.mail = wx.StaticText(mainPanel, 904, "注册邮箱", (180, 110))
        self.pw = wx.StaticText(mainPanel, 905, "密码", (180, 140))
        pub.subscribe(self.updateDisplay, "result")

    def updateDisplay(self,msg):
        t = msg
        self.result.SetValue(msg)

    def OnButtonBeginCrawl(self,event):
        self.result.SetValue("正在准备，请稍后")
        beginp_ = int(self.beginp.GetValue())
        endp_ = int(self.endp.GetValue())
        searchkeyw = self.serachkeyword.GetValue()
        id = self.yourid.GetValue()
        pw = self.yourpw.GetValue()
        TestThread(beginp_,endp_,searchkeyw,id,pw)


def crawler(beginp,endp,serachkeyword,yourid,yourpw):

    picture_star=[]
    picture = []

    opt = selenium.webdriver.ChromeOptions()

    #opt.set_headless()


    driver = webdriver.Chrome("./chromedriver.exe",options=opt)#path to chromedriver
    driver.set_page_load_timeout(30)
    driver.delete_all_cookies()
    try:
        driver.get('https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=accounts&view_type=page&ref=')
    except TimeoutException:
        print('time out after 30 seconds when loading page')
        driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
    #print("start now")
    elem=driver.find_element_by_xpath(".//*[@id='LoginComponent']/form/div[1]/div[1]/input")
    elem.send_keys(yourid)
    elem = driver.find_element_by_xpath(".//*[@id='LoginComponent']/form/div[1]/div[2]/input")
    elem.send_keys(yourpw)
    driver.find_element_by_xpath(".//*[@id='LoginComponent']/form/button").click()
    sleep(5)
    '''
    cookie= driver.get_cookies()
    print(cookie)
    '''
        #当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
    #search_key_word=input("plz input the search keyword")
    search_key_word = serachkeyword
    url_former = "https://www.pixiv.net/search.php"

    #pagenumber = int(input("plz input first pagenumber"))
    #last_page = int(input("plz input last pagenumber"))#结束的页数

    pagenumber = beginp
    last_page = endp

    save_path = 'test_'+search_key_word+str(pagenumber)+'-'+str(last_page)+'.txt'
    f_obj = open(save_path, 'w', encoding="utf-8")
    #f_obj.write('\n')
    while pagenumber<=last_page:


        next_page_end = "?word="+search_key_word+"&order=date_d&p="+str(pagenumber)
        nextpage = url_former+next_page_end
        #print("now it's scanning page " + str(pagenumber))
        print(pagenumber,"sent")
        wx.CallAfter(pub.sendMessage, "result", msg="检索第"+str(pagenumber)+"页")
        try:
            driver.get(nextpage)
        except:
            continue

        #print("now it's scanning page " + str(pagenumber))

        page_content = driver.page_source

        #print("now it's scanning page " + str(pagenumber))
        #读取所有的图片地址到一个集合，然后读取所有的star数目到一个集合
        pic_pattern = re.compile('/bookmark_detail.php\?illust_id=\d+?".+?</a>')#寻找全部图片
        star_pic_pattern = re.compile('/bookmark_detail.php\?illust_id=(\d+?)".+?</a>')#寻找有star的图片
        star_pattern = re.compile('_bookmark-icon-inline"></i>(.+?)</a>')#寻找star数目
        #print("now it's scanning page " + str(pagenumber))

        for y in star_pattern.findall(page_content):
            picture_star.append(int(y))
        #print("now it's scanning page "+str(pagenumber))
        picturenumber = 0

        for x in pic_pattern.findall(page_content):
            #print(x)
            l = star_pattern.findall(x)
            #print(l)
            #如果l非空，意味着有star，进行判断
            if l:
                if int(l[0])>200:
                    k = star_pic_pattern.findall(x)
                    #print(k[0])
                    f_obj.write("https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+k[0]+" "+l[0]+"\n")
                    f_obj.flush()
        picture_star.clear()
        picture.clear()
        pagenumber = pagenumber+1

    f_obj.close()
    wx.CallAfter(pub.sendMessage, "result", msg="已完成,\n可打开文件查询")

if __name__ == "__main__":
    app = wx.App(0)
    c_frame = Crawlerframe(None,3333,"pixiv")
    c_frame.Show(True)
    app.MainLoop()
