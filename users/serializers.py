from rest_framework import serializers
from .models import RFUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFUser
        fields = ('id', 'username', 'email', 'render_coin', 'is_superuser')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFUser
        fields = ('username', 'password', 'email', 'render_coin', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def validate(self, attrs):
        if attrs.get('is_superuser') and 'password' in attrs:
            raise serializers.ValidationError("Superusers cannot have a password at creation.")
        return attrs

    def create(self, validated_data):
        is_superuser = validated_data.pop('is_superuser', False)
        password = validated_data.pop('password', None)

        if not is_superuser and not password:
            raise serializers.ValidationError({"password": "Password is required."})

        user = RFUser.objects.create(
            **validated_data,
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
        if password:
            user.set_password(password)

        user.save()
        return user
