from django.urls import path
from . import views
from django.views.generic import TemplateView
from admin_portal.views import notification, signalsList, viewDiscussion, DisplayTopics, likeUnlikeView, allApprovedMembers


app_name = "members_portal"
urlpatterns = [
    path('profile_settings/', views.membersProfileSetting.as_view(), name="members_profile_settings"),
    path('profile_details/<slug:id>/', views.membersProfileDetails, name="members_profile_details"),
    path('profile_update/<slug:id>/', views.membersProfileUpdate.as_view(), name="members_profile_update"),
    path('dashboard/', views.dashboard, name='members_dashboard'),
    path('notifications/', notification, name="notifications"),
    path('all_audios/', views.courseSectionView, name="all_audios"),
    path('all_videos/', views.videoSectionView, name="all_videos"),
    path('all_ebooks/', views.courseSectionView, name="all_ebooks"),
    path('all_signals/', views.courseSectionView, name="all_signals"),
    path('course_detail/<slug:id>', views.CourseDetailView.as_view(), name="course_detail"),
    path('live_output/<slug:id>', views.CourseDetailView.as_view(template_name='members_portal/live_output.html'), name="live_output"),
    path('save_course/<int:id>', views.saveAsFavorite, name="save_course"),
    path('fav_ebooks/', views.favorite_courses, name="favorite_ebooks"),
    path('fav_videos/', views.favorite_courses, name="favorite_videos"),
    path('fav_audios/', views.favorite_courses, name="favorite_audios"),
    path('fav_signals/', views.favorite_courses, name="favorite_signals"),
    path('signals/', signalsList, name="signals"),
    path('comment/', views.CreateComment.as_view(), name="create_comment"),
    path('all_topics/', DisplayTopics.as_view(), name="all_topics"),
    path('discussions/<int:id>', viewDiscussion, name="discussions"),
    path('like/<int:id>', likeUnlikeView, name="like"),
    path('unlike/<int:id>', likeUnlikeView, name="unlike"),
    path('create_review/<int:course_id>', views.createReview, name="create_review"),
    path('risk_calculator/', TemplateView.as_view(template_name="members_portal/calculator.html"), name="risk_calculator"),
    path('all_members/', allApprovedMembers.as_view(), name="all_members"),
    path('risks_calculator/', views.calculator, name="risks_calculator"),
   
] 