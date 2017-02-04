import re
import requests
import traceback
from bs4 import BeautifulSoup,SoupStrainer

Text = '[12月]  求片求助貼'
pattern = re.compile(r"^\[[\d月]{1,3}]{1,2}\s*[求片助貼]{5}$")
pattern2 = re.compile(r"[\d]{5,9}")
key_word = str(input("Enter key word: "))
Dict = {}
List1 = []
List2 = []  # All url
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}
proxy = {
    'http': 'socks5://127.0.0.1:1084'
}


class __Query:
    def __init__(self):
        self.session = requests.session()
        self.tech_url = "http://t66y.com/thread0806.php?fid=7"

    def show_url(self):     #获取求助帖url
        s = self.session
        r = s.get(self.tech_url,headers = headers,proxies = proxy)
        soup = BeautifulSoup(r.content,'lxml',parse_only=SoupStrainer('td',{'style': "text-align:left;padding-left:8px"}))
        for i in soup.contents[2:9]:
            if re.match(pattern,i.h3.font.get_text()):
                List1.append(i)
        fin_url = "http://t66y.com/" + List1[0].a["href"]
        pattern3 = re.compile(r"^(http://t66y.com/htm_data/7)/([\d]{3,5})/([\d]{6,8}).html")
        List2.append(fin_url)
        Dict['full'] = fin_url
        Dict['code'] = re.match(pattern3,fin_url).group(3)
        return fin_url

    def count(self,url):
        s = self.session
        try:
            r = s.get(url,proxies = proxy,headers=headers)
            soup = BeautifulSoup(r.content,'lxml',parse_only=SoupStrainer('a',{'id': "last"}))
            page = re.findall(r"[\d]{1,3}$",soup.contents[1]['href'])
            print("Total pages: %s" % page[0])
            for a in ["http://t66y.com/read.php?tid={}&page={}".format(Dict['code'],i) for i in range(2,int(page[0]) + 1)]:
                List2.append(a)
        except:
            traceback.print_exc()


    def look_up(self,url,*kw):
        s = self.session
        r = s.get(url, headers=headers,proxies=proxy)
        soup = BeautifulSoup(r.content,'lxml',parse_only=SoupStrainer('table',{'style': "border-top:0"}))
        #print(soup.contents[9].find_all('div',{'class': "tpc_content"})[0].get_text())       # SoupStrainer advanced usage
        try:
            for a in soup.contents[1:]:
                '''if a.find_all('div',{'class': "tpc_content"})[0].find_all('blockquote'):
                    print("Quote: {}Post: {}".format(
                            a.find_all('div',{'class': "tpc_content"})[0].find_all('blockquote')[0],
                            a.find_all('div',{'class': "tpc_content"})[0].find_all('br')
                            ))'''
                # print(type(a.find_all('div',{'class': "tpc_content"})[0].get_text()))
                for arg in kw:
                    if arg in a.find_all('div',{'class': "tpc_content"})[0].get_text():
                        print("Found: {} \n URL: {}".format(a.find_all('div',{'class': "tpc_content"})[0].get_text(),url))
        except:
            traceback.print_exc()


try:
    test = __Query()
    test.count(test.show_url())
    # test.look_up('http://t66y.com/read.php?tid=2242822&page=22','白咲碧')
    for i in List2:
        test.look_up(i,key_word)
except:
    traceback.format_exc()
