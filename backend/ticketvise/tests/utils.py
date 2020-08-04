"""
(Test) Utils
-------------------------------
These are the utils that are used for the tests.
"""
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits

from ticketvise.models.comment import Comment
from ticketvise.models.course import Course
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User


def random_string(size=6, chars=ascii_uppercase + ascii_lowercase + digits):
    """
    Generate a random string.
    Code source: https://stackoverflow.com/a/2257449

    :param int size: size of string (default: 6).
    :param str chars: possible characters (default: all letters and digits).

    :return: Random string of `size` characters.
    :rtype: str
    """
    return ''.join(choice(chars) for _ in range(size))


def random_email():
    """
    Generate a random email address.

    :return: A random email address.
    :rtype: str
    """
    return random_string() + "@" + random_string() + "." + random_string(3)


def random_color():
    """
    Generate a hexadecimal random color.

    :return: A random color.
    :rtype: str
    """
    return f"#{random_string(chars=digits)}"


def create_course(name="", code="", color=""):
    """
    Create new course with random course code and color

    :param str name: Name of the course.
    :param str code: Code of the course.
    :param str color: Color of the course.

    :return: Course.
    :rtype: Course
    """
    name = name or random_string()
    code = code or random_string()
    color = color or random_color()

    return Course.objects.create(name=name, code=code, color=color)


def create_label(course=None, name="", color="", is_form_label=True, is_active=True):
    """
    Create a new label with random color for testing.

    :param Course course: Associated course.
    :param str name: Name of the label.
    :param str color: Colorcode of the label.
    :param str scheduling_algorithm: Associated algorithm for scheduling.
    :param int scheduling_priority: Associated scheduling priority.
    :param bool is_form_label: Can a student use it in ticket submission.
    :param bool is_active: Can the label be used.

    :return: Label.
    :rtype: Label
    """
    course = course or create_course()
    name = name or random_string()
    color = color or random_color()

    return Label.objects.create(course=course, name=name, color=color,
                                is_form_label=is_form_label,
                                is_active=is_active)


def create_user(username="", password="", email="", first_name="", last_name=""):
    """
    Create a new user with a role and a course in the database.

    :param str username: Username of the user.
    :param str password: Password of the user.
    :param str email: Email of the user.

    :return: Newly created user.
    :rtype: User
    """
    username = username or random_string()
    password = password or random_string()
    email = email or random_email()

    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                    email=email)
    user.set_password(password)
    user.save()

    return user

def create_ticket(author=None, assignee=None, course=None, title="",
                  status=Ticket.Status.PENDING, content="", labels=[]):
    """
    Create a ticket with random content for testing.

    :param User author: Author of ticket.
    :param User assignee: User assigned to ticket.
    :param Course course: Associated course.
    :param str title: Title of ticket.
    :param str status: The status of the ticket.

    :return: Ticket.
    :rtype: Ticket
    """
    author = author or create_user()
    course = course or create_course()
    title = title or random_string()
    content = content or random_string()

    ticket = Ticket.objects.create(author=author, assignee=assignee, course=course,
                                   title=title, content=content, status=status)
    for label in labels:
        ticket.labels.add(label)
    return ticket


def create_comment(ticket=None, author=None, content="",
                   is_reply: bool = False, is_active=True):
    """
    Create a comment with random content for testing.

    :param Ticket ticket: Associated ticket.
    :param User author: Author of comment.
    :param dict content: Content of comment.
    :param bool is_reply: Boolean to distinguish between comments and replies.

    :return: Comment.
    :rtype: Comment
    """
    ticket = ticket or create_ticket()
    author = author or create_user()
    content = content or random_string()

    return Comment.objects.create(ticket=ticket, author=author, content=content, is_reply=is_reply, is_active=is_active)