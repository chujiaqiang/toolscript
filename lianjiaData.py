# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

import re
import urllib
import urllib2
import math
import codecs

domain='http://bj.lianjia.com/'
url = domain + '/ershoufang/'

def get_all_xiaoqu_info():
    html_doc = urllib.urlopen(url).read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    def has_href_but_title(tag):
        return tag.has_attr('href') and not tag.has_attr('title')
    #得到所有区域
    all_xiao_list=[]
    for item in soup.find(attrs={"data-role": "ershoufang"}).find_all('a'):
        #print "%s|%s" % (item.get('href') , item.string)
        quyu_url=item.get('href')
        quyu_html_doc = urllib.urlopen(domain + quyu_url).read()
        quyu_soup = BeautifulSoup(quyu_html_doc, 'html.parser')

        for item02 in quyu_soup.find(attrs={"data-role": "ershoufang"}).find_all(has_href_but_title):
            xiaoqu_info=list()
            xiqu_url=domain + item02.get('href')
            #print '%s|%s|%s' % (item.get('href'), item.string,  item02.string)
            xiaoqu_info.append(domain + item02.get('href'))
            xiaoqu_info.append(item.string)
            xiaoqu_info.append(item02.string)
            all_xiao_list.append(xiaoqu_info)
    # for item in all_xiao_list:
    #     print '|'.join(item)
    return all_xiao_list


headers = {
        'Accept':r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':r'gzip, deflate',
        'Accept-Language':r'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection':r'keep-alive',
        'Host':r'bj.lianjia.com',
        'Referer':r'http://bj.lianjia.com/ershoufang/beiqijia',
        'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        #'Cookie':r'lianjia_uuid=18acab8e-de62-43a9-b3d4-962b28968ec7; _smt_uid=57219c21.42bc10ea; CNZZDATA1253477573=294732555-1461819878-http%253A%252F%252Fwww.baidu.com%252F%7C1467557395; _jzqa=1.598087999714383000.1461820449.1467148977.1467525301.10; _jzqy=1.1461820449.1465381613.3.jzqsr=baidu.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6; CNZZDATA1254525948=1894244370-1461815948-http%253A%252F%252Fwww.baidu.com%252F%7C1467557174; CNZZDATA1255633284=1405522112-1461816002-http%253A%252F%252Fwww.baidu.com%252F%7C1467556338; CNZZDATA1255604082=136337279-1461816253-http%253A%252F%252Fwww.baidu.com%252F%7C1467557177; _ga=GA1.2.433541691.1461820452; miyue_hide=%20index%20%20index%20%20index%20%20index%20%20index%20; _jzqx=1.1461823997.1462357481.2.jzqsr=bj%2Elianjia%2Ecom|jzqct=/ershoufang/rs%e5%8d%97%e5%b2%b8.jzqsr=bj%2Elianjia%2Ecom|jzqct=/ershoufang/yanjiao/; select_city=110000; all-lj=b3d70adee01740a6a0beb306d0f6f412; _jzqb=1.31.10.1467525301.1; _jzqc=1; _jzqckmp=1; lianjia_ssid=dedfe462-961f-4b4e-a935-1e170a4cf252; _qzja=1.1927253355.1461820449108.1467148976556.1467525301331.1467528966161.1467528974420.0.0.0.136.10; _qzjb=1.1467525301331.31.0.0.0; _qzjc=1; _qzjto=31.1.0; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1',
        'DN':'1',
        'Cache-Control': 'max-age=0'
}

def getHouseInfoForOneURL(quyuInfo):
    house_list=[]
    #xiaoqu_url=r'http://bj.lianjia.com/ershoufang/changying/p1/'
    xiaoqu_url=quyuInfo[0]
    xiao_html_doc= urllib.urlopen(xiaoqu_url).read()
    xiaoqu_soup = BeautifulSoup(xiao_html_doc, 'html.parser')
    total_house=int(xiaoqu_soup.find("h2",class_="total fl").find('span').string)

    if total_house == 0:
        print 'no hourse fouund'
        return house_list

    total_page = math.ceil(total_house / 30.0)
    for page_index in range(1, int(total_page)+1):
        page_url= '%s%d' % ('http://bj.lianjia.com/ershoufang/changying/p',page_index)
    #     print page_url
        house_info=dict()
        for house_info in  xiaoqu_soup.find('ul',class_='listContent').find_all('div', class_="info"):
            house_info['href']= house_info.find('a').get('href')
            house_info['title']= house_info.find('a').string
            house_info['address_xiaoqu']=house_info.find('div',class_="houseInfo").a.string
            house_info['address_info']= house_info.find('div',class_="houseInfo").a.next_sibling
            house_info['flood']= house_info.find('div',class_="flood").find('div',class_="positionInfo").span.next_sibling
            house_info['area']= house_info.find('div',class_="flood").find('div',class_="positionInfo").a.string
            house_info['totalPrice']= house_info.find('div',class_="totalPrice").span.string + house_info.find('div',class_="totalPrice").span.next_sibling
            house_info['unitPice']= house_info.find('div',class_="unitPrice").span.string
            house_info['area']= quyuInfo[1]
            house_info['area02']= quyuInfo[2]
            house_list.append(house_info)

    return house_list

file = codecs.open('lianjia.txt','wb','utf-8')

quyu_list = get_all_xiaoqu_info()
for quyu in quyu_list:
    print '%s %s :(%s)' % (quyu[0], quyu[1], quyu[2])
    house_list = getHouseInfoForOneURL(quyu)
    for house in house_list:
        house_str= '%s|%s|%s|%s|%s|%s|%s|%s|%s\n' % (
            house['area'], house['area02'],house['title'], house['address_xiaoqu'], house['address_info'],house['flood'], house['area'],house['totalPrice'],house['unitPice']
        )
        file.write(house_str)
file.close()


