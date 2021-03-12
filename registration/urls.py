from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'authentication'
urlpatterns = [
  path('forget_pwd', TemplateView.as_view(template_name="registration/forgot_password.html"), name="forgot_pwd"),
  path('plans/', TemplateView.as_view(template_name="registration/membership.html"), name="plans"),
  path('sign_up', views.signUp, name='signup'),
  path('login/', views.login_view, name="login"),
  path('logout/', views.logout_view, name="logout"),
  path('password_reset/', auth_views.PasswordResetView.as_view(template_name="reset_pwd/password_reset_form.html", email_template_name="reset_pwd/password_reset_email.html", subject_template_name="reset_pwd/password_reset_subject.txt", success_url=reverse_lazy('authentication:password_reset_done')), name="password_reset"),
  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="reset_pwd/password_reset_done.html"), name="password_reset_done"),
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset_pwd/password_reset_confirm.html", success_url=reverse_lazy('authentication:password_reset_complete')), name="password_reset_confirm"),
  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_pwd/password_reset_complete.html"), name="password_reset_complete"),
  path('verification/', views.verifyTransaction, name="trans_verification"),
  path('thank_you/', TemplateView.as_view(template_name="registration/thank_you.html"), name="thank_you"),
  path('home/', TemplateView.as_view(template_name="registration/index.html"), name="home"),
  # path('dashboard/', views.dashboard, name='members_dashboard'),
 
]