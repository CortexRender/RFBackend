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
        if not is_superuser and 'password' not in validated_data:
            raise serializers.ValidationError("Password is required.")
        user = RFUser.objects.create(
            **validated_data,
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
        if not is_superuser and 'password' in validated_data:
            user.set_password(validated_data['password'])

        user.save()
        return user
