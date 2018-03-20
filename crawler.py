#encoding:utf-8
from time import sleep

import re
import urllib.request
import urllib

from selenium import webdriver
from selenium.common.exceptions import TimeoutException



picture_star=[]
picture = []

driver = webdriver.Chrome("C:\\Users\hasee\AppData\Local\Programs\Python\Python35\Scripts\chromedriver.exe")#path to chromedriver
driver.delete_all_cookies()

driver.get("https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index")

print("start now")
elem=driver.find_element_by_xpath(".//*[@id='LoginComponent']/form/div[1]/div[1]/input")
elem.send_keys("2823694360@qq.com")
elem = driver.find_element_by_xpath(".//*[@id='LoginComponent']/form/div[1]/div[2]/input")
elem.send_keys("lm710115")
driver.find_element_by_xpath(".//*[@id='LoginComponent']/form/button").click()
sleep(5)
'''
cookie= driver.get_cookies()
print(cookie)
'''
    #当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
search_key_word=input("plz input the search keyword")

url_former = "https://www.pixiv.net/search.php"

pagenumber = int(input("plz input first pagenumber"))
last_page = int(input("plz input last pagenumber"))#结束的页数

save_path = 'D:\\test_'+search_key_word+str(pagenumber)+'-'+str(last_page)+'.txt'
f_obj = open(save_path, 'w', encoding="utf-8")
f_obj.write('\n')
while pagenumber<=last_page:


    next_page_end = "?word="+search_key_word+"&order=date_d&p="+str(pagenumber)
    nextpage = url_former+next_page_end
    print("now it's scanning page " + str(pagenumber))
    try:
        driver.get(nextpage)
    except:
        continue

    print("now it's scanning page " + str(pagenumber))

    page_content = driver.page_source

    print("now it's scanning page " + str(pagenumber))
    #读取所有的图片地址到一个集合，然后读取所有的star数目到一个集合
    pic_pattern = re.compile('/bookmark_detail.php\?illust_id=\d+?".+?</a>')#寻找全部图片
    star_pic_pattern = re.compile('/bookmark_detail.php\?illust_id=(\d+?)".+?</a>')#寻找有star的图片
    star_pattern = re.compile('_bookmark-icon-inline"></i>(.+?)</a>')#寻找star数目
    print("now it's scanning page " + str(pagenumber))

    for y in star_pattern.findall(page_content):
        picture_star.append(int(y))
    print("now it's scanning page "+str(pagenumber))
    picturenumber = 0

    for x in pic_pattern.findall(page_content):
        print(x)
        l = star_pattern.findall(x)
        print(l)
        #如果l非空，意味着有star，进行判断
        if l:
            if int(l[0])>200:
                k = star_pic_pattern.findall(x)
                print(k[0])
                f_obj.write("www.pixiv.net"+k[0]+" "+l[0]+"\n")

    picture_star.clear()
    picture.clear()
    pagenumber = pagenumber+1

f_obj.close()