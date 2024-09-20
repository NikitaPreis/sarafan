from core import constants as const
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=const.USER_EMAIL_MAXLENGHT,)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=const.USER_EMAIL_MAXLENGHT,)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
