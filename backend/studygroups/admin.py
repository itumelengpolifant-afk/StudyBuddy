from django.contrib import admin

from .models import (
    Attendance,
    GroupMember,
    Message,
    Module,
    Note,
    Notification,
    StudyGroup,
    StudySession,
    Vote,
)

admin.site.register(Module)
admin.site.register(StudyGroup)
admin.site.register(GroupMember)
admin.site.register(StudySession)
admin.site.register(Vote)
admin.site.register(Attendance)
admin.site.register(Note)
admin.site.register(Message)
admin.site.register(Notification)