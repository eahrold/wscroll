from django.db import models

class WebPage(models.Model):
    url = models.CharField(max_length=400,unique=True)
    
    def __unicode__(self):
         return self.url 
         
class Collection(models.Model):
    name = models.CharField(max_length=200)
    delay = models.IntegerField(null=True,blank=True)
    url = models.ManyToManyField(WebPage,blank=True)
    
    def __unicode__(self):
        return self.name