from ticketvise.models.notification.assigned import TicketAssignedNotification
from ticketvise.models.notification.comment import CommentNotification
from ticketvise.models.notification.mention import MentionNotification
from ticketvise.models.notification.new import NewTicketNotification
from ticketvise.models.notification.reminder import TicketReminderNotification


def unread_related_ticket_notifications(ticket, user):
    """
    Mark all notifications related to the given ticket as unread.
    :param Ticket ticket: Ticket for which all related notifications are marked
                          unread.
    :param User user: User for which the notifications are marked as unread.
    :return: None.
    """
    TicketAssignedNotification.objects.filter(ticket=ticket, receiver=user).update(is_read=True)
    CommentNotification.objects.filter(comment__ticket=ticket, receiver=user).update(is_read=True)
    MentionNotification.objects.filter(comment__ticket=ticket, receiver=user).update(is_read=True)
    NewTicketNotification.objects.filter(ticket=ticket, receiver=user).update(is_read=True)
    TicketReminderNotification.objects.filter(ticket=ticket, receiver=user).update(is_read=True)
