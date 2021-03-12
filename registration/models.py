from django.db import models
from django.contrib.auth.models import User

class MembersInfo(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    updated = models.BooleanField(default=False)
    notification = models.IntegerField(default=0)
    signal_notification = models.IntegerField(default=0)
    signal_update = models.BooleanField(default=False)

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    card_email = models.EmailField()
    card_last_digit = models.IntegerField()
    card_type = models.CharField(max_length=30)
    card_exp_month = models.CharField(max_length=30)
    card_exp_year = models.CharField(max_length=50)
    card_bank = models.CharField(max_length=50, )
    card_auth = models.CharField(max_length=50)
    card_account_name = models.CharField(max_length=100, null=True)
    card_first_name = models.CharField(max_length=50)
    card_last_name = models.CharField(max_length=50)

class Package(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    description = models.CharField(max_length=250, null=True)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package_subscribed = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)
    has_expired = models.BooleanField(default=False)
   










