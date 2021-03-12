from django.shortcuts import render
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from members_portal.models import members_profile, LikeUnlike, members_profile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from admin_portal.models import *
from django.urls import reverse_lazy
from admin_portal.forms import *
from admin_portal.forms import createCourseForm
from registration.models import MembersInfo
from django.http import  HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def dashboard(request):
    videos = Course.objects.filter(category='video').order_by('date_created')
    audios = Course.objects.filter(category='audio').order_by('date_created')
    signals = Course.objects.filter(category='signal').order_by('date_created')
    ebooks = Course.objects.filter(category='ebook').order_by('date_created')
    total_signals = signals.count()
    total_videos = videos.count()
    total_audios = audios.count()
    total_ebooks = ebooks.count()
    total_members = User.objects.filter(is_staff=False).count()
    # for video in videos:
    #     diff = datetime.now().date() - video.date_created
    #     if diff >40:
    #         # date_diff = diff.days
    #         print("Checking")
    context = {'total_signals':total_signals, 'total_videos':total_videos, 'total_audios': total_audios, 
    'total_ebooks':total_ebooks, 'total_members':total_members, 'videos':videos, 'audios':audios, 'ebooks':ebooks}
    return render(request, 'admin_portal/instructor_dashboard.html', context)
    
@login_required
def adminProfileDetails(request, id):
    instance = get_object_or_404(members_profile, User=id)
    videos = Course.objects.filter(category='video')
    audios = Course.objects.filter(category='audio')
    signals = Course.objects.filter(category='signal')
    ebooks = Course.objects.filter(category='ebook')
    video_total = videos.count()
    ebook_total = ebooks.count()
    signal_total = signals.count()
    audio_total = audios.count()
    

    context = {'instance': instance, 'video_total':video_total, 'signal_total':signal_total, 'ebook_total':ebook_total, 'audio_total':audio_total }
    return render (request, 'admin_portal/instructor_profile_view.html', context)

@method_decorator(login_required, name='dispatch')
class courseCreateView(SuccessMessageMixin, CreateView):
    model = Course
    template_name = "admin_portal/create_new_course.html"
    fields = ('title', 'subtitle', 'description', 'membership', 'category', 'cover_img', 'volume', 'duration', 'status', 'material')
    success_url = reverse_lazy('admin_portal:create_course')
    context_object_name = 'course'
    success_message = "Course Created Successfully!"

@method_decorator(login_required, name="dispatch")
class CourseListView(ListView):
    template_name =  'admin_portal/instructor_courses.html'
    paginate_by = 10
    ordering = ['-date_created']
    model = Course
    context_object_name = 'ebook_list'

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        if package == 2 or 4:
            context['video_list'] = Course.objects.filter(category="video").order_by('-date_created')
            context['audio_list'] = Course.objects.filter(category="audio").order_by('-date_created')
            context['ebook_list'] = Course.objects.filter(category="ebook").order_by('-date_created')
            context['signal'] = Course.objects.filter(category="signal education").order_by('-date_created')
        elif package == 1:
            context['video_list'] = Course.objects.filter(category="video", membership="vip & regular").order_by('-date_created')
            context['audio_list'] = Course.objects.filter(category="audio", membership="vip & regular").order_by('-date_created')
            context['ebook_list'] = Course.objects.filter(category="ebook", membership="vip & regular").order_by('-date_created')
            context['signal'] = Course.objects.filter(category="signal education", membership="vip & regular").order_by('-date_created')
        elif package == 3:
            context['video_list'] = Course.objects.filter(category="video", membership="signal education").order_by('-date_created')
            context['audio_list'] = Course.objects.filter(category="audio", membership="signal education").order_by('-date_created')
            context['ebook_list'] = Course.objects.filter(category="ebook", membership="signal education").order_by('-date_created')
            context['signal'] = Course.objects.filter(category="signal education", membership="signal education").order_by('-date_created')
        return context

@method_decorator(login_required, name="dispatch")
class CourseUpdateView(UpdateView):
    # course_instance = Course.objects.filter(id=self.pk)
    template_name = "admin_portal/create_new_course.html"
    model = Course
    form_class = createCourseForm
    context_object_name = 'update_data'
    success_url = reverse_lazy('admin_portal:video_course')
    success_message = "Course Updated Successfully!"

@login_required
def course_delete_view(request, id):
    instance = Course.objects.get(id=id)
    instance.delete()
    messages.success(request, "Course Deleted Successfully")
    return (HttpResponseRedirect(request.META['HTTP_REFERER']))

@method_decorator(login_required, name="dispatch")
class CourseDetailView(DetailView):
    models = Course
    template_name = 'admin_portal/course_detail.html'
    context_object_name = 'course_data'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    
    def get_queryset(self, *args, **kwargs):
        instance = self.kwargs.get('id')
        return Course.objects.filter(id=instance)

@login_required
def discussionView(request, id):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid:
            form.save(commit=False)
            form.instance.topic_id = id
            form.instance.user = request.user
            form.save(commit=True)
            MembersInfo.objects.all().update(notification = F('notification')+1)
            return (HttpResponseRedirect(request.META['HTTP_REFERER']))
        else:
            messages.error(request, 'Error')
    return render(request, 'admin_portal/instructor_profile_view.html')

@login_required
def replyCommentView(request, id, topic_id):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid:
            form.save(commit=False)
            form.instance.user = request.user
            form.instance.reply = True
            form.instance.topic_id = topic_id
            form.instance.comment_replied = id
            form.save(commit=True)
            MembersInfo.objects.all().update(notification = F(notification)+1) 
            return (HttpResponseRedirect(request.META['HTTP_REFERER']))
        else:
            messages.error(request, 'Error')
    return render(request, 'admin_portal/instructor_profile_view.html')

@login_required
def deleteCommentView(request, id):
    instance = Discussion.objects.filter(id=id, user_id=request.user.id)
    instance.delete()
    messages.success(request, 'Comment Deleted')
    return (HttpResponseRedirect(request.META['HTTP_REFERER']))

@login_required
@csrf_exempt
def likeUnlikeView(request, id):
    instances = LikeUnlike.objects.filter(user_id=request.user.id, Comment_id=id)
    discussion_instance = Discussion.objects.filter(id=id)
    # response_data = {}
    if '/like' in request.path:
        for instance in instances:
            if instance and instance.like is False:
                discussion_instance.update(like_count=F('like_count')+1, unlike_count= F('unlike_count')-1)
                instance.like = True
                instance.save()
                messages.success(request, "Liked Comment!")
                
        if not instances:
            LikeUnlike.objects.create(user_id=request.user.id, Comment_id=id, like=True)
            discussion_instance.update(like_count=F('like_count')+1)
            messages.success(request, "Liked Comment!")
        return JsonResponse({"status":True})
    if '/unlike' in request.path:
        for instance in instances:
            if instance and instance.like is True:
                discussion_instance.update(unlike_count=F('unlike_count')+1, like_count= F('like_count')-1) 
                instance.like = False
                instance.save()
                messages.success(request, "Unliked Comment!")
        if not instances:
            LikeUnlike.objects.create(user_id=request.user.id, Comment_id=id, like=False)
            discussion_instance.update(unlike_count=F('like_count')+1)
            messages.success(request, "Unliked Comment!")
        return JsonResponse({"status":False})
    # return (HttpResponseRedirect(request.META['HTTP_REFERER']))

@login_required
def notification(request):
    unread_notifications = MembersInfo.objects.filter(User_id=request.user.id)
    signal_notification = ""
    for unread in unread_notifications:
        if "notifications/" in request.path:
            notifications = Discussion.objects.order_by('-comment_date')[:unread.notification]
            unread_notifications.update(notification=0)
        elif "members_portal/signals/" in request.path:
            signal_notification = Signals.objects.order_by('-signal_date')[unread.signal_notification]
            unread_notifications.signal_update(signal_notification=0)
        context = {'notifications':notifications, 'signal_notification':signal_notification}
        return render(request, 'admin_portal/instructor_notifications.html', context)

@method_decorator(login_required, name="dispatch")
class CreateSignal(SuccessMessageMixin, CreateView):
    model = Signals
    template_name = 'admin_portal/create_signals.html'
    success_url = reverse_lazy('admin_portal:signals')
    fields = ('signal_title', 'signal_content', 'members')
    success_message = "Cool! Signal Created Successfully"

@receiver(post_save, sender=Signals)
def update_signal_notification_count(sender, instance,  created, **kwargs):
    if created:
        MembersInfo.objects.all().update(signal_notification= F('signal_notification')+1)
        MembersInfo.objects.all().update(signal_update=True)
    
@login_required
def signalsList(request):
    instance = MembersInfo.objects.filter(User_id=request.user.id).update(signal_notification=0)
    signals_list = Signals.objects.all().order_by("-signal_date")
    page = request.GET.get('page', 1)
    paginator = Paginator(signals_list, 5)
    try:
        signals = paginator.page(page)
    except PageNotAnInteger:
        signals = paginator.page(1)
    except EmptyPage:
        signals = paginator.page(paginator.num_pages)
    return render(request, 'admin_portal/signals.html', {'signals':signals})

@method_decorator(login_required, name="dispatch")
class DiscussionTopic(SuccessMessageMixin, CreateView):
    model = DiscussionTopics
    fields = ('content', 'topic')
    success_url = reverse_lazy('admin_portal:discussion_topic')
    template_name = 'admin_portal/create_topics.html'
    success_message = "Great!!! Dicsussion Topic Created"

@method_decorator(login_required, name="dispatch")
class DisplayTopics(ListView):
    model = DiscussionTopics
    template_name = "admin_portal/discussion_topics.html"
    context_object_name = "topics"

@login_required
def viewDiscussion(request, id):
    discussion_query = Discussion.objects.filter(reply=False, topic_id=id).order_by('-comment_date')
    comment_replies = Discussion.objects.filter(reply=True, topic_id=id).order_by('-comment_date')
    context = {'discussion_query':discussion_query, 'comment_replies':comment_replies, 'id':id }
            
    return render(request, 'admin_portal/view_discussion.html', context)

@method_decorator(login_required, name="dispatch")
class allApprovedMembers(ListView):
    model = members_profile
    template_name = "admin_portal/all_members.html"
    context_object_name = "members"
    
@method_decorator(login_required, name="dispatch")
class createMarket(SuccessMessageMixin, CreateView):
    model = Market
    template_name = "admin_portal/create_market.html"
    fields = ("lot_size", "market_name", "points", "lowest_risk_dollar")
    success_message = "Cool! Market Created Successfully"
    success_url = reverse_lazy('admin_portal:create_market')