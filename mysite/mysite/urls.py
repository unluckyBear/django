from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$','helloworld.views.hello'),
    url(r'^hello/(.+)/$','helloworld.views.hello2'),
    url(r'^movie/search/','movie.views.search'),
    url(r'^movie/hot/','movie.views.hot'),
    url(r'^movie/list/','movie.views.list'),
    url(r'^movie/save/', include('movie.urls')),
)
