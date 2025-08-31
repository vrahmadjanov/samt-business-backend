from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import BusinessUser


class BusinessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = ['id', 'phone_number', 'email', 'first_name', 'last_name']


class BusinessTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Явно указываем, что логинимся по полю phone_number
    username_field = 'phone_number'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone_number'] = user.phone_number
        return token


class BusinessTokenObtainPairView(TokenObtainPairView):
    serializer_class = BusinessTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(BusinessUserSerializer(request.user).data)
