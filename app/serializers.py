
from rest_framework import serializers
from .models import UserRegister
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token


class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password')
    profile_image = serializers.FileField()
    permission_classes = [AllowAny]

    class Meta:
        model = UserRegister
        fields = ('username', 'email', 'password', 'profile_image', 'token')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['user']['username'],
                                        email=validated_data['user']['email'], password=validated_data['user']['password'])
        token = Token.objects.get(user=user)
        print("user create: ", token)
        return UserRegister(user=user, profile_image=validated_data['profile_image'])


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(label='Email Address', required=False, allow_blank=True)
    permission_classes = [AllowAny]

    class Meta:
        model = User
        fields = ('username', 'email', 'password',  'token')
        extra_kwargs = {"password":
                            {"write_only": True},
                        }

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password")
        if not email and not username:
            raise ValidationError("A user name or email is required to login")

        user = authenticate(username=username, password=password)
        if user:
            user_obj = User.objects.get(username=username, email=email)
        else:
            raise ValidationError("Incorrect username of password")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect password")

        token = Token.objects.get(user=user_obj)
        data["token"] = token
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticatedOrReadOnly]
    class Meta:
        model = User
        fields = '__all__'
