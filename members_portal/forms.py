from django import forms
from members_portal.models import *

class members_profile(forms.ModelForm):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=200)
    profession = forms.CharField(max_length=250)
    about = forms.CharField(max_length=250)
    phone_number = forms.CharField(max_length=200)
    facebook = forms.URLField(max_length=200)
    linkedin = forms.URLField(max_length=200)
    twitter = forms.URLField(max_length=200)
    profile_img = forms.ImageField()

    class Meta:
        fields = ('profession', 'about', 'phone_number', 'facebook', 'linkedin', 'twitter', 'first_name', 'last_name', 'profile_img')

class ReviewForm(forms.ModelForm):
    review = models.CharField(max_length=250)
    class Meta:
        model = AddReview
        fields = ('review',)

class Calculator(forms.Form):
    stop_loss = forms.FloatField()
    account_balance = forms.FloatField()
    percentage_risk = forms.FloatField()
    lot_size = forms.FloatField()