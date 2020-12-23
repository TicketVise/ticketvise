"""
Scheduling
-------------------------------
Schedules the ticket according to its labels or the scheduling policy of
the inbox.
"""
from functools import reduce
import operator
import random

from django.db.models import Q

from ticketvise.models.inbox import InboxUserSection, SchedulingAlgorithm


def schedule_ticket(ticket):
    """
    Assign a :class:`Ticket` to the proper :class:`User`.
    To assign a ticket to the proper user, a scheduling algorithm is used that can be derived from the ticket.
    If the ticket has a label with a priority, then the ticket is scheduled by the scheduling algorithm of the label.
    If the ticket has no label with a prioruty, then the ticket is scheduled by the scheduling algorithm of the inbox.

    :param Ticket ticket: The ticket to schedule.

    :return: None.
    """
    if ticket.inbox.scheduling_algorithm == SchedulingAlgorithm.ROUND_ROBIN:
        schedule_round_robin(ticket)
    elif ticket.inbox.scheduling_algorithm == SchedulingAlgorithm.LEAST_ASSIGNED_FIRST:
        schedule_least_assigned_first(ticket)
    elif ticket.inbox.scheduling_algorithm == SchedulingAlgorithm.SECTIONS:
        schedule_sections(ticket)
    elif ticket.inbox.scheduling_algorithm == SchedulingAlgorithm.FIXED:
        return ticket.assign_to(ticket.inbox.fixed_scheduling_assignee)
    else:
        raise NotImplementedError(f"Scheduling algorithm {ticket.inbox.scheduling_algorithm} not implemented.")


def schedule_round_robin(ticket):
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
    inbox_assistants = inbox.get_assignable_assistants_and_coordinators()
    num_assistants = inbox_assistants.count()
    new_assignee = inbox_assistants[inbox.round_robin_parameter % num_assistants]
    inbox.round_robin_parameter_increase()
    ticket.assign_to(new_assignee)


def schedule_least_assigned_first(ticket):
    """
    Assign a ticket to a random assistant that is assigned the least number of tickets.

    :param Ticket ticket: :class:`Ticket` that needs to be assigned.

    :return: None.
    """
    inbox = ticket.inbox
    inbox_assistants = inbox.get_assignable_assistants_and_coordinators()
    min_assigned = []
    min_count = float("inf")

    # Find the assistants that are assigned to the least number of tickets.
    for assistant in inbox_assistants:
        assigned_count = inbox.tickets.filter(assignee=assistant, status="ASGD").count()

        if not min_assigned or assigned_count <= min_count:
            if assigned_count == min_count or not min_assigned:
                min_assigned.append(assistant)
            else:
                min_assigned = [assistant]
                min_count = assigned_count

    ticket.assign_to(random.choice(min_assigned))


def schedule_sections(ticket):
    """
    Assign a ticket to the assistant that corresponds to the section.

    :param Ticket ticket: :class:`Ticket` that needs to be assigned.

    :return: None.
    """
    inbox_staff = ticket.inbox.get_assignable_assistants_and_coordinators()
    sections = InboxUserSection.objects.filter(reduce(operator.or_, (Q(section=x.section) for x in ticket.author.inbox_sections.all())))
    staff = inbox_staff.filter(reduce(operator.or_, (Q(inbox_sections=x) for x in sections)))
    
    # If no assistant in linked through sections we just choose one out of every TA.
    if len(staff) == 0:
        staff = inbox_staff

    ticket.assign_to(random.choice(staff))
