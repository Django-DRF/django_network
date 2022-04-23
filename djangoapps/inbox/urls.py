from django.urls import path

from djangoapps.inbox import views

urlpatterns = [
    path('', views.inbox, name='inbox'),  # N.B. the route will be specified in the main, djangonetwork/urls.py
    path('<int:conversation_id>/', views.conversation, name='conversation'),
]
