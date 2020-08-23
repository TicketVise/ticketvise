import threading

from django.contrib.auth.models import AnonymousUser


class CurrentUserMiddleware:
    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        CurrentUserMiddleware.thread_local.current_user = request.user

        response = self.get_response(request)

        CurrentUserMiddleware.thread_local.current_user = None

        return response

    @staticmethod
    def get_current_user():
        user = getattr(CurrentUserMiddleware.thread_local, 'current_user', None)
        if isinstance(user, AnonymousUser):
            return None

        return user
