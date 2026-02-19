from rest_framework import serializers
from listly_app.models import listly_user, task


class list_serializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        queryset=listly_user.objects.all(), slug_field="user_name"
    )

    class Meta:
        model = task
        fields = [
            "id",
            "username",
            "description",
            "completed",
            "created_at",
            "updated_at",
        ]