#coding:utf-8
import sys, os, cStringIO, urllib2, Image
from django.shortcuts import render_to_response, HttpResponse
from models import Channel,Cinema,CinemaCode,MoviePrice
from bs4 import BeautifulSoup
from datetime import *
from time import sleep
from strLikeness import strcmp

import urllib,re


# Create your views here.
   
    
#爬取淘宝电影所有电影院 
def saveCinema (request): 
    cinemas = Cinema.objects.filter(cinemacode__channel__id=1)

    channel=Channel.objects.get(id=2)
    html = urllib.urlopen('https://dianying.taobao.com/cinemaList.htm').read()
    soup = BeautifulSoup(html)
    div = soup.find_all('div',class_='sortbar-more J_cinemaMore')[0]
    url = div['data-ajax']
    params = div['data-param'].split('&')
    param_page = [p for p in params if 'pageLength' in p][0]
    pageSize = param_page.split('=')[1]

    for page in range(int(pageSize)):
        sleep(5)
        html = urllib.urlopen(url + '?page=' + str(page + 1)).read()
        soup2 = BeautifulSoup(html)
        for li in soup2.find_all('li'):
            link = li.find_all('a')[1]
            href = link['href']
            code = re.compile('(cinemaId=\d+)').findall(href)[0].split('=')[1]
            name = link.text
            address = li.find_all('span',class_='limit-address')[0].text.strip()

            #匹配address和数据库中最相似的一个
            dicts = {}
            for exist in cinemas:
                diff = strcmp(exist.address, address)
                dicts[diff] = exist

            minKey = min([k for k in sorted(dicts.keys())])
            cinema = dicts[minKey]             
            cinemaCode = CinemaCode(code=code,cinema=cinema,channel=channel)
            cinemaCode.save()
            print 'name:' + name + ' code:' + code
    return HttpResponse("save success! ")


    
#爬取淘宝电影各电影院各电影每天的价格
def savePrice (request):
    channel = Channel.objects.get(code='taobao')
    MoviePrice.objects.filter(channel=channel).delete()
    cinemaCodeList = CinemaCode.objects.filter(channel=channel)
    for cinemaCode in cinemaCodeList:
        sleep(5)
        html = urllib.urlopen('https://dianying.taobao.com/cinemaDetailSchedule.htm?cinemaId=' + cinemaCode.code).read()
        soup = BeautifulSoup(html)
        tags = soup.find_all('div', class_='select-tags')[0]
        for a in tags.find_all('a'):
            name = a.text
            params = a['data-param'].split('&')
            showId = [p for p in params if 'showId' in p][0]
            sleep(5)
            movieDetail = urllib.urlopen('https://dianying.taobao.com/cinemaDetailSchedule.htm?showDate=2016-07-24&cinemaId=' + cinemaCode.code + '&showId=' + showId).read()
            soup2 = BeautifulSoup(movieDetail)

            tbody = soup2.find('tbody')
            priceDict = {}
            try:
                for tr in tbody.find_all('tr'):
                    language_type = tr.find(class_='hall-type').text.strip()
                    price = tr.find(class_='now').text
                    priceDict[price] = language_type  #找到该电影有几种不同的价格
            except BaseException, e:
                print 'error occured!',e


            for k,v in priceDict.iteritems():
                print k + '-' + v
                mp = MoviePrice(name=name,language_type=v,price=k,channel=channel,cinema=cinemaCode.cinema)
                mp.save()
                           
    return HttpResponse("save success! ")