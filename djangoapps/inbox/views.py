from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MessageForm
from .models import Conversation, Message


def check_if_conversation_exists(request, recipient_id, conversation_id):
    if conversation_id:
        conversation = Conversation.objects.filter(user__in=[request.user.id]).get(pk=conversation_id)

        return conversation
    else:
        # Return all conversation where the logged in user and the ID of the recipient is within the User object
        conversations = Conversation.objects.filter(user__in=[request.user.id]).filter(user__in=[recipient_id])

        if conversations:
            return conversations.first()
        else:
            return None


@login_required
def inbox(request):
    return render(request, 'inbox/inbox.html')


@login_required
def conversation(request, conversation_id):
    recipient_id = request.GET.get('recipient_id', '')
    conversation = check_if_conversation_exists(request, recipient_id, conversation_id)

    if not conversation:
        if conversation_id == 0 and recipient_id:
            recipient = request.user.userprofile.get_friends().filter(
                Q(created_by_id=recipient_id) | Q(requested_to_id=recipient_id))

            if recipient:
                conversation = Conversation.objects.create()
                conversation.user.add(request.user.id)
                conversation.user.add(recipient_id)
                conversation.save()

                return redirect('conversation', conversation_id=conversation.id)
            else:
                messages.error(request, 'Something went wrong. Please try again',
                               extra_tags='is-danger')

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()

            conversation.save()

            return redirect('conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()

    context = {
        'conversation': conversation,
        'form': form
    }

    return render(request, 'inbox/conversation.html', context)
