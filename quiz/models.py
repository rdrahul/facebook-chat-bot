from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserDetails(models.Model):
    fb_id=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)

    def __str__(self):
        return self.fb_id + ' '+ self.first_name+' ' +self.last_name 

class Questions(models.Model):
    question=models.TextField(unique=True);
    option1=models.CharField(max_length=100);
    option2=models.CharField(max_length=100);
    option3=models.CharField(max_length=100);
    option4=models.CharField(max_length=100);
    answer=models.CharField(max_length=100);
    links=models.CharField(max_length=255);
    pic_url=models.CharField(max_length=255);
    extra=models.CharField(max_length=255);
    genre=models.CharField(max_length=100);

class Feedback(models.Model):
    user=models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    content=models.TextField()

