from django.urls import path

from djangoapps.post import views

urlpatterns = [
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
    path('add_post/', views.add_post, name='add_post'),
]
