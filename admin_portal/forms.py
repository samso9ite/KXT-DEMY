from django import forms
from admin_portal.models import *

class createCourseForm(forms.ModelForm):
    title = forms.CharField(max_length=250)
    subtitle = forms.CharField(max_length=250)
    description = forms.CharField(max_length=250)
    membership = forms.CharField(max_length=20)
    category = forms.CharField(max_length=30)
    cover_img = forms.ImageField()
    material = forms.FileField()
    volume = forms.IntegerField()
    duration = forms.IntegerField()
    status = forms.CharField(max_length=50)
    
    class Meta:
        model = Course
        fields = ('title', 'subtitle', 'material', 'description', 'membership', 'category', 'cover_img', 'volume', 'duration', 'status',)

class DiscussionForm(forms.ModelForm):
    comment = forms.CharField(max_length=250)

    class Meta:
        model = Discussion
        fields = ('comment',)