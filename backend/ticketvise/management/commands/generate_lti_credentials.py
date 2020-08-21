import secrets

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command that generates LTI credentials"""

    def handle(self, *args, **options):
        print("LTI_KEY:", secrets.token_hex(16))
        print("LTI_SECRET:", secrets.token_hex(32))
