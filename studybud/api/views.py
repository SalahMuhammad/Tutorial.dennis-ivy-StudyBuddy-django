from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RoomSerializer

from rooms.models import Room


# this view can only take in a get request
@api_view(['GET'])
def getRoutes(req):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    return Response(routes)


@api_view(['GET'])
def getRooms(req):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getRoom(req, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)

    return Response(serializer.data)
