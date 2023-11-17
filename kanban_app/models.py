from django.db import models
from datetime import datetime

class Column(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now)

class Task(models.Model):
    text = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Column, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
