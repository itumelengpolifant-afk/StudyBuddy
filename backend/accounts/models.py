from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        GROUP_OWNER = 'group_owner', 'Group Owner'
        MEMBER = 'member', 'Student'
        TUTOR = 'tutor', 'Tutor'

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.MEMBER
    )

    def __str__(self):
        return f"{self.username or self.username} ({self.role})"