from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^meituan/cinema/','movie.meituan.saveCinema'),
    #url(r'^meituan/movie/','movie.meituan.saveMovie'),
    url(r'^meituan/price/','movie.meituan.savePrice'),
    url(r'^taobao/cinema/','movie.taobao.saveCinema'), 
    url(r'^taobao/price/','movie.taobao.savePrice'),
)
