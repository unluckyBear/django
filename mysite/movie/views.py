#coding:utf-8
import sys, os, cStringIO, urllib2, Image
from django.shortcuts import render_to_response, HttpResponse
from models import Channel,Cinema,Movie,MoviePrice
from bs4 import BeautifulSoup
from datetime import datetime

import urllib,re


# Create your views here.
def add (request):
    channels=Channel.objects.all()
    return render_to_response('add.html',{'channels':channels})

def saveMovie (request):
    channel=Channel.objects.get(id=1)
    html = urllib.urlopen('http://sh.meituan.com/dianying').read()
    soup = BeautifulSoup(html)
    for movie in soup.find_all('ul', class_='reco-slides__slides')[0].find_all('li')[0].find_all('a',class_='btn'):
        name = movie['title']
        href = movie['href']
        code = href[href.rfind('/') + 1:href.find('#')]
        m = Movie(name=name,code=code,channel=channel)
        m.save()
    return HttpResponse("save success! ")
    
    
def saveCinema (request):
    channel=Channel.objects.get(id=1)
    for n in range(2):       
        html = urllib.urlopen('http://sh.meituan.com/dianying/cinemalist/pudongxinqu/all/page' + str(n+1)).read()
        soup = BeautifulSoup(html)
        for cinema in soup.find(id='J-cinema-info-list').find_all('div', class_='J-cinema-item cinema-item cf'):
            link = cinema.find_all('h4')[0].find_all('a',class_='link--black__green')[0]          
            href = link['href']
            code = href[href.rfind('/') + 1:]
            name = link.text
            address = cinema.find_all('dd')[0].text.strip()
            c = Cinema(name=name,code=code,address=address,channel=channel)
            c.save()
    return HttpResponse("save success! ")

def saveMeiTuanMovie (request):
    MoviePrice.objects.all().delete()
    channel = Channel.objects.get(code='meituan')
    cinemaList = channel.cinema_set.all()
    for cinema in cinemaList:
        html = urllib.urlopen('http://sh.meituan.com/shop/' + cinema.code).read()
        soup = BeautifulSoup(html)
        for movieInfo in soup.find_all('div',class_='movie-info'):
            name = movieInfo.find('a')['title']          
            for n, showtime in enumerate(movieInfo.find(class_='show-time').find_all('a')):          
                release_date = showtime['data-date']
                table = movieInfo.find_all('table')[n]
                tr = table.find_all('tr')[1]
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
                            url = re.compile('(http.*png)').findall(p['style'].split(';')[0])[0]
                            position = p['style'].split(';')[1].split(':')[1].replace(' ', '')
                            wh = re.compile('(-?\d+)').findall(position)
                            num = parseNum(url, abs(int(wh[0])), abs(int(wh[1])))
                            if num == 10:
                               num = '.'
                            price += str(num)
                        price += tr.find(class_='price').text
                    else:
                        price += 'price not found'
                    mp = MoviePrice(name=name,release_date=release_date,language_type=language_type,price=price,channel=channel,cinema=cinema)
                    print price
                    mp.save()
                except BaseException, e:
                    print 'error occured!',e                       
    return HttpResponse("save success! ")
            

def search (request):
    return render_to_response('search.html')


def list (request):
    channel = Channel.objects.get(code='meituan')
    movieName = request.GET.get('movie_name')
    cinemaName = request.GET.get('cinema_name')
    cinema = Cinema.objects.get(name=cinemaName,channel=channel)
    #movie = Movie.objects.get(name=movieName,channel=channel)
    movieList = MoviePrice.objects.filter(name=movieName,channel=channel,cinema=cinema)
    movieList = [movie for movie in movieList if datetime.strptime(movie.release_date.strftime("%Y-%m-%d") + " " + movie.release_time.split('-')[0], "%Y-%m-%d %H:%M") > datetime.now()]
    return render_to_response('list.html',{'movies':movieList})


#解析美团网图片式价格
def parseNum(url, x, y):
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