from background_task import background
from logging import getLogger
from registration.models import Subscription
from django.contrib.auth.models import User
from registration.models import Card
from django.utils.crypto import get_random_string

logger = getLogger(__name__)

@background(schedule=10)
def demo_task(message):
    users = User.objects.all()
    has_subscription = False
   
    for user in users:
         #get active subscription
        try:
            active = Subscription.objects.get(user=user.id,is_active=True,has_expired=False)
            if active:
                start_date = active.start_date
                from datetime import datetime
                diff = datetime.now().date() - start_date
                date_diff = diff.days
                if active.package_subscribed is 4:
                    if date_diff >= 15:
                        active.has_expired = True
                        is_active=False
                        active.save()
                    else:
                        has_subscription = True

                elif active.package_subscribed is not 4:   
                    if date_diff >= 30:
                        active.has_expired = True
                        is_active=False
                        active.save()
                    else:
                        has_subscription = True

        except Subscription.DoesNotExist:
            pass
        
        if not has_subscription:
            latest_plan = Subscription.objects.filter(user=user.id).order_by('-id')[:1]
            package = None
            for plan in latest_plan:
                package = plan.package_subscribed
            
            #Get users card
            users_card = Card.objects.filter(user=user.id)
            for card in users_card:

                from paystackapi.transaction import Transaction
                import uuid
                reference = get_random_string(length=20)
                print(reference)
                response = Transaction.charge(reference=reference,
                authorization_code=card.card_auth,
                email=card.card_email, amount=int(package.amount)*100)
                print(response)

                if response['status']==True and response['data']['status'] != 'failed':
                    subscription = Subscription(user=user, is_active=True, package_subscribed=package, has_expired=False)
                    subscription.save()
                    break