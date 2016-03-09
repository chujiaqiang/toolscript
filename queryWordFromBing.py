# -*- coding:utf-8 -*-

import re
import urllib

word = 'security'
url = "http://www.iciba.com/" + word

content = urllib.urlopen(url).read()

print word

# 查询读音
str = r"<div class='base-speak'>(.*?)</div>"

items = re.findall(str, content, re.S)

for item in items:
    print '英：', re.findall("<span>英(.*)</span>", item)[0]
    print '美：', re.findall("<span>美(.*)</span>", item)[0]

# 查询释义
str = r"<ul class='base-list switch_part' >(.*?)</ul>"
items = re.findall(str, content, re.S)[0]
# print items
print '***************************************************'
items02 = re.findall(r"<li>\s*<span class='prop'>(.*?)</span>\s*<p>\s*(.*?)</p>", items, re.S)
for item in items02:
    print item[0], item[1].replace(' ', '')

exit(0)
