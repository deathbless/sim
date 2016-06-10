#coding=utf-8
__author__ = 'deathbless'


import cookielib,urllib2,urllib
import gzip
import StringIO
import sys
opener = urllib2.build_opener()
f = open("test.txt","w")

simUrl = "http://www.thesimsresource.com/downloads/browse/category/sims4-objects/"
searchText = "href=\"/downloads/details/category/sims4"


waitList = []

def test():
    userMainUrl = simUrl
    req = urllib2.Request(userMainUrl)
    resp = urllib2.urlopen(req)
    respHtml = resp.read()
    data = StringIO.StringIO(respHtml)
    gzipper = gzip.GzipFile(fileobj=data)
    html = gzipper.read()
    # print html
    # f.write(html)
    findText(html)


num = 1
def findText(html):
    t = 0
    num = 1
    front = "http://www.thesimsresource.com"
    while html.find(searchText,t) != -1:
        t = html.find(searchText,t)
        end = html.find('"',t+10)
        str = html[t:end]
        str = front + str[6:]
        waitList.append(str) # 添加进待爬去列表
        t = t + 1

    print waitList.__len__()
    for url in waitList:
        # print num, ":", url
        num = num + 1
        openUrl(url)
        pass




startTitle = '<div class="big-header">'
endTitle =  '<span class="icon-star star-big star-'

startAuthor = 'class="big-creator">'

def openUrl(url):
    global num
    userMainUrl = url
    req = urllib2.Request(userMainUrl)
    resp = urllib2.urlopen(req)
    respHtml = resp.read()
    data = StringIO.StringIO(respHtml)
    gzipper = gzip.GzipFile(fileobj=data)
    try:
        html = gzipper.read()
    except:
        html = respHtml
    # print html.find(startTitle), html.find(endTitle)
    if html.find(startTitle)!= -1 and html.find(endTitle)!= -1:
        title = html[html.find(startTitle) + startTitle.__len__():html.find(endTitle)]

        authorS = html.find(startAuthor)
        authorE = html.find('<',authorS + len(startAuthor))
        author = html[authorS + len(startAuthor):authorE]

        print num, ":", title.strip(), '[', author.strip(), ']'
    num = num + 1

def getList(num):
    pass

if __name__ == '__main__':
    test()
    pass
