from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from members_portal.views import CourseDetailView

app_name = "admin_portal"
urlpatterns = [
    path("dashboard/", views.dashboard, name="admin_dashboard"),
    path('profile_view/<slug:id>/', views.adminProfileDetails, name="admin_profile"),
    path('create_course/', views.courseCreateView.as_view(), name="create_course"),
    path('video_course/', views.CourseListView.as_view(), name="video_list"),
    path('audio_course/', views.CourseListView.as_view(), name="audio_list"),
    path('ebook_course/', views.CourseListView.as_view(), name="ebook_list"),
    path('signal_materials/', views.CourseListView.as_view(), name="signals_list"),
    path('update_course/<int:pk>', views.CourseUpdateView.as_view(), name="update_course"),
    path('delete_course/<int:id>', views.course_delete_view, name="delete_course"),
    path('course_details/<slug:id>', views.CourseDetailView.as_view(), name="course_details"),
    path('comment/<int:id>', views.discussionView, name="comment"),
    path('reply_comment/<int:id>/<int:topic_id>', views.replyCommentView, name="reply_comment"),
    path('delete_comment/<int:id>/', views.deleteCommentView, name="deleteComment"),
    path('notifications/', views.notification, name="notifications"),
    path('signals/', views.CreateSignal.as_view(), name="signals"),
    path('all_signals/', views.signalsList, name="all_signals"),
    path('like/<int:id>', views.likeUnlikeView, name="like"),
    path('unlike/<int:id>', views.likeUnlikeView, name="unlike"),
    path('create_topic/', views.DiscussionTopic.as_view(), name="discussion_topic"),
    path('all_topics/', views.DisplayTopics.as_view(), name="all_topics"),
    path('discussions/<int:id>', views.viewDiscussion, name="discussions"),
    path('live_output/<slug:id>', CourseDetailView.as_view(template_name='members_portal/live_output.html'), name="live_output"),
    path('all_member/', TemplateView.as_view(template_name='admin_portal/all_members.html'), name="all_members"),
    path('all_members/', views.allApprovedMembers.as_view(), name="all_members"),
    path('create_market/', views.createMarket.as_view(), name="create_market"),
   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)