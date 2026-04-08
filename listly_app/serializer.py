from rest_framework import serializers
from listly_app.models import listly_user, task


class UserTaskSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=50,
        error_messages={
            "does_not_exist": "User with this username does not exist. Please provide a valid username.",
            "required": "Username is required.",
            "blank": "Username cannot be blank.2",
            "null": "Username cannot be null.",
            "invalid": "Invalid username format.",
        },
    )

    class Meta:
        model = task
        fields = [
            "pk",
            "username",
            "description",
            "completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "pk"]

        extra_kwargs = {
            "description": {
                "error_messages": {
                    "blank": "Description cannot be empty. shala description de"
                }
            }
        }

    def create(self, validated_data):
        print(self.validated_data)
        userName = validated_data["username"]
        userName.user_name = userName.user_name + "_listly"
        description = validated_data["description"]
        completed = validated_data.get("completed", False)
        user, created = listly_user.objects.get_or_create(user_name=userName)
        task_instance = task.objects.create(
            username=user, description=description, completed=completed
        )
        return task_instance

    def validate_username(self, value):
        for ele in value:
            if ele.isdigit():
                raise serializers.ValidationError(
                    "Username cannot contain digits. Please provide a valid username."
                )
        return value

    def validate_description(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Description must be at least 5 characters long."
            )
        return value

class TaskListSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = task
        fields = ["description", "completed", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    userTasks = TaskListSerializer(many=True, read_only=True)
    total_tasks = serializers.SerializerMethodField()

    get_total_tasks = lambda self, obj: obj.userTasks.count()
    
    class Meta:
        model = listly_user
        fields = ["user_name", "userTasks", "total_tasks"]