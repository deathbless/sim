#coding=utf-8
__author__ = 'deathbless'


import cookielib
import urllib2
import gzip
import StringIO
import os

waitList = []  # 待爬取的mod的url集合
opener = None  # 带cookie的模拟浏览器
cookie = cookielib.MozillaCookieJar()  # cookie
l = []  # cookie集合

def getFile(url):
    """
    从url处获取图片的二进制
    :param url: 图片url
    :return: 二进制数据
    """
    try:
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        req = urllib2.Request(url)
        operate = opener.open(req)
        data = operate.read()
        return data
    except BaseException, e:
        print e
        return None

def saveFile(file_name, data):
    """
    保存图片
    :param file_name: 图片文件名
    :param data: 图片数据
    :return:
    """
    if data == None:
        return
    f = open(file_name, "wb")
    f.write(data)
    f.flush()
    f.close()

def login():
    """
    登录模块，带会员cookie登录
    :return: 登录器对象
    """
    global opener, l, cookie
    cookie = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    url = "http://www.thesimsresource.com:80/ajax.php?c=account&a=dologin&email=mfmiss%40hotmail.com&password=lopatinsky4012"
    req = urllib2.Request(url)
    response = opener.open(req)
    data = response.read()
    l = eval(data)
    url2 = "http://www.thesimsresource.com:80/ajax.php?c=account&a=init&key=" + l['LoginKey'] + "&mid=" + l['MemberID']
    req2 = urllib2.Request(url2)
    response2 = opener.open(req2)
    data = response2.read()
    return opener

def downloadPackage(url, filename):
    """
    具体下载package的方法，先下载gz文件再解压缩再改名删除其他的
    :param url: 下载的地址
    :param filename: 保存的名称
    :return:
    """
    itemId = url[url.find("/id/") + len("/id/"):url.find("/",url.find("/id/") + len("/id/"))]
    url4 = "http://www.thesimsresource.com:80/ajax.php?c=downloads&a=getdownloadurl&ajax=1&itemid=" + itemId + "&mid=3306870&lk=" + l['LoginKey']
    headers = {
        'Host': 'www.thesimsresource.com',
        'Proxy-Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'Referer':url,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    req4 = urllib2.Request(url4, headers=headers)
    response4 = opener.open(req4)
    respHtml = response4.read()
    data = StringIO.StringIO(respHtml)
    gzipper = gzip.GzipFile(fileobj=data)
    data = gzipper.read()
    before = '"url":"'
    end = '","s3filename":'
    realUrl = data[data.find(before) + len(before):data.find(end)]
    realUrl = realUrl.replace("\n", "")
    realUrl = realUrl.replace("\\", "")
    req5 = urllib2.Request(realUrl)
    response5 = opener.open(req5)
    data = response5.read()
    # urllib.urlretrieve("1.package", realUrl)
    saveFile("1.gz", data)
    gfile = open('1.gz', 'rb')
    g = gzip.GzipFile(mode="rb", fileobj=gfile)
    open(filename + ".package", "wb").write(g.read())
    gfile.close()
    os.remove("1.gz")

def openUrl(url):
    """
    打开指定页面，返回对应的html代码
    :param url:  要打开的页面的地址
    :return: 该地址的html代码
    """
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    respHtml = resp.read()
    data = StringIO.StringIO(respHtml)
    gzipper = gzip.GzipFile(fileobj=data)
    try:
        html = gzipper.read()
    except:
        html = respHtml
    return html

def getPage(num):
    """
    爬取列表页面获得具体mod的url
    :param num: 要爬取页面的数量
    :return: mod具体的url集合list
    """
    simUrlStart = "http://www.thesimsresource.com/downloads/browse/category/sims4-objects/page/"
    simUrlEnd = "/cnt/8748/"
    for i in range(1, num + 1):
        simUrl = simUrlStart + str(i) + simUrlEnd
        html = openUrl(simUrl)
        findMod(html)

    openMod()

def findMod(html):
    """
    从mod列表里面寻找到具体的mod的url
    :param html: mod列表代码
    :return:
    """
    t = 0
    urlStart = "http://www.thesimsresource.com"
    searchText = "href=\"/downloads/details/category/sims4"

    while html.find(searchText, t) != -1:
        t = html.find(searchText, t)
        end = html.find('"', t+10)
        str = html[t:end]
        str = urlStart + str[6:]
        waitList.append(str)  # 添加进待爬去列表
        t = t + 1

def openMod():
    """
    具体打开mod的url
    :return:
    """
    # print len(waitList)

    titleStart = '<div class="big-header">'
    titleEnd1 = '<span class="icon-star star-big star-'
    titleEnd2 = '</div>'
    authorStart = 'class="big-creator">'
    pictureStart = '<a href="/scaled/'
    pictureBefore = 'http://www.thesimsresource.com'

    for url in waitList:
        html = openUrl(url)
        title = "null"
        author = "null"
        titleSnum = html.find(titleStart)
        titleEnum = html.find(titleEnd1)
        if titleEnum == -1:
            titleEnum = html.find(titleEnd2, titleSnum)
        if titleSnum != -1 and titleEnum != -1:
            title = html[titleSnum + len(titleStart):titleEnum]
            title = title.strip()
            title = title.title()
            title = title.replace(" ", "")
        # 标题获取完成
        authorSnum = html.find(authorStart)
        authorEnum = html.find('<', authorSnum + len(authorStart))
        if authorSnum != -1 and authorEnum != -1:
            author = html[authorSnum + len(authorStart):authorEnum]
            author = author.strip()
            author = author.title()
            author = author.replace(" ", "")
        # 作者获取完成
        filename = '[' + author + ']' + title
        if filename not in os.listdir('.'):
            os.mkdir(filename)
        else:
            continue
        os.chdir(filename)
        print "now downloading " + filename + " ,please wait for a while"
        # 建立文件夹并进入完成
        jump = '<meta http-equiv="refresh" content="0.2;url=' + url + '">'
        web = open(filename + ".html", "w")
        web.write(jump)
        web.close()
        # 建立链接快捷方式完成
        num = 1
        pictureSnum = html.find(pictureStart)
        while pictureSnum != -1:
            pictureEnum = html.find('"', pictureSnum + len(pictureStart))
            picture = html[pictureSnum + 9:pictureEnum]
            pictureUrl = pictureBefore + picture
            data = getFile(pictureUrl)
            saveFile(title + '_' + str(num) + '.jpg', data)
            num = num + 1
            pictureSnum = html.find(pictureStart, pictureEnum)
        # 存储图片完成
        if str(cookie._cookies).find("3306870") == -1:
            continue  # 如果没有登录会员就鸽了下载
        downloadPackage(url, filename)
        os.chdir('..')  # 退出当前mod文件夹
        print title + " has done!"

if __name__ == '__main__':
    login()
    # os.chdir('..')
    # if 'mods' not in os.listdir('.'):
    #     os.mkdir('mods')
    # os.chdir("mods")
    # print "please input the number of page:"
    # num = raw_input()
    # getPage(int(num))
