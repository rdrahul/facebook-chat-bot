from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserDetails(models.Model):
    fb_id=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)

    def __str__(self):
        return self.fb_id + ' '+ self.first_name+' ' +self.last_name 


