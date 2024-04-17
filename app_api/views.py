from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app_api.mixins.token import TokenAPIMixin
from app_api.models import Country
from app_api.serializers import CountrySerializer, UserLoginSerializer, \
    UserListSerializer
from rest_framework.authtoken.models import Token


# Create your views here.
class CountryListView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    @swagger_auto_schema(
        responses={
            200: CountrySerializer(many=True),
            400: 'Bad Request',
        },
        tags=['Countries'],
    )
    def get(self, request):
        serializer = CountrySerializer(Country.objects.all(), many=True)
        return Response(serializer.data)


class AuthAPIView(APIView, TokenAPIMixin):

    permission_classes = [
    ]

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: 'User successfully logged in',
            400: 'Bad Request',
            401: 'Invalid login credentials'
        },
        tags=['Authentication'],
    )
    def post(self, request):
        """
        Do system's authentication and with correct credentials returns
        user serialized object
        """
        login_serializer = UserLoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            return Response(
                login_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = authenticate(
                username=login_serializer.data.get('username', ''),
                password=login_serializer.data.get('password', '')
            )
            if not user:
                return Response(
                    {'error': 'Invalid login credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)
        is_expired, token = self._handle_expiration(token)
        user_serialized = UserListSerializer(user)
        return Response({
            'user': user_serialized.data,
            'expires_in': self._expires_in(token),
            'access_token': token.key,
        }, status=status.HTTP_200_OK)


class AuthLogoutAPIView(APIView, TokenAPIMixin):

    permission_classes = [
        IsAuthenticated
    ]

    @swagger_auto_schema(
        responses={
            200: 'User successfully logged out',
            400: 'Bad Request',
            401: 'Invalid login credentials'
        },
        tags=['Authentication'],
    )
    def post(self, request):
        """
        Do logout for a logged in user
        """
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if token:
            token = token.split(' ')[1]
            try:
                t = Token.objects.get(key=token)
                Token.objects.filter(user=t.user).delete()
            except Exception as e:
                pass
            return Response({
                'message': 'Logged Out'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Not Authorized',
            }, status=status.HTTP_401_UNAUTHORIZED)
