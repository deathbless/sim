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

def findText(html):
    t = 0
    while html.find(searchText,t) != -1:
        t = html.find(searchText,t)
        end = html.find('"',t+10)
        str = html[t:end]
        print str
        t = t + 1


def getList(num):
    pass

if __name__ == '__main__':
    test()
    pass
