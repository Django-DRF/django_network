from django.urls import path

from djangoapps.core import views


urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('about/', views.about, name='about'),
]


