from django.db import models

# Create your models here.
class Channel(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    url = models.CharField(max_length=100)
    
class Cinema(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(null=False,max_length=20)
    address = models.CharField(max_length=800)
    #channel = models.ForeignKey(Channel)

class CinemaCode(models.Model):
    code = models.CharField(null=False,max_length=50)
    cinema = models.ForeignKey(Cinema)
    channel = models.ForeignKey(Channel)

 
#class Movie(models.Model):
#    name = models.CharField(max_length=100)

#class MovieCode(models.Model):    
#    code = models.CharField(null=False,max_length=20)
#    movie = models.ForeignKey(Movie)
#    channel = models.ForeignKey(Channel)


class MoviePrice(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=50)
    #code = models.CharField(null=False,max_length=20)
    #release_date = models.DateField()
    #release_time = models.CharField(max_length=50)
    language_type = models.CharField(max_length=30)
    #video_hall = models.CharField(max_length=30)  
    price = models.CharField(max_length=100)  
    channel = models.ForeignKey(Channel)
    cinema = models.ForeignKey(Cinema)