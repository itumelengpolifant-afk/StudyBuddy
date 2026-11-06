import secrets
import string

from django.conf import settings
from django.db import models


def generate_join_code():
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))


class Module(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.code} - {self.name}"


class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='groups'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_groups',
    )
    join_code = models.CharField(
        max_length=10, unique=True, default=generate_join_code
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='GroupMember',
        related_name='study_groups',
    )

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        MEMBER = 'member', 'Member'

    group = models.ForeignKey(
        StudyGroup, on_delete=models.CASCADE, related_name='memberships'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.MEMBER
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'user'], name='unique_group_member'
            )
        ]

    def __str__(self):
        return f"{self.user} in {self.group} ({self.role})"


class StudySession(models.Model):
    class Status(models.TextChoices):
        PROPOSED = 'proposed', 'Proposed'
        CONFIRMED = 'confirmed', 'Confirmed'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    group = models.ForeignKey(
        StudyGroup, on_delete=models.CASCADE, related_name='sessions'
    )
    venue = models.CharField(max_length=200, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PROPOSED
    )

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return f"{self.group} session ({self.status})"


class Vote(models.Model):
    session = models.ForeignKey(
        StudySession, on_delete=models.CASCADE, related_name='votes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes'
    )
    time_slot = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'user', 'time_slot'],
                name='unique_vote_per_option',
            )
        ]

    def __str__(self):
        return f"{self.user} voted {self.time_slot}"


class Attendance(models.Model):
    session = models.ForeignKey(
        StudySession, on_delete=models.CASCADE, related_name='attendance_records'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    present = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'user'], name='unique_session_attendance'
            )
        ]

    def __str__(self):
        return f"{self.user} - {'present' if self.present else 'absent'}"


class Note(models.Model):
    group = models.ForeignKey(
        StudyGroup, on_delete=models.CASCADE, related_name='notes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes'
    )
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to='notes/')

    def __str__(self):
        return self.title


class Message(models.Model):
    group = models.ForeignKey(
        StudyGroup, on_delete=models.CASCADE, related_name='messages'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages'
    )
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"{self.user}: {self.text[:30]}"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"To {self.user}: {self.message[:30]}"