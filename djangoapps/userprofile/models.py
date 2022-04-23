from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/avatars/%Y/%m/%d', blank=True, null=True)
    subtitle = models.CharField(max_length=50, default='Default subtitle text (editable)')  # subtitle = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user.get_full_name()}'  # Show full name of each user in Django admin panel

    def get_friends(self):
        return FriendRequest.objects.filter(status=FriendRequest.ACCEPTED).filter(Q(requested_to=self.user) | Q(created_by=self.user))

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 'https://bulma.io/images/placeholders/128x128.png'


class FriendRequest(models.Model):
    REQUESTED = 'requested'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    # Form labels
    CHOICES_STATUS = (
        (REQUESTED, 'Requested'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    requested_to = models.ForeignKey(User, related_name='requested_friendships', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_friendships', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=REQUESTED)

    def __str__(self):
        return f'Created by {self.created_by.get_full_name()} - Sent to {self.requested_to.get_full_name()}'
