from django.contrib import admin

from .models import Userprofile, FriendRequest


# Customisations for Django admin / USERPROFILE/ Friend requests
class FriendRequestAdmin(admin.ModelAdmin):

    def show_users_names(object):
        return f'Created by {object.created_by.get_full_name()} - Sent to {object.requested_to.get_full_name()}'

    show_users_names.short_description = 'Names'

    list_display = ['id', show_users_names, 'status', 'created_at']
    list_filter = ['created_at', 'status']  # Filter section
    search_fields = ['id', 'status'] # Searchbar (searches by ID)

admin.site.register(Userprofile)
admin.site.register(FriendRequest, FriendRequestAdmin)
