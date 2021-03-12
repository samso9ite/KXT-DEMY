from django.db import models
from django.contrib.auth.models import User
from admin_portal.models import Course, Discussion

# Create your models here.

class members_profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    profession = models.CharField(max_length=250, null=True, blank=True)
    about = models.CharField(max_length=250)
    website = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    profile_img = models.ImageField(upload_to='images/profile_imgs/')

class Favorites(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='fav_course')

class Comment(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class LikeUnlike(models.Model):
    Comment = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(null=True)

class AddReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)


