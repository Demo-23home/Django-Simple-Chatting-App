from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group
from django.http import HttpResponseForbidden

# Create your views here.


# Create Group
@login_required
def create_group(request):
    user = request.user
    new_group = Group.objects.create()
    new_group.add_user(user)
    new_group.save()
    return redirect("home")


# Delete Group
@login_required
def delete_group(request, uuid):
    group = Group.objects.get(uuid=uuid)
    group.delete()
    return redirect("home")


# Join Group
@login_required
def join_group(request, uuid):
    user = request.user
    group = Group.objects.get(uuid=uuid)
    group.add_user(user)
    group.save()
    return redirect("home")


# Leave Group
@login_required
def leave_group(request, uuid):
    group = Group.objects.get(uuid=uuid)
    user = request.user
    group.remove_user(user)
    group.save()
    return redirect("home")


# Open Chat
@login_required
def open_chat(request, uuid):
    group = Group.objects.get(uuid=uuid)
    user = request.user

    # check on user
    if user not in group.members.all():
        return HttpResponseForbidden("Not a member. Try another group.")

    messages = group.message_set.all()
    sorted_messages = sorted(messages, key=lambda message: message.time_stamped)
    context = {"messages": sorted_messages, "uuid": uuid}
    return render(request, "chat/chat.html", context=context)
