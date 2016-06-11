__author__ = 'deathbless'
import cookielib
import urllib2
import gzip
import StringIO

def login(name, password):
    pass

f = open("test.txt", "w")

def test():
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
    url3 = "http://www.thesimsresource.com/mytsr/account/account"
    req3 = urllib2.Request(url3)
    response3 = opener.open(req3)
    data = response3.read()
    f.write(data)


if __name__ == '__main__':
    test()