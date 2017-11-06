#coding:utf-8
import sys, os, cStringIO, urllib2, Image
from django.shortcuts import render_to_response, HttpResponse
from models import Channel,Cinema,CinemaCode,MoviePrice
from bs4 import BeautifulSoup
from datetime import *
from time import sleep

import urllib,re


# Create your views here.

"""                
if u'国金百丽宫影院' not in name:
    sleep(5)
    html2 = urllib.urlopen('http://sh.meituan.com/shop/' + code).read()
    soup2 =  BeautifulSoup(html2)     
    tel_div = soup2.find_all('div',class_='biz-base-info')[0].find_all('div',class_='field-group')[1]
    print tel_div
    reg = re.compile('^\d+(-)?\d+((-)?|(\s*/\s*)?)\d+$')
    tel = tel_div.find(text=reg)
    print tel
"""

"""
#爬取美团网所有电影名
def saveMovie (request):
    channel=Channel.objects.get(id=1)
    Movie.objects.all().delete()
    MovieCode.objects.filter(channel=channel).delete()
    html = urllib.urlopen('http://sh.meituan.com/dianying').read()
    soup = BeautifulSoup(html)
    for li in soup.find_all('ul', class_='reco-slides__slides')[0].find_all('li'):
        for movie in li.find_all('a',class_='btn'):
            name = movie['title']
            href = movie['href']
            code = href[href.rfind('/') + 1:href.find('#')]
            m = Movie(name=name)
            m.save()
            mc = MovieCode(code=code,movie=m,channel=channel)
            mc.save()
            print 'name:' + name + ' code:' + code
    return HttpResponse("save success! ")
"""
   
    
#爬取美团网所有电影院
def saveCinema (request):
    channel=Channel.objects.get(id=1)
    for n in range(10):
        sleep(5)
        html = urllib.urlopen('http://sh.meituan.com/dianying/cinemalist/all/all/page' + str(n+1)).read()
        soup = BeautifulSoup(html)
        for n, cinema in enumerate(soup.find(id='J-cinema-info-list').find_all('div', class_='J-cinema-item cinema-item cf')):           
            link = cinema.find_all('h4')[0].find_all('a',class_='link--black__green')[0]
            href = link['href']
            code = href[href.rfind('/') + 1:]
            name = link.text
            address = cinema.find_all('dd')[0].text.strip()
      
            c = Cinema(name=name,address=address,city=u'上海')
            c.save()
            cinemaCode = CinemaCode(code=code,cinema=c,channel=channel)
            cinemaCode.save()
            print 'name:' + name + ' code:' + code
    return HttpResponse("save success! ")


    
#爬取美团网各电影院各电影每天的价格
def savePrice (request):
    channel = Channel.objects.get(code='meituan')
    MoviePrice.objects.filter(channel=channel).delete()
    cinemaCodeList = CinemaCode.objects.filter(channel=channel)
    for cinemaCode in cinemaCodeList:
        sleep(5)
        html = urllib.urlopen('http://sh.meituan.com/shop/' + cinemaCode.code).read()
        soup = BeautifulSoup(html)
        for movieInfo in soup.find_all('div',class_='movie-info'):
            name = movieInfo.find('a')['title']
            href = movieInfo.find('a')['href'].split('?')[0]
            movieCode = (re.compile('\/\w*\/(\d+)').search(href).groups())[0]
            cover_url = [k.find_all('img')[0]['src'] for k in soup.findAll("div", attrs={"data-movie": True}) if k['data-movie'] == movieCode][0]    
            print cover_url
            #showtime = movieInfo.find(class_='show-time').find_all('a')[0]:          
            #release_date = showtime['data-date']

            try:
                table = movieInfo.find_all('table')[0]
                priceDict = {}
                for n, tr in enumerate(table.find_all('tr')):
                    if n > 0:                          
                        try:                                                 
                            #start_time = tr.find(class_='start-time').text
                            #end_time = tr.find(class_='end-time').text
                            #release_time = '-'.join((start_time, end_time))                           
                            #video_hall = tr.find_all('td')[2].text
                            language_type = tr.find_all('td')[1].text
                            price = ''
                            if tr.find(class_='price'):
                                strong = tr.find(class_='price')                
                                for p in strong.find_all('i'):
                                    url = re.compile('\((.*)\)').findall(p['style'].split(';')[0])[0]
                                    position = p['style'].split(';')[1].split(':')[1].replace(' ', '')
                                    wh = re.compile('(-?\d+)').findall(position)
                                    num = parseNum('http:' + url, abs(int(wh[0])), abs(int(wh[1])))
                                    if num == 10:
                                       num = '.'
                                    price += str(num)
                                #price += tr.find(class_='price').text
                            else:
                                price += 'price not found'

                            #print price
                            priceDict[price] = language_type  #找到该电影有几种不同的价格
                        except BaseException, e:
                            print 'error occured!',e   
            except BaseException, e:
                print 'error occured!',e

            for k,v in priceDict.iteritems():
                print k + '-' + v
                mp = MoviePrice(name=name,url=cover_url,language_type=v,price=k,channel=channel,cinema=cinemaCode.cinema)                
                mp.save()
                                        
    return HttpResponse("save success! ")
            

#解析美团网图片式价格
def parseNum(url, x, y):
    print url
    img = Image.open(cStringIO.StringIO(urllib2.urlopen(url).read()))

    cg = img.crop((x, y + 2, x + 7, y + 12)).resize((20,30)).convert('L')
    diffs = [0,0,0,0,0,0,0,0,0,0,0]

    for yi in range(30):
        for xi in range(20):
            imgDir = os.path.join(sys.path[0],'movie/numbers')
            for i in os.listdir(imgDir):
                if os.path.isfile(os.path.join(imgDir,i)) and i.endswith('.png') :
                    img_i = Image.open(os.path.join(imgDir,i))
                    if cg.getpixel((xi, yi)) != img_i.getpixel((xi, yi)):
                        diffs[int(i.split('.')[0])] += 1

    return diffs.index(min(diffs))