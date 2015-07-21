#coding:utf-8
from django.shortcuts import render_to_response, HttpResponse
from models import Channel,Cinema,Movie,MoviePrice
from bs4 import BeautifulSoup
from datetime import datetime

import urllib


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
                for k, tr in enumerate(table.find_all('tr')):
                    if k > 0:
                        try:                                                 
                            start_time = tr.find(class_='start-time').text
                            end_time = tr.find(class_='end-time').text
                            release_time = '-'.join((start_time, end_time))
                            language_type = tr.find_all('td')[1].text
                            video_hall = tr.find_all('td')[2].text
                            if tr.find(class_='price'):                        
                                price = tr.find(class_='price').text
                            else:
                                price = 'price not found'
                            mp = MoviePrice(name=name,release_date=release_date,release_time=release_time,language_type=language_type,video_hall=video_hall,price=price,channel=channel,cinema=cinema)
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