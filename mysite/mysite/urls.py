from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$','helloworld.views.hello'),
    url(r'^hello/(.+)/$','helloworld.views.hello2'),
    url(r'^movie/add/','movie.views.add'),
    url(r'^movie/search/','movie.views.search'),
    url(r'^movie/save/','movie.views.saveMovie'),
    url(r'^movie/list/','movie.views.list'),
    url(r'^cinema/save/','movie.views.saveCinema'),
    url(r'^meituan/save/','movie.views.saveMeiTuanMovie'),
)
