"""
Admin
-------------------------------
This module contains various settings for the Django admin panel. It is used
to display custom through tables and register models to the admin panel.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Course
from ticketvise.models.label import Label
from ticketvise.models.notification import Notification, MentionNotification
from ticketvise.models.ticket import Ticket, TicketStatusChangedNotification
from ticketvise.models.user import User


class CourseInlineAdmin(admin.TabularInline):
    """
    Allows the many-to-many relationship table between the ``User`` and ``Course``
    to be displayed in the admin panel.
    """

    #: Through table model for the many-to-many relationship.
    model = User.courses.through


class CustomUserAdmin(UserAdmin):
    """
    Custom User interface for the admin panel. Inherits the built-in ``UserAdmin``.
    Used to display the many-to-many relationship between ``User`` and ``Course``.
    """

    #: Inline through tables to display on the admin panel.
    inlines = (CourseInlineAdmin,)


# Register all models in the admin panel.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Label)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(MentionNotification)
admin.site.register(TicketStatusChangedNotification)
