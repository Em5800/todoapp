from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Todo (models.Model) :
    CATEGORY_CHOICES = [
        ('Pending', 'Pending'),
        ('Backlog', 'Backlog'),
        ('Finished', 'Finished'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Pending')
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title