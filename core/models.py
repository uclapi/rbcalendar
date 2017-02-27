from django.db import models

# Create your models here.


class Query(models.Model):
    roomid = models.CharField(max_length=200, blank=True)
    start_datetime = models.CharField(max_length=200, blank=True)
    end_datetime = models.CharField(max_length=200, blank=True)
    date = models.CharField(max_length=200, blank=True)
    siteid = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    hash = models.CharField(max_length=500, unique=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_started = models.DateTimeField()
    last_accessed = models.DateTimeField(blank=True, null=True)
