from django.shortcuts import render
from registration.forms import signUpForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import render, redirect   
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from registration.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from paystackapi.transaction import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from background_task import background
from members_portal import urls
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

import paystackapi
paystackapi.SECRET_KEY = 'sk_live_1e187842e5ffdc17bc0ace04bac194e608d6682f'

# Create your models here.
def signUp(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully")
            return HttpResponseRedirect(reverse('authentication:login'))
        else:
            messages.error(request, 'Error')
    else:
        form = signUpForm()
    return render(request, 'registration/sign_up.html', {'form':form})

@receiver(post_save, sender=get_user_model())   
def create_others_instance(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string("registration/thank_you.html")
        email = EmailMessage("Welcome to KXT' DEMY", html_content, to=[instance.email], from_email=settings.EMAIL_HOST_USER)
        email.content_subtype = "html"
        res = email.send()
        MembersInfo.objects.create(updated=False, User=instance)
        package = Package.objects.get(name="free trial")
        Subscription.objects.create(user_id=instance.id, package_subscribed_id=package.id, is_active=True)
        
def login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_portal:admin_dashboard')
            else:
                if Subscription.objects.filter(user=user.id, is_active=False).last():
                    return redirect('authentication:plans')
                else:
                    return redirect('members_portal:members_dashboard')
        else:
            messages.error(request, "Username or Password isn't Correct")
    return render(request, 'registration/sign_in.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))

@csrf_exempt
def verifyTransaction(request):
    status = False
    message = ''
    ref = request.POST.get('reference')
    response = Transaction.verify(reference=ref)
    if response['status']==True and response['data']['status'] != 'failed':
        auth_code = response['data']['authorization']['authorization_code']
        last_digit = response['data']['authorization']['last4']
        expiry_month = response['data']['authorization']['exp_month']
        card_exp_year = response['data']['authorization']['exp_year']
        card_bank = response['data']['authorization']['bank']
        card_account_name = response['data']['authorization']['account_name']
        card_first_name = response['data']['customer']['first_name']
        card_last_name = response['data']['customer']['last_name']
        card_email = response['data']['customer']['email']
        card_type = response['data']['authorization']['card_type']
        package = response['data']['metadata']['custom_fields']['package']
        
        card = Card(user=request.user, card_auth=auth_code, card_last_digit=last_digit, card_exp_month=expiry_month,card_exp_year=card_exp_year,
                 card_bank=card_bank, card_account_name=card_account_name, card_first_name=card_first_name, 
                 card_last_name=card_last_name, card_email=card_email, card_type=card_type) 
        card.save()
        package = Package.objects.get(id=int(package))
        subscription = Subscription(user=request.user, is_active=True, package_subscribed=package, has_expired=False)
        subscription.save()
        status = True
        message = 'Transaction Successful'
    else:
        status = False
        message = response['message']
   
    return JsonResponse({'status':status, 'message': message})

