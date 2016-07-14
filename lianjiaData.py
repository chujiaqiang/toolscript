# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

import re
import urllib2
import math
import codecs

class House(object):
    id = None;
    area = None
    area02 = None
    href = None
    title = None
    address_xiaoqu = None
    address_info = None
    flood = None
    area = None
    totalPrice = None
    unitPice = None
    def __init(self):
        self.id = ""
        self.area = "";
        self.area02 = ""
        self.href = ""
        self.title = ""
        self.address_xiaoqu = ""
        self.address_info = ""
        self.flood = ""
        self.area = ""
        self.totalPrice = ""
        self.unitPice = ""
    def __str__(self):
        return unicode('%s#%s#%s#%s#%s#%s#%s#%s#%s#%s' % (self.area, self.area02, self.id, self.title, self.totalPrice, self.unitPice,
                                                       self.address_xiaoqu, self.flood, self.address_info, self.href
                                               ))

    def __unicode__(self):
        return unicode(self.__str__())


domain='http://bj.lianjia.com/'
url = domain + '/ershoufang/'

def getHtmlContent(url):
    headers = {
        'Host':r'bj.lianjia.com',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

    req = urllib2.Request(url, headers=headers)
    return urllib2.urlopen(req).read()


def get_all_xiaoqu_info():
    html_doc = getHtmlContent(url)

    soup = BeautifulSoup(html_doc, 'html.parser')

    def has_href_but_title(tag):
        return tag.has_attr('href') and not tag.has_attr('title')
    #得到所有区域
    all_xiao_list=[]
    for item in soup.find(attrs={"data-role": "ershoufang"}).find_all('a'):
        #print "%s|%s" % (item.get('href') , item.string)
        quyu_url=item.get('href')
        quyu_html_doc = getHtmlContent(domain + quyu_url)
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





def getHouseInfoForOneURL(quyuInfo):
    house_list=[]
    #xiaoqu_url=r'http://bj.lianjia.com/ershoufang/changying/p1/'
    xiaoqu_url=quyuInfo[0]
    xiao_html_doc= getHtmlContent(xiaoqu_url)
    xiaoqu_soup = BeautifulSoup(xiao_html_doc, 'html.parser')
    total_house=int(xiaoqu_soup.find("h2",class_="total fl").find('span').string)

    if total_house == 0:
        print 'no hourse fouund'
        return house_list
        
    if total_house > 3000:
        print '3000+ hourse fouund, need split it into small pages'
        return house_list
    print 'total:%d' % total_house

    total_page = math.ceil(total_house / 30.0)
    for page_index in range(1, int(total_page)+1):
        page_url= '%s/pg%d' % (xiaoqu_url,page_index)
        print page_url
        page_html_doc= getHtmlContent(page_url)
        page_soup = BeautifulSoup(page_html_doc, 'html.parser')
        #print page_url

        for house_info in  page_soup.find('ul',class_='listContent').find_all('div', class_="info"):
            house = House()
            house.area= quyuInfo[1]
            house.area02= quyuInfo[2]
            house.href = house_info.find('a').get('href')
            house.id = re.findall(r'/([0-9]*?).html', house.href)[0]
            house.title = house_info.find('a').string
            house.address_xiaoqu = house_info.find('div', class_="houseInfo").a.string
            house.address_info = house_info.find('div', class_="houseInfo").a.next_sibling
            house.flood = house_info.find('div', class_="flood").find('div', class_="positionInfo").span.next_sibling
            #house.area = house_info.find('div', class_="flood").find('div', class_="positionInfo").a.string
            house.totalPrice = house_info.find('div', class_="totalPrice").span.string
            house.unitPice = house_info.find('div', class_="unitPrice").span.string
            house_list.append(house)

    return house_list

def getOnePage(url, page):
    #page_url = '%s/pg%d' % (r'http://bj.lianjia.com/ershoufang/andingmen/', 6)
    page_url = '%s/pg%d' % (url, page)
    print page_url
    page_html_doc = getHtmlContent(page_url)
    page_soup = BeautifulSoup(page_html_doc, 'html.parser')
    # print page_url

    for house_info in page_soup.find('ul', class_='listContent').find_all('div', class_="info"):

        house = House()

        house.href = house_info.find('a').get('href')
        house.id = re.findall(r'/([0-9]*?).html', house.href)[0]
        house.title = house_info.find('a').string
        house.address_xiaoqu = house_info.find('div', class_="houseInfo").a.string
        house.address_info = house_info.find('div', class_="houseInfo").a.next_sibling
        house.flood = house_info.find('div', class_="flood").find('div', class_="positionInfo").span.next_sibling
        house.area = house_info.find('div', class_="flood").find('div', class_="positionInfo").a.string
        house.totalPrice = house_info.find('div', class_="totalPrice").span.string
        house.unitPice = house_info.find('div', class_="unitPrice").span.string
        print unicode(house)


if __name__ == '__main__':
    file = codecs.open('lianjia.txt','wb','utf-8')

    quyu_list = get_all_xiaoqu_info()
    for quyu in quyu_list:
        print '%s %s :(%s)' % (quyu[0], quyu[1], quyu[2])
        house_list = getHouseInfoForOneURL(quyu)
        for house in house_list:
            file.write(unicode(house) + '\n')
    file.close()


