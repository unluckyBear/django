from django.shortcuts import render_to_response
import datetime

# Create your views here.
def hello(request):
    date = datetime.datetime.now()
    return render_to_response('hello.html',{'current_date':date})


def hello2(request,name):
    date = datetime.datetime.now()
    return render_to_response('hello.html',{'name':name,'current_date':date})   
