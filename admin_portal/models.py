from django.db import models
from registration.models import User
# from django.utils import timezone

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    membership = models.CharField(max_length=20)
    category = models.CharField(max_length=30)
    cover_img = models.ImageField(upload_to='images/coverImg')
    material = models.FileField(upload_to='materials/')
    volume = models.IntegerField()
    duration = models.IntegerField()
    status = models.CharField(max_length=50,null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    course_overview = models.CharField(max_length=250)

class DiscussionTopics(models.Model):
    topic = models.CharField(max_length=100)
    content = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)

class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(DiscussionTopics, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    comment_date = models.DateTimeField(auto_now_add=True)
    reply = models.BooleanField(default=False)
    comment_replied = models.IntegerField(null=True)
    like_count = models.IntegerField(default=0)
    unlike_count = models.IntegerField(default=0)
   
class Signals(models.Model):
    signal_title = models.CharField(max_length=50)
    signal_content = models.CharField(max_length=250)
    signal_date = models.DateTimeField(auto_now=True)
    members = models.CharField(max_length=50)


class Market(models.Model):
    market_name = models.CharField(max_length=50)
    lot_size = models.FloatField() 
    lowest_risk_dollar = models.FloatField()
    points = models.FloatField()
    