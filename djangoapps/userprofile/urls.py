from django.contrib.auth import views as auth_views
from django.urls import path

from djangoapps.userprofile import views

urlpatterns = [

    path('sign-up/', views.signup, name='signup'),
    path('log-out/', auth_views.LogoutView.as_view(), name='logout'),
    path('log-in/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('me/', views.profile, name='myprofile'),
    path('me/edit/', views.edit_profile, name='edit_profile'),
    path('me/feed/', views.myfeed, name='myfeed'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/friends/', views.friends, name='friends'),
    path('search/', views.search, name='search'),

]
