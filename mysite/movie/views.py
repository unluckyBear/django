#coding:utf-8
from django.shortcuts import render_to_response, HttpResponse
from models import Channel,Cinema,CinemaCode,MoviePrice
from datetime import *
from strLikeness import strcmp
import requests
import json
from django.core import serializers


# Create your views here.

def search (request):
    return render_to_response('search.html')

def hot (request):
     movies = MoviePrice.objects.values('name','url').distinct().filter(url__icontains="http://")
     result = []
     for m in movies:
         result.append(dict((['name', m['name']], ['url', m['url']])))
     
     print result 
     return HttpResponse(json.dumps(result,ensure_ascii=False), content_type="application/json")
    
def list (request):
    #channel = Channel.objects.get(code='meituan')    
    #cinema = Cinema.objects.get(name=cinemaName,channel=channel)
    #movie = Movie.objects.get(name=movieName,channel=channel)
    #movieList = MoviePrice.objects.filter(name__contains=movieName,channel=channel,cinema=cinema, release_date__gte=date.today())
    #movieList = [movie for movie in movieList if datetime.strptime(movie.release_date.strftime("%Y-%m-%d") + " " + movie.release_time.split('-')[0], "%Y-%m-%d %H:%M") > datetime.now()]

    movie=request.REQUEST.get('movie')
    location=request.REQUEST.get('location')
    print location
    cinemas = Cinema.objects.all()
    
    r = requests.get('http://api.map.baidu.com/telematics/v3/movie?qt=nearby_cinema&location=' + location +'&ak=dLulKIfwaRtKmht7v3ZybBSc&output=json&radius=3000')
    data = r.json()
    if data['error'] == 0:
        movieInfos = []
        content = data['result']
        for i in range(len(content)):
            address = content[i]['address']
            print address

            #匹配address和数据库中最相似的一个
            dicts = {}
            for exist in cinemas:
                diff = strcmp(exist.address, address)
                dicts[diff] = exist

            minKey = min([k for k in sorted(dicts.keys())])
            cinema = dicts[minKey]

            moviePrices = MoviePrice.objects.filter(cinema=cinema, name=movie)
            movieInfo = MovieInfo(movie, cinema.name)

            prices = []
            for p in moviePrices:
                priceInfo = PriceInfo(p.channel.name, p.price, p.language_type)
                prices.append(priceInfo)

            movieInfo.prices = prices
            movieInfos.append(movieInfo)
                
    return HttpResponse(json.dumps(movieInfos,ensure_ascii=False,default=convert_to_dict), content_type="application/json") 



class MovieInfo(object):

    def __init__(self, movieName, cinemaName):
        self.movieName = movieName
        self.cinemaName = cinemaName


class PriceInfo(object):

    def __init__(self, channelName, price, language_type):
        self.channelName = channelName
        self.price = price
        self.language_type = language_type


def convert_to_dict(obj):
    '''把Object对象转换成Dict对象'''
    dict = {}
    dict.update(obj.__dict__)
    return dict

def convert_to_dicts(objs):
    '''把对象列表转换为字典列表'''
    obj_arr = []
     
    for o in objs:
        #把Object对象转换成Dict对象
        dict = {}
        dict.update(o.__dict__)
        obj_arr.append(dict)
     
    return obj_arr