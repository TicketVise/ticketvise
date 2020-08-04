"""
Scheduling
-------------------------------
Schedules the ticket according to its labels or the scheduling policy of
the course.
"""
from ticketvise.models.course import Course, SchedulingAlgorithm
from ticketvise.models.ticket import Ticket


def schedule_ticket(ticket: Ticket):
    """
    Assign a :class:`Ticket` to the proper :class:`User`.
    To assign a ticket to the proper user, a scheduling algorithm is used that can be derived from the ticket.
    If the ticket has a label with a priority, then the ticket is scheduled by the scheduling algorithm of the label.
    If the ticket has no label with a prioruty, then the ticket is scheduled by the scheduling algorithm of the course.

    :param Ticket ticket: The ticket to schedule.

    :return: None.
    """
    schedule(ticket.course.scheduling_algorithm, ticket)


def schedule_by_course(course: Course):
    """
    Gets the scheduling algorithm of a :class:`Course`.

    :param Course course: The course to get the scheduling algorithm of.

    :return: The scheduling algorithm of the course.
    :rtype: str
    """
    return course.scheduling_algorithm


def schedule(scheduling_algorithm, ticket: Ticket):
    """
    Schedule a ticket (i.e. assign it to the right TA according to the scheduling algorithm).

    :param str scheduling_algorithm: Scheduling algorithm to use.
    :param Ticket ticket: :class:`Ticket` to schedule.
    :param Label label: :class:`Label` that was used to schedule the ticket. Can be ``None``.
    :param bool use_course_algorithm: Whether to use the :class:`Course` scheduling
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
    The round-robin scheduling is done globally for the course: each label contributes
    to the round-robin parameter of the course.

    :param Ticket ticket: :class:`Ticket` that needs to be scheduled.
    :param Label label: :class:`Label` that was used to schedule the ticket.
    :param bool use_course_algorithm: Whether to use the :class:`Course` scheduling
                                      algorithm or the :class:`Label` scheduling algorithm.

    :return: None.
    """
    course = ticket.course
    course_assistants = course.get_assistants_and_coordinators()
    num_assistants = course_assistants.count()
    new_assignee = course_assistants[course.round_robin_parameter % num_assistants]
    course.round_robin_parameter_increase()
    ticket.assign_to(new_assignee)


def schedule_least_assigned_first(ticket: Ticket):
    """
    Assign a ticket to the assistant that is assigned the least number of tickets.

    :param Ticket ticket: :class:`Ticket` that needs to be assigned.

    :return: None.
    """
    course = ticket.course
    course_assistants = course.get_assistants_and_coordinators()
    min_assignee = None
    min_count = None

    # Find the assistant that is assigned to the least number of tickets.
    for assistant in course_assistants:
        assigned_count = course.tickets.filter(assignee=assistant).count()

        if min_assignee is None or assigned_count < min_count:
            min_assignee = assistant
            min_count = assigned_count

    ticket.assign_to(min_assignee)
