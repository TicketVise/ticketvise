"""
Statistics
-------------------------------
Various utility functions used for displaying statistics to users.
"""
import datetime
from datetime import timedelta

from django.db.models import Count, Avg, Subquery, OuterRef, F

from ticketvise.models.comment import Comment, CommentHelpful
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, TicketLabel


def calculate_timedelta_hours(time):
    """
    Converts the timedelta to hours with one decimal.

    :param timedelta time: The timedelta.

    :return: Amount of hours in the timedelta. If the rounded number is 0, return 0.1.
    :rtype: float
    """
    return round(time.total_seconds() / 3600, 1) or 0.1 if time.total_seconds() else 0.0


def get_amount_all_tickets(inbox):
    """
    Get the amount of tickets in a inbox.

    :param Inbox inbox: The inbox where to search for tickets.

    :return: The amount of tickets in the inbox.
    :rtype: int
    """
    return Ticket.objects.filter(inbox=inbox).count()


def get_amount_type(inbox, status):
    """
    Get the amount of tickets in a inbox with a given status.

    :param Inbox inbox: The inbox where to search for tickets.
    :param Ticket.Status status: The status which a ticket has to have to be counted.

    :return: The amount of tickets with the given status in a inbox.
    :rtype: int
    """
    return Ticket.objects.filter(inbox=inbox, status=status).count()


def get_amount_ticket_label(inbox, label):
    """
    Get the amount of tickets in a inbox with a label.

    :param Inbox inbox: The inbox where to search for tickets.
    :param Label label: The label which a ticket has to have to be counted.

    :return: The amount of tickets with the given label in a inbox.
    :rtype: int
    """
    return Ticket.objects.filter(inbox=inbox, labels=label).count()


def get_amount_labels(inbox):
    """
    Get the amount of tickets for every label in a inbox.

    :param Inbox inbox: The inbox where to search for tickets and labels.

    :return: A ditctionary where a label is mapped to the amount of tickets
             with the given label in a inbox.
    :rtype: list
    """
    result_list = []

    for label in Label.objects.filter(inbox=inbox):
        result_list.append([label, get_amount_ticket_label(inbox, label)])

    return result_list


def get_popular_labels(inbox):
    """
    Get a list of tuples with the names of the top 5 most
    popular labels and the number of times they were used.

    :param Inbox inbox: The inbox of which we need the 5 most popular tickets.

    :return: A list of 5 tuples with the label and the number of use cases.
    :rtype: list
    """
    return sorted(get_amount_labels(inbox), reverse=True, key=lambda x: x[1])[:5]


def get_response_time_ticket(ticket):
    """
    Get the response time of a TA on a single ticket.

    :param Ticket ticket: The ticket of which we need to response time.

    :return: The response time of a single ticket (Datetime object).
    :rtype: timedelta
    """
    ticket_date_created = ticket.date_created
    teachers = ticket.inbox.get_assistants_and_coordinators()
    comments = ticket.comments.all().filter(ticket=ticket, author__in=teachers, is_reply=True).order_by("date_created")

    if comments.count() == 0:
        return timedelta(0)

    ticket_date_first_response = comments[0].date_created

    return ticket_date_first_response - ticket_date_created


def get_average_response_time_ta(inbox, ta):
    """
    Get the average response time of a TA in a inbox.

    :param Inbox inbox: The inbox where to search.
    :param User ta: The TA of which the response time is queried.

    :return: The average response time of a TA in a inbox on the tickets.
    :rtype: timedelta
    """
    tickets = Ticket.objects.filter(inbox=inbox, assignee=ta, comments__author=ta, comments__is_reply=True).distinct()

    if not tickets.count():
        return timedelta(0)

    return sum([get_response_time_ticket(ticket) for ticket in tickets], timedelta(0)) / tickets.count()


# def get_average_response_time_all_ta_2(inbox):
#     return Ticket.objects.filter(inbox=inbox, comments__is_reply=True) \
#         .annotate(response_time=F('date_created') - F('comments__date_created')) \
#         .aggregate(avg_response_time=Avg('response_time')) \
#         .values('assignee') \
#         .orderby('response_time')


def get_average_response_time_all_ta(inbox):
    """
    Get the average response times of all TAs in a inbox.

    :param Inbox inbox: The inbox where to search.

    :return: The average response times of all TAs in a inbox on the tickets.
    :rtype: list
    """

    result_list = []
    tas = inbox.get_assistants_and_coordinators()

    for ta in tas:
        result_list.append([ta, calculate_timedelta_hours(get_average_response_time_ta(inbox, ta))])

    return result_list


def get_average_response_time(inbox):
    """
    Get the average response time in a inbox.

    :param Inbox inbox: The inbox where to search.

    :return: The average response time in a inbox on the tickets.
    :rtype: float
    """
    recent_comment_ids = Comment.objects.filter(ticket__inbox=inbox, is_reply=True) \
        .order_by("ticket", "-date_created") \
        .distinct("ticket") \
        .values("id")

    avg_response_time = Comment.objects.filter(id__in=Subquery(recent_comment_ids)) \
        .annotate(response_time=F('date_created') - F('ticket__date_created')) \
        .aggregate(avg_response_time=Avg("response_time"))

    result = avg_response_time["avg_response_time"] if avg_response_time["avg_response_time"] else datetime.timedelta()
    return calculate_timedelta_hours(result)


def get_amount_ticket_assigned_answered_closed(inbox):
    """
    Get the amount of assigned, amount of answered and amount of closed for each TA.

    :param Inbox inbox: The inbox where to search.

    :return: The amount of tickets which were assigned to a TA for all TAs.
    :rtype: list
    """
    assigned_list = get_amount_type_all_assistants(inbox, Ticket.Status.ASSIGNED)
    answered_list = get_amount_type_all_assistants(inbox, Ticket.Status.ANSWERED)
    closed_list = get_amount_type_all_assistants(inbox, Ticket.Status.CLOSED)

    return [
        [ta, assigned, answered, closed]
        for (ta, assigned), (_, answered), (_, closed) in zip(assigned_list, answered_list, closed_list)
    ]


def get_amount_type_student(inbox, status, student):
    """
    Get the amount of tickets from a student in a inbox with a given status.

    :param Inbox inbox: The inbox where to search for tickets.
    :param Ticket.Status status: The status which a ticket has to have to be counted.
    :param User assistant: The assistant of which we want the amount of tickets with a given status.

    :return: The amount of tickets with the given status in a inbox.
    :rtype: int
    """
    return Ticket.objects.filter(inbox=inbox, status=status, author=student).count()


def get_amount_student_ticket_label(inbox, student, label):
    """
    Get the amount of tickets from a student in a inbox with a label.

    :param Inbox inbox: The inbox where to search for tickets.
    :param User student: The student of which we need the label amount.
    :param Label label: The label which a ticket has to have to be counted.

    :return: The amount of tickets with the given label in a inbox.
    :rtype: int
    """
    return Ticket.objects.filter(author=student, inbox=inbox, labels=label).count()


def get_amount_student_labels(inbox, student):
    """
    Get the amount of tickets for every label in a inbox.

    :param Inbox inbox: The inbox where to search for tickets and labels.
    :param User student: The student of which we need the label amounts.

    :return: A ditctionary where a label is mapped to the amount of tickets
             with the given label in a inbox for a student.
    :rtype: list
    """
    result_list = []

    for label in Label.objects.filter(inbox=inbox):
        result_list.append([label, get_amount_student_ticket_label(inbox, student, label)])

    return result_list


def get_popular_used_labels(inbox, student):
    """
    Get a list of tuples with the names of the top 5 most
    popular labels and the number of times they were used.

    :param Inbox inbox: The inbox of which we need the 5 most popular tickets.
    :param User student: The student of which we need the 5 most popular tickets.

    :return: A list of tuples with the label and the number of use cases.
    :rtype: list
    """
    return sorted(get_amount_student_labels(inbox, student), reverse=True, key=lambda x: x[1])[:5]


def get_amount_tickets_days(inbox, student):
    """
    Get a list of tuples with the amount of tickets were created for each day.

    :param Inbox inbox: The inbox of which we need the tickets.
    :param User student: The student by which the tickets are created.

    :return: A list of tuples with the amount of tickets and the day.
    :rtype: list
    """
    return (
        inbox.get_tickets_by_author(student).values_list("date_created__date").annotate(amount=Count("date_created"))
    )


def average_response_time_of_tickets(inbox, student):
    """
    Get the average response time over all of the student's tickets.

    :param Inbox inbox: The inbox of which we need the tickets.
    :param User student: The student by which the tickets are created.

    :return: Average response time over all of the student's tickets.
    :rtype: float
    """
    student_tickets = inbox.get_tickets_by_author(student)

    if student_tickets.count() == 0:
        average_response_time = timedelta(0)
    else:
        average_response_time = (
                sum([get_response_time_ticket(ticket) for ticket in student_tickets], timedelta(0))
                / student_tickets.count()
        )

    return calculate_timedelta_hours(average_response_time)


def get_ticket_responders_data(inbox, student):
    """
    Convert the mapping from responders to respond count to table data for
    the front-end.

    :param Inbox inbox: Inbox to get the data from.
    :param User student: Student to get the tickets from.

    :return: Data formatted for front-end.
    :rtype: list
    """
    data = []
    tickets = inbox.get_tickets_by_author(student)
    teachers = inbox.get_assistants_and_coordinators()
    raw_data = get_ticket_responders(tickets, teachers)

    for teacher, value in raw_data.items():
        data.append([teacher.get_full_name(), value["amount"]])

    return data


def get_ticket_responders(tickets, teachers):
    """
    Map the responders of tickets to the amount of times they responded.
    Loops over all tickets, and gets the assistent that responded to
    the ticket first.

    :param list tickets: Tickets to get responders of.
    :param list teachers: Teachers to filter by.

    :return: Data that maps responders to the amount of times they responded.
    :rtype: dict
    """
    teachers_to_amount = {}

    for ticket in tickets:
        responder_comments = ticket.comments.filter(author__in=teachers, is_reply=True).order_by("date_created")

        if responder_comments.count() > 0:
            responder_comment = responder_comments[0]
            author = responder_comment.author
            date = responder_comment.date_created

            if author not in teachers_to_amount.keys():
                teachers_to_amount[author] = {"amount": 1, "dates": {date: 1}, "comments": [responder_comment.id]}
            else:
                teachers_to_amount[author]["amount"] += 1
                teachers_to_amount[author]["comments"].append(responder_comment.id)

                if date not in teachers_to_amount[author]["dates"].keys():
                    teachers_to_amount[author]["dates"][date] = 1
                else:
                    teachers_to_amount[author]["dates"][date] += 1

    return teachers_to_amount


def get_amount_type_assistant(inbox, status, assistant):
    """
    Get the amount of tickets of an asistant in a inbox with a given status.

    :param Inbox inbox: The inbox where to search for tickets.
    :param Ticket.Status status: The status which a ticket has to have to be counted.
    :param User assistant: The assistant of which we want the amount of tickets with a given status.

    :return: The amount of tickets with the given status in a inbox.
    :rtype: int
    """
    return Ticket.objects.filter(inbox=inbox, status=status, assignee=assistant).count()


def get_amount_type_all_assistants(inbox, status):
    """
    Get the amount of tickets which were assigned to a TA for all TAs.

    :param Inbox inbox: The inbox where to search.
    :param Ticket.Status status: The status of the ticket.

    :return: The amount of tickets which were assigned to a TA for all TAs.
    :rtype: list
    """
    assistants = inbox.get_assistants_and_coordinators()

    return [[assistant, get_amount_type_assistant(inbox, status, assistant)] for assistant in assistants]


def get_last_5_processed_tickets_ta(inbox, assistant):
    """
    Get the 5 most recently processed tickets of a given TA.

    The query for ticket_dicts will contain a ticket multiple times when a TA
    replied to it multiple times, so we need to remove the duplicates using:
    https://www.w3schools.com/python/python_howto_remove_duplicates.asp

    :param Inbox inbox: The inbox where to search.
    :param User assistant: The assistant of which we want to get the 5 most recently processed tickets.

    :return: The 5 most recently processed tickets of a given TA.
    :rtype: list
    """
    answered_tickets = inbox.get_tickets_by_assignee(assistant, status=Ticket.Status.ANSWERED)
    closed_tickets = inbox.get_tickets_by_assignee(assistant, status=Ticket.Status.CLOSED)
    processed_tickets = answered_tickets | closed_tickets

    ticket_dicts = (
        Comment.objects.filter(ticket__in=processed_tickets, author=assistant, is_reply=True).order_by(
            "-date_created").values("ticket")[:5]
    )
    list_of_tickets = [Ticket.objects.get(pk=ticket["ticket_id"]) for ticket in ticket_dicts.values()]
    tickets_no_dups = list(dict.fromkeys(list_of_tickets))

    return tickets_no_dups


def response_time_tickets(tickets):
    """
    Get the response times of a list of tickets.

    :param list tickets: A list of tickets.

    :return: A list of response times of the given tickets.
    :rtype: list
    """
    return [calculate_timedelta_hours(get_response_time_ticket(ticket)) for ticket in tickets]


def get_amount_responses_days(inbox, assistant):
    """
    Get the amount of tickets responded to per day.

    :param Inbox inbox: The inbox of which we need the tickets.
    :param User assistant: The assistant that responed to tickets.

    :return: A list of tickets responded to per day.
    :rtype: list
    """
    mapping = get_ticket_responders(inbox.tickets.all(), [assistant])

    if assistant in mapping.keys():
        comments_by_date = (
            Comment.objects.filter(pk__in=mapping[assistant]["comments"]).values_list("date_created__date").annotate(
                amount=Count("date_created"))
        )
        comments_by_date = [
            [f"{mapping[0].year}-{mapping[0].month}-{mapping[0].day}", mapping[1]] for mapping in comments_by_date
        ]

        return comments_by_date

    return []


def get_most_answered_label_ta(inbox, ta):
    """
    Get the most answered label for the given TA in an inbox.
    """
    tickets = TicketLabel.objects.filter(ticket__inbox=inbox, ticket__assignee=ta, ticket__comments__author=ta, ticket__comments__is_reply=True).distinct()
    
    return tickets[0].label if tickets.count() > 0 else None


def get_amount_of_helpful_reacted_comments(inbox, ta):
    """
    Get the number of comments of the given TA that were reacted with helpful or not helpful.
    """
    amount = CommentHelpful.objects.filter(comment__ticket__inbox=inbox, comment__author=ta, comment__is_reply=True).count()

    return amount


def get_helpfulness(inbox, ta):
    """
    Get the helpfulness of the given TA in an inbox.
    """
    total = get_amount_of_helpful_reacted_comments(inbox, ta)
    amount = CommentHelpful.objects.filter(comment__ticket__inbox=inbox, comment__author=ta, comment__is_reply=True, is_helpful=True).count()

    return (amount / total) * 100 if total > 0 else 0
