from django.shortcuts import render
from members_portal.forms import *
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from members_portal.models import members_profile
from members_portal.models import *
from django.contrib.auth.decorators import login_required
from admin_portal.models import Discussion, Market
from registration.models import MembersInfo
from django.http import HttpResponseRedirect
from django.template.defaulttags import register
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

@method_decorator(login_required, name='dispatch')
class membersProfileSetting(CreateView):
    model = members_profile
    template_name = 'members_portal/setting.html'
    fields = ('profession', 'about', 'website', 'phone_number', 'twitter', 'linkedin', 'name', 'surname', 'facebook', 'profile_img')
    success_url = reverse_lazy('members_portal:dashboard')

    def form_valid(self, form):
        user = self.request.user
        form.instance.User = user
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class membersProfileUpdate(UpdateView):
    # model = members_profile
    template_name = 'members_portal/setting.html'
    context_object_name = 'member'
    fields = ('profession', 'about', 'website', 'phone_number', 'twitter', 'linkedin', 'name', 'surname', 'facebook', 'profile_img')
    success_url = reverse_lazy('members_portal:members_dashboard')

    def get_object(self):
        return members_profile.objects.get (User= self.request.user.id)

@login_required
def membersProfileDetails(request, id):
    instance = get_object_or_404(members_profile, User=id)
    discussion_query = Discussion.objects.filter(reply=True)

    return render (request, 'members_portal/student_profile_view.html', 
    context={'instance': instance, 'discussion_query': discussion_query})

    
@login_required
def dashboard(request):
    user = request.user
    if user.is_authenticated:
        all_members = members_profile.objects.all().select_related("User")
        # all_members = User.objects.filter(is_staff=False)
        notification = MembersInfo.objects.filter(User_id=request.user)
        all_videos = Course.objects.filter(category='video').order_by("-date_created")
        all_audios = Course.objects.filter(category='audio').order_by("-date_created")
        all_ebooks = Course.objects.filter(category = 'ebook').order_by("-date_created")
        all_signals = Course.objects.filter(category='signals').order_by("-date_created")
        all_vid = all_videos[:6]
        all_audio = all_audios[:6]
        all_ebook = all_ebooks[:6]
        context = {
            'all_members': all_members, 'notification':notification, 'all_audio': all_audio, 'all_ebook': all_ebook,
            'all_vid': all_vid , 'all_audios': all_audios, 'all_videos': all_videos, 'all_audios': all_audios,
        }
        return render(request, 'members_portal/student_dashboard.html', context)
    else:
        return render(request, 'registration/login.html')

@login_required
def videoSectionView(request):
    all_videos = Course.objects.filter(category="video")
    ordered_videos = all_videos.order_by("-date_created")
    context = {
        'ordered_videos':ordered_videos
    }
    return render(request, 'members_portal/videos_page.html', context)

@login_required
def courseSectionView(request):
    if 'all_ebooks/' in request.path:
        all_ebooks = Course.objects.filter(category="ebook")
        ordered_courses = all_ebooks.order_by("-date_created")
    elif 'all_audios/' in request.path:
        all_audios = Course.objects.filter(category="audio")
        ordered_courses = all_audios.order_by("-date_created")
    elif 'all_signals/' in request.path:
        all_signals = Course.objects.filter(category="signal education")
        ordered_courses = all_signals.order_by("-date_created")
    # fav_courses = Favorites.objects.all()
    context = {
        'ordered_courses':ordered_courses
    }
    return render(request, 'members_portal/courses.html', context)

@method_decorator(login_required, name="dispatch")
class CourseDetailView(DetailView):
    template_name = 'members_portal/audio_detail_page.html'
    context_object_name = 'audio_content'
    model = Course
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_queryset(self, *args, **kwargs):
        instance = self.kwargs.get('id')
        return Course.objects.filter(id=instance)

    def get_context_data(self, *args, **kwargs):
        instance = self.kwargs.get('id')
        context = super(CourseDetailView,self).get_context_data(**kwargs)
        context['all_reviews'] = AddReview.objects.filter(course_id=instance).order_by("-date_created")
        return context

@login_required
def saveAsFavorite(request, id):
    added_instance = Favorites.objects.filter(User_id=request.user.id, fav_course_id=id)
    if added_instance :
        added_instance.delete()
        messages.error(request, "Successfully Removed From Favorite!")
    else:
        instance = Favorites.objects.create(User_id=request.user.id, fav_course_id=id)
        messages.success(request, "Added to Favorite!")
    return (HttpResponseRedirect(request.META['HTTP_REFERER']))

@login_required
def favorite_courses(request):
    all_fav_courses = []
    if 'fav_ebooks/' in request.path:
        fav_courses = Favorites.objects.filter(User_id=request.user.id)
        for ebook in fav_courses:
             if ebook.fav_course.category == 'ebook':
                all_fav_courses.append(ebook)
    elif 'fav_audios/' in request.path:
        fav_courses = Favorites.objects.filter(User_id=request.user.id)
        for audio in fav_courses:
             if audio.fav_course.category == 'audio':
                all_fav_courses.append(audio)
    elif 'fav_signals/' in request.path:
        fav_courses = Favorites.objects.filter(User_id=request.user.id)
        for signal in fav_courses:
             if signal.fav_course.category == 'signal education':
                all_fav_courses.append(signal)
    elif 'fav_videos/' in request.path:
        fav_courses = Favorites.objects.filter(User_id=request.user.id)
        for video in fav_courses:
             if video.fav_course.category == 'video':
                all_fav_courses.append(video)
    context = {
        'all_fav_courses':all_fav_courses
    }
    return render(request, 'members_portal/courses.html', context)

@register.filter
def get_item(all_fav_courses, key):
    for record in all_fav_courses:
        if key in record:
            return record.get(key)


@method_decorator(login_required, name="dispatch")
class CreateComment(CreateView):
    model = Comment
    template_name = 'members_portal/live_output.html'
    success_url = 'members_portal:live_output'
    fields = ('comment', 'user')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

@login_required
def createReview(request, course_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.course_id = course_id
            form.instance.user_id = request.user.id
            form.save(commit=True)
            return (HttpResponseRedirect(request.META['HTTP_REFERER']))
        else:
            print(form.errors)
            return (HttpResponseRedirect(request.META['HTTP_REFERER']))
    # return render(request, 'members_portal/audio_detail_page.html')

# def calculator(request):
#     if request.method == 'POST':
#         form = Calculator(request.POST)
#         if form.is_valid():
#             lot_size = form.cleaned_data["lot_size"]
#             print(lot_size)
#             percentage_risk = form.cleaned_data["percentage_risk"]
#             account_balance = form.cleaned_data["account_balance"]
#             instance = Market.objects.get(lot_size=lot_size)
#             amount_to_loose = percentage_risk / 100 * account_balance
#             lowest_risk_dollar_result = amount_to_loose / instance.lowest_risk_dollar
#             lot_size_result = lot_size / lowest_risk_dollar_result
#             print(amount_to_loose)
#             print(lowest_risk_dollar_result)
#             print(lot_size_result)
#             return (HttpResponseRedirect(request.META['HTTP_REFERER']))
#         else:
#             print("Form not valid")
#     return render(request, 'members_portal/calculator.html')

def calculator(request):
    if request.method == 'POST' and request.is_ajax:
        response_data = {}
        form = Calculator(request.POST)
        if form.is_valid():
            lot_size = float(request.POST.get("lot_size"))
            stop_loss = float(request.POST.get("stop_loss"))
            print(stop_loss)
            percentage_risk = float(request.POST.get("percentage_risk"))
            account_balance = float(request.POST.get("account_balance"))
            instance = Market.objects.get(lot_size=lot_size)
            # lowest_risk_dollar = instance.lowest_risk_dollar
            amount_to_loose = percentage_risk / 100 * account_balance
            points_calc = stop_loss / instance.points
            print(points_calc)
            lowest_risk_dollar_result = amount_to_loose / points_calc
            print(lowest_risk_dollar_result)
            lot_size_result =  lowest_risk_dollar_result / lot_size
            response_data['amount_to_loose'] = amount_to_loose
            response_data['lot_size_result'] = lot_size_result
            # messages.success(request, "Lot Size Calculated")
            return JsonResponse({'response': response_data}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    return render(request, 'members_portal/calculator.html')