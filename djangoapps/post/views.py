from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm
from .models import Post, Like, Comment


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # "goto" references userprofile/templates/userprofile/myfeed.html/
    # <a href="{% url 'like_post' post.id %}?goto=myfeed" class="level-item">
    goto = request.GET.get('goto', '')

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(post=post, created_by=request.user)

    if goto:
        return redirect(goto)

    return redirect('profile', user_id=post.created_by.id)


@login_required
@require_POST
def add_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
    else:
        messages.error(request, 'something went wrong. Please try again', extra_tags='is-danger')

    return redirect('myprofile')


@login_required
@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.created_by = request.user
        comment.save()

    return redirect('profile', user_id=post.created_by.id)
