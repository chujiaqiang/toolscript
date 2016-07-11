#! -*- coding: utf8 -*-

import urllib
import re

#get word's info from http://dict.cn
url=r'http://dict.cn/home'
html=urllib.urlopen(url).read()
#print html

f = open("C:\\Users\\IBM_ADMIN\\Desktop\\Hadoop- The Definitive Guide, 4th Edition.txt")
dict = {}
for line in f.readlines():
    line = line.lower().strip()
    
    p = re.compile(r'\W+')
    arry = p.split(line)
    for word in arry:
        if dict.has_key(word):
            dict[word] += 1
        else:
            dict[word] = 1
f.close()

f =open("C:\\Users\\IBM_ADMIN\\Desktop\\Hadoop- The Definitive Guide, 4th Edition.lst",'wb+')
del dict[""]
for item in sorted(dict.iteritems(), key = lambda asd:asd[1], reverse = True):
    worditem = "%s\t%d\n" % (item[0],item[1])
    f.write(worditem)
    #print worditem
    #url='%s%s' % (r'http://dict.cn/home',item[0])
    #html=urllib.urlopen(url).read()
f.close()



    
