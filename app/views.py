from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView

from .models import UserRegister, User
from .serializers import UserLoginSerializer, UserRegisterSerializer, UserProfileSerializer


class UserRegesterViewSet(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UserRegister.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = (TokenAuthentication,)

class UserLoginViewSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return  Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutViewSet(APIView):
    queryset = User.objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer
