from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', "password", 'email', 'account_id']
        # read_only_fields = ['password']

    # def create(self, validated_data):
    #     print("USer => Create")
    #     instance = super().create(validated_data)
    #     if not instance.password.startswith("pbkdf2_sha256"):
    #         instance.password = instance.set_password(instance.password)
    #     instance.save()
    #
    #
    # def update(self, instance, validated_data):
    #     print("USer => Create")
    #     instance = super().create(validated_data)
    #     if not instance.password.startswith("pbkdf2_sha256"):
    #         instance.password = instance.set_password(instance.password)
    #     instance.save()



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    class Meta:
        # model = User
        fields = ['username', 'password']

    # def validate(self, attrs):
    #     """Validate the username and password"""
    #     user_data = {}
    #     username = attrs.get('username')
    #     password = attrs.get('password')
    #
    #     if username and password:
    #         # Authenticate the user
    #         user = authenticate(username=username, password=password)
    #         if not user:
    #             raise serializers.ValidationError("Invalid username or password.")
    #         user_data["username"] = user.username
    #         user_data["user"] = user
    #         user_data["email"] = user.email
    #     else:
    #         raise serializers.ValidationError("Both username and password are required.")
    #
    #     # Attach the user object to the serializer for further processing
    #     return user_data

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)
    class Meta:
        fields = ['password', "confirm_password"]
