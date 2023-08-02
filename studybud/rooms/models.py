from django.db import models

from authentication.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    # id = models.UUIDField()
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # if topic class is below this class we can still access it put by wrapping name with quotes
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # blank means that i can suppmet form with blank description
    description = models.TextField(null=True, blank=True)
    # related_name
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    # updated every time instance updated
    updated = models.DateTimeField(auto_now=True)
    # only takes a time stamp when we first save or create this instance
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']  # or in views

    def __str__(self):  # string representation of this room
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        # return first 50 characters
        return self.body[0:50]
