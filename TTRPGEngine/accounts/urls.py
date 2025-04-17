from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account_home/', views.account_home, name='account_home'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="password_change.html"), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/templates/"), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/templates/"), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/templates/"), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/templates/"), name='password_reset_complete')
    path('about/', views.about, name='about')
]