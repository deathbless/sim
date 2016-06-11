__author__ = 'deathbless'
import cookielib
import urllib2
import gzip
import StringIO

def login(name, password):
    pass


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
    url3 = ""



if __name__ == '__main__':
    test()