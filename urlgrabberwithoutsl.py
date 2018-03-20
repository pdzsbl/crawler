import urllib.request
import urllib.parse
import http.cookiejar
import re
#login part
def getpostKey(opener,url):
    postKey=""
    content=opener.open(url).read().decode("utf-8")
    postkey=re.findall(r"<input.+?name=\"post_key\".+?>",content)[0].split(" ")[3].split("\"")[1]
    print(postkey)
    return postkey
BASE_URL = "https://www.pixiv.net/"
ToGetKeyURL = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
postURL = "https://accounts.pixiv.net/api/login?lang=zh"

Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
Origin = "https://accounts.pixiv.net"
Referer = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
Host = "accounts.pixiv.net"
cookie = http.cookiejar.CookieJar()
cookieHandle = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(cookieHandle)

header = \
    {
        "User-Agent": Agent,
        "Origin": Origin,
        "Referer": Referer,
        "Host": Host
    }

head = []

for key, value in header.items():
    head.append((key, value))

opener.addheaders = head


getInfo=getpostKey(opener, ToGetKeyURL)
post_data=\
        {
            "pixiv_id":"2823694360@qq.com",
            "password":"lm710115",
            #"captcha":"",
            #"g_recaptcha_response":"",
            "post_key":getInfo,
            #"source":"pc",
            #"ref":"wwwtop_accounts_index",
            #"return_to":"https://www.pixiv.net/",
         }
post_data=urllib.parse.urlencode(post_data,"utf-8")
print(post_data.encode("utf-8"))
if opener.open(postURL,post_data.encode("utf-8")).getcode()==200:
    print("Login Successfully")
else:
    print("Login failed")
print(opener)
#login part ends

search_key_word=input("plz input the search keyword")
url_former = "https://www.pixiv.net/search.php"
pagenumber = int(input("plz input first pagenumber"))
last_page = int(input("plz input last pagenumber"))
save_path = 'D:\\test_'+search_key_word+str(pagenumber)+'-'+str(last_page)+'1.txt'
f_obj = open(save_path, 'w', encoding="utf-8")
picture_star=[]
picture = []
while pagenumber<=last_page:
    next_page_end = "?word=" + search_key_word + "&order=date_d&p=" + str(pagenumber)
    nextpage = url_former + next_page_end
    print("now it's scanning page " + str(pagenumber))
    page_content = opener.open(nextpage).read().decode("utf-8")
    pic_pattern = re.compile('/bookmark_detail.php\?illust_id=\d+?".+?</a>')  # 寻找全部图片
    star_pic_pattern = re.compile('/bookmark_detail.php\?illust_id=(\d+?)".+?</a>')  # 寻找有star的图片
    star_pattern = re.compile('_bookmark-icon-inline"></i>(.+?)</a>')  # 寻找star数目
    print("now it's scanning page " + str(pagenumber))
    for y in star_pattern.findall(page_content):
        picture_star.append(int(y))
    print("now it's scanning page " + str(pagenumber))
    picturenumber = 0

    for x in pic_pattern.findall(page_content):
        l = star_pattern.findall(x)
        print(x)
        print(l)
        # if l is not empty, there's star here, so judge whether more than 200
        if l:
            if int(l[0]) > 200:
                k = star_pic_pattern.findall(x)
                print(k[0])
                f_obj.write("www.pixiv.net" + k[0] + " " + l[0] + "\n")

    picture_star.clear()
    picture.clear()
    pagenumber = pagenumber + 1

f_obj.close()