"""
Admin
-------------------------------
This module contains various settings for the Django admin panel. It is used
to display custom through tables and register models to the admin panel.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox, InboxSection, InboxUserSection
from ticketvise.models.label import Label
from ticketvise.models.notification import Notification
from ticketvise.models.notification.assigned import TicketAssignedNotification
from ticketvise.models.notification.comment import CommentNotification
from ticketvise.models.notification.mention import MentionNotification
from ticketvise.models.notification.new import NewTicketNotification
from ticketvise.models.notification.reminder import TicketReminderNotification
from ticketvise.models.ticket import Ticket, TicketEvent, TicketStatusEvent, \
    TicketAssigneeEvent, TicketLabelEvent, TicketAttachment, TicketSharedUser
from ticketvise.models.user import User, UserInbox


class InboxInlineAdmin(admin.TabularInline):
    """
    Allows the many-to-many relationship table between the ``User`` and ``Inbox``
    to be displayed in the admin panel.
    """

    #: Through table model for the many-to-many relationship.
    model = User.inboxes.through


class CustomUserAdmin(UserAdmin):
    """
    Custom User interface for the admin panel. Inherits the built-in ``UserAdmin``.
    Used to display the many-to-many relationship between ``User`` and ``Inbox``.
    """
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    inlines = (InboxInlineAdmin,)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'receiver', 'is_read', 'email_message_id', 'date_edited', 'date_created')

# Register all models in the admin panel.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Inbox)
admin.site.register(InboxSection)
admin.site.register(InboxUserSection)
admin.site.register(UserInbox)
admin.site.register(Label)
admin.site.register(Ticket)
admin.site.register(TicketAttachment)
admin.site.register(TicketEvent)
admin.site.register(TicketStatusEvent)
admin.site.register(TicketAssigneeEvent)
admin.site.register(TicketLabelEvent)
admin.site.register(Comment)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(TicketAssignedNotification)
admin.site.register(CommentNotification)
admin.site.register(MentionNotification)
admin.site.register(NewTicketNotification)
admin.site.register(TicketReminderNotification)
admin.site.register(TicketSharedUser)
