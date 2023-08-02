from django.shortcuts import render, redirect
# for multiple conditions in filter
from django.db.models import Q
# it's a decoratorfor user authorization
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from authentication.models import User

from rooms.models import Room, Topic, Message
from .forms import UserForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q)
    )  # .order_by('-updated') # -updatd means descindening
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))

    topics = Topic.objects.all()[:5]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def profile(req, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    # messages = user.message__set

    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics}
    return render(req, 'base/user_profile.html', context)


@login_required(login_url='/auth')
def updateUser(req):
    user = req.user
    form = UserForm(instance=user)

    if req.method == 'POST':
        form = UserForm(req.POST, files=req.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(req, 'base/update-user.html', context)


def activities(req):
    room_messages = Message.objects.all()

    context = {'room_messages': room_messages}
    return render(req, 'base/activity.html', context)
