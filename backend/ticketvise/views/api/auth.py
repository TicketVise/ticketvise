from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from ticketvise.security.token import token_expire_handler, expires_in
from ticketvise.views.api.user import UserSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class LoginApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_401_UNAUTHORIZED)

        # Retrieving token of user, checking if not expired otherwise a create new one.
        token, _ = Token.objects.get_or_create(user=user)
        is_expired, token = token_expire_handler(token)

        return Response({
            'user': UserSerializer(user).data,
            'expires_in': expires_in(token),
            'token': token.key
        })
