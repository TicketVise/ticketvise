import threading

from django.contrib.auth.models import AnonymousUser


class CurrentUserMiddleware:
    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        CurrentUserMiddleware.thread_local.request = request

        response = self.get_response(request)

        CurrentUserMiddleware.thread_local.request = None

        return response

    @staticmethod
    def get_current_user():
        request = getattr(CurrentUserMiddleware.thread_local, 'request', None)
        if not request or (request and isinstance(request.user, AnonymousUser)):
            return None

        return request.user
