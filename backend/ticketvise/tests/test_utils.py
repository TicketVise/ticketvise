from django.test import TestCase

from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role
from ticketvise.settings import DEFAULT_AVATAR_PATH
from ticketvise.utils import add_global_context


class UtilsTestCase(TestCase):
    def setUp(self):
        """
        Initialize the testing variables.
        """
        self.context = {}

    def test_global_context(self):
        """
        Test adding global context to a dictionary.
        """
        add_global_context(self.context)
        self.assertEqual(self.context, {
            "DEFAULT_AVATAR_PATH": DEFAULT_AVATAR_PATH,
            "ROLE_STUDENT": Role.GUEST,
            "ROLE_ASSISTANT": Role.AGENT,
            "ROLE_COORDINATOR": Role.MANAGER,
            "STATUS_PENDING": Ticket.Status.PENDING,
            "STATUS_ASSIGNED": Ticket.Status.ASSIGNED,
            "STATUS_ANSWERED": Ticket.Status.ANSWERED,
            "STATUS_CLOSED": Ticket.Status.CLOSED
        })
