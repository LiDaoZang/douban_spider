import requests
from bs4 import BeautifulSoup
import pandas as pd

def GetBookList(link):
    res=requests.get(link,headers=headers,allow_redirects = False)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,"html.parser")
    dates=[]

    for date in soup.select('span[class="date"]'):
        dates.append(str(date.text).replace('\n','').replace('读过',''))

    # tags=[]
    # for tag in soup.select('span[class="tags"]'):
    #     tags.append(str(tag.text))

    books=[]
    for book in soup.select('a[title]'):
        books.append(str(book.text).replace('\n','').replace(' ',''))
    for i in range(len(books)-len(dates)):#去掉爬取到的多余的自定义标签名称
        books.pop()

    results={}
    results['book']=books
    results['date']=dates
    # results['tag']=tags

    return results

start_link = ' '#这个单引号之间填入你的豆瓣，想读网页端的网址

headers = {
"Host": "book.douban.com",

"Referer":" ",#填入你豆瓣个人界面的网址

'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

}

depth = 37 #你的页数

lists={'BOOK':[],'DATE':[]}

for i in range(depth):
    link= start_link + str(15*i)
    llist=GetBookList(link)
    lists['BOOK'].extend(llist['book'])
    lists['DATE'].extend(llist['date'])
    # lists['TAG'].extend(llist['tag'])

pd.set_option('display.max_rows', None)
df_book=pd.DataFrame(lists)
df_book.to_csv('MyWishBooks.csv')