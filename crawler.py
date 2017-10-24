#encoding:utf-8
from time import sleep

import re
import urllib.request
import urllib

from selenium import webdriver

picture_star=[]
picture = []

driver = webdriver.Chrome("C:\\Users\hasee\AppData\Local\Programs\Python\Python35\Scripts\chromedriver.exe")
driver.get("https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index")
#放弃让爬虫自己登陆，改为手动登陆后等待爬虫帮我爬网页
print("start now")
sleep(5)#这里根据网络连接状态自己决定停多少秒，反正如果卡升天的话等待加载的时间基本是允许你输入加登录的，所以也可以去掉这一行

search_key_word='lovelive'#此处输入搜索关键词

url_former = "https://www.pixiv.net/search.php"
url_former0 = "?s_mode=s_tag&word="
nextpage = url_former + url_former0 + search_key_word
pagenumber = 20#开始的页数
last_page = 40#结束的页数

save_path = 'D:\\test'+str(pagenumber)+'-'+str(last_page)+'.txt'
f_obj = open(save_path, 'w', encoding="utf-8")
f_obj.write('\n')
while pagenumber<=last_page:


    next_page_end = "?word="+search_key_word+"&order=date_d&p="+str(pagenumber)
    nextpage = url_former+next_page_end

    try:
        driver.get(nextpage)
    except:
        continue

    try:
        page_content = driver.page_source
    except:
        continue
    #读取所有的图片地址到一个集合，然后读取所有的star数目到一个集合
    pic_pattern = re.compile('href="/member_illust.php\?mode=medium&amp;illust_id=\d+?".+?</figcaption>')#寻找全部图片
    star_pic_pattern = re.compile('href="(/member_illust.php\?mode=medium&amp;illust_id=\d+?)".+?bookmark-badge"></i>.+?</a>')#寻找有star的图片和star数目
    star_pattern = re.compile('bookmark-badge"></i>(.+?)</a>')
    for y in star_pattern.findall(page_content):
        picture_star.append(int(y))
    print("now it's scanning page "+str(pagenumber))
    picturenumber = 0

    for x in pic_pattern.findall(page_content):
        l = star_pattern.findall(x)
        #如果l非空，意味着有star，进行判断
        if l:
            if int(l[0])>200:
                k = star_pic_pattern.findall(x)
                f_obj.write("www.pixiv.net"+k[0]+" "+l[0]+"\n")

    picture_star.clear()
    picture.clear()
    pagenumber = pagenumber+1
print(over)
f_obj.close()