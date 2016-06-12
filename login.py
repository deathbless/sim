__author__ = 'deathbless'
import cookielib
import urllib2
import gzip
import StringIO
import zipfile

def login(name, password):
    pass

f = open("test.txt", "w")

def saveFile(file_name, data):
    if data == None:
        return
    f = open(file_name, "wb")
    f.write(data)
    f.flush()
    f.close()


if __name__ == '__main__':
    test()