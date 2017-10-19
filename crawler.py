import re
import urllib.request
import urllib

from collections import deque

picture = deque()
visited_page = set()
visited_pictures = set();


data={}
data['word']=''#此处输入搜索关键词

url_values = urllib.parse.urlencode(data)
url_former = "https://www.pixiv.net/search.php"
url_former0 = "?s_mode=s_tag&word="
nextpage = url_former + url_former0 + url_values
pagenumber = 1
while nextpage:#nextpage不为空就一直继续
    visited_page|={nextpage}
    pagenumber = pagenumber + 1
    next_page_end = "?word=adf&order=date_d&p="+pagenumber
    nextpage = nextpage 
    try:
        urlop = urllib.request.urlopen(nextpage,timeout = 10)
    except:
        continue


