from registration.models import MembersInfo, Subscription
from members_portal.models import members_profile, Favorites
from admin_portal.models import Discussion, Market, Signals
from django.shortcuts import render


def general_info(request):
    try:
        update_data = MembersInfo.objects.get(User=request.user.id)
        
        if update_data.notification < 4 or update_data.signal_notification < 4:
            list_signals = Signals.objects.order_by("-signal_date")[:update_data.signal_notification]
            comments = Discussion.objects.order_by("-comment_date")[:update_data.notification]
        else:
            comments = Discussion.objects.order_by("-comment_date")[:3]
            list_signals = Signals.objects.order_by("-signal_date")[:3]
        return {
            'data': update_data.updated, 'notification_count': update_data.notification, 'comments':comments, 'signals_count': update_data.signal_notification, 'list_signals':list_signals
        }

    except MembersInfo.DoesNotExist:
        update_data = None
        return{
            'data': update_data
        }

def created_check(request):
    try:
        profile_check = members_profile.objects.get(User=request.user.id)
        return {
            'profile': profile_check
        }

    except members_profile.DoesNotExist:
        profile_check = None
        return {
            'profile': profile_check
        }
   
def check_fav(request):
    try:
        checked_result = Favorites.objects.filter(User_id=request.user.id).values_list('fav_course_id')
        response = []
        for a in checked_result:
            response.append(a[0])
        return{
            'checked_result': response
        }
    except:
        pass

def user_img(request):
    try:
        if request.user.is_authenticated:
            profile_img = members_profile.objects.get(User_id=request.user.id)
            return{
                'profile_img':profile_img.profile_img.url
            }
        else:
            return{
                'profile_img':[]
            }
    except:
        return{
                'profile_img':[]
            }

def check_plan(request):
    try:
        if request.user.is_authenticated and request.user.is_staff is False:
            plan = Subscription.objects.get(user_id=request.user.id)
            print(plan)
            return{
                    'package':plan.package_subscribed_id
            }
        else:
            return{
                'package':[]
            }
    except:
        pass

def market(request):
    try:
        if request.user.is_authenticated:
            all_market = Market.objects.all()
            return{
                'all_market':all_market
            }
        else:
            return{
                'all_market':[]
            }
    except:
        pass


     
 