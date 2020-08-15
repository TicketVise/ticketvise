"""
Scheduling
-------------------------------
Schedules the ticket according to its labels or the scheduling policy of
the inbox.
"""
from ticketvise.models.inbox import Inbox, SchedulingAlgorithm
from ticketvise.models.ticket import Ticket


def schedule_ticket(ticket: Ticket):
    """
    Assign a :class:`Ticket` to the proper :class:`User`.
    To assign a ticket to the proper user, a scheduling algorithm is used that can be derived from the ticket.
    If the ticket has a label with a priority, then the ticket is scheduled by the scheduling algorithm of the label.
    If the ticket has no label with a prioruty, then the ticket is scheduled by the scheduling algorithm of the inbox.

    :param Ticket ticket: The ticket to schedule.

    :return: None.
    """
    schedule(ticket.inbox.scheduling_algorithm, ticket)


def schedule_by_inbox(inbox: Inbox):
    """
    Gets the scheduling algorithm of a :class:`Inbox`.

    :param Inbox inbox: The inbox to get the scheduling algorithm of.

    :return: The scheduling algorithm of the inbox.
    :rtype: str
    """
    return inbox.scheduling_algorithm


def schedule(scheduling_algorithm, ticket: Ticket):
    """
    Schedule a ticket (i.e. assign it to the right TA according to the scheduling algorithm).

    :param str scheduling_algorithm: Scheduling algorithm to use.
    :param Ticket ticket: :class:`Ticket` to schedule.
    :param Label label: :class:`Label` that was used to schedule the ticket. Can be ``None``.
    :param bool use_inbox_algorithm: Whether to use the :class:`Inbox` scheduling
                                      algorithm or the :class:`Label` scheduling algorithm.

    :return: None.

    :raises NotImplementedError: When the scheduling algorithm is invalid.
    """
    if scheduling_algorithm == SchedulingAlgorithm.ROUND_ROBIN:
        schedule_round_robin(ticket)
    elif scheduling_algorithm == SchedulingAlgorithm.LEAST_ASSIGNED_FIRST:
        schedule_least_assigned_first(ticket)
    elif scheduling_algorithm == SchedulingAlgorithm.MANUAL:
        return
    else:
        raise NotImplementedError("It seems like the scheduling algorithm you wanted to use is undefined!")


def schedule_round_robin(ticket: Ticket):
    """
    Assign a ticket to the assistants in a round-robin fashion.
    The round-robin scheduling is done globally for the inbox: each label contributes
    to the round-robin parameter of the inbox.

    :param Ticket ticket: :class:`Ticket` that needs to be scheduled.
    :param Label label: :class:`Label` that was used to schedule the ticket.
    :param bool use_inbox_algorithm: Whether to use the :class:`Inbox` scheduling
                                      algorithm or the :class:`Label` scheduling algorithm.

    :return: None.
    """
    inbox = ticket.inbox
    inbox_assistants = inbox.get_assistants_and_coordinators()
    num_assistants = inbox_assistants.count()
    new_assignee = inbox_assistants[inbox.round_robin_parameter % num_assistants]
    inbox.round_robin_parameter_increase()
    ticket.assign_to(new_assignee)


def schedule_least_assigned_first(ticket: Ticket):
    """
    Assign a ticket to the assistant that is assigned the least number of tickets.

    :param Ticket ticket: :class:`Ticket` that needs to be assigned.

    :return: None.
    """
    inbox = ticket.inbox
    inbox_assistants = inbox.get_assistants_and_coordinators()
    min_assignee = None
    min_count = None

    # Find the assistant that is assigned to the least number of tickets.
    for assistant in inbox_assistants:
        assigned_count = inbox.tickets.filter(assignee=assistant).count()

        if min_assignee is None or assigned_count < min_count:
            min_assignee = assistant
            min_count = assigned_count

    ticket.assign_to(min_assignee)
