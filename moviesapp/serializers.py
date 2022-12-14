from django.db import transaction
from rest_framework import serializers
from moviesapp.models import User

# from moviesapp.models import Collection, Movie


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate(self, data, *args, **kwargs):
        return super(UserCreateSerializer, self).validate(data, *args, **kwargs)

    @transaction.atomic()
    def create(self, validated_data):
        # Register new users
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "password",
            "username",
            "first_name",
            "last_name",
            "role",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "role")


# class CollectionsCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Collection
#         fields = ("id", "user_id")

#     def create(self, validated_data):
#         user = User.objects.get(pk=validated_data.pop("user"))
#         return Collection.objects.create(**validated_data, user=user)


# class CollectionsListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Collection
#         fields = ("id", "user_id")
