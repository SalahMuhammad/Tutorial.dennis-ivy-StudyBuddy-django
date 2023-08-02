from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from .models import Topic, Room, Message
from .forms import RoomForm


def room(request, pk):
    room = Room.objects.get(id=pk)
    # give us the set of messages in database that are related to this room
    # message is same as in models
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'f/room.html', context)


def topics(req):
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)

    context = {'topics': topics}
    return render(req, 'base/topics.html', context)


# if user isn't loged in, adn request this view, will redirect to login page
@login_required(login_url='/auth')
def create(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(
            name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'f/room_form.html', context)


@login_required(login_url='/auth')
def update(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Permission Denied.')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(
            name=topic_name)

        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()

        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')

    context = {'form': form,
               'topics': topics,
               'room': room}
    return render(request, 'f/room_form.html', context)


@login_required(login_url='/auth')
def delete(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Permission Denied.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': room})


@login_required(login_url='/auth')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Permission Denied.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'delete.html', context)
