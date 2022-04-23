from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from djangoapps.post.forms import PostForm
from djangoapps.post.models import Post

from .forms import SignUpForm, UserprofileForm
from .models import Userprofile, FriendRequest


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            userprofile = Userprofile.objects.create(user=user)
            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request, 'userprofile/signup.html', {'form': form})


def search(request):
    query = request.GET.get('query', '')
    users = User.objects.all()

    if query:
        for term in query.split():
            # filter on multiple fields at once and run a search on each field
            users = users.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(email__icontains=term) | Q(username__icontains=term))
    else:
        users = []

    context = {
        'users': users
    }

    return render(request, 'userprofile/search.html', context)


def profile(request, user_id=0):
    if request.user.is_authenticated and user_id == 0:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)

    requested_friendship = FriendRequest.objects.filter(created_by=request.user).filter(requested_to=user).first()
    already_friends = request.user.userprofile.get_friends().filter(Q(requested_to=user) | Q(created_by=user))

    # 'action' references <a href="?action=send_friend_request"> in userprofile/profile.html
    action = request.GET.get('action', '')

    if action == 'send_friend_request':
        if not requested_friendship:
            requested_friendship = FriendRequest.objects.create(requested_to=user, created_by=request.user)
        else:
            # 'messages' is a default global variable, from settings.INSTALLED_APPS[]
            messages.error(request, 'Friendship already requested', extra_tags='is-danger')

    form = PostForm()
    context = {
        'user': user,
        'form': form,
        'already_friends': already_friends,
        'requested_friendship': requested_friendship
    }
    return render(request, 'userprofile/profile.html', context)


def friends(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    requested_friendships = FriendRequest.objects.filter(requested_to=user).filter(status=FriendRequest.REQUESTED)

    requested_friendship_id = request.GET.get('requested_friendship_id', '')
    action = request.GET.get('action', '')

    if action:
        requested_friendship = requested_friendships.get(pk=requested_friendship_id)
        if action == 'accept_request':
            requested_friendship.status = FriendRequest.ACCEPTED
            requested_friendship.save()
            messages.success(request, 'Friend request accepted!', extra_tags='is-success')

        elif action == ' reject_request':
            requested_friendship.status = FriendRequest.REJECTED
            requested_friendship.save()
            # messages.success(request, 'Friend request accepted!', extra_tags='is-warning')

        return redirect('friends', user_id=user.id)

    context = {
        'user': user,
        'requested_friendships': requested_friendships
    }
    return render(request, 'userprofile/friends.html', context)


@login_required
def myfeed(request):
    page = request.GET.get('page', 1)
    friendslist = request.user.userprofile.get_friends()
    friends_ids = []

    for friend in friendslist:
        if friend.created_by not in friends_ids:
            friends_ids.append(friend.created_by.id)
        elif friend.requested_to not in friends_ids:
            friends_ids.append(friend.requested_to.id)

    posts = Post.objects.filter(created_by__in=friends_ids)

    paginator = Paginator(posts, 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(posts.num_pages)

    return render(request, 'userprofile/myfeed.html', {'posts': posts})


@login_required
def edit_profile(request):
    userprofile = request.user.userprofile

    if request.method == 'POST':
        form = UserprofileForm(request.POST, request.FILES, instance=userprofile)

        if form.is_valid():
            form.save()

            messages.success(request, 'Your profile was updated successfully!', extra_tags='is-success')

            return redirect('myprofile')
    else:
        form = UserprofileForm(instance=userprofile)

    return render(request, 'userprofile/edit_profile.html', {'form': form})
