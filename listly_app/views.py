from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Prefetch
from rest_framework import authentication, generics, permissions, serializers
from listly_app.authentication import TokenAuth
from listly_app.forms import listly_user_form, newTask
from listly_app.models import listly_user, task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from listly_app.permissions import TasksPermission
from listly_app.serializer import UserSerializer, UserTaskSerializer
from django.contrib.sessions.models import Session
from rest_framework.pagination import PageNumberPagination

# Create your views here.
def to_do_app(request):
    print(request.session)
    return render(request, "welcome.html", {"form": listly_user_form()})


def user_lists(request):
    data = listly_user.objects.prefetch_related(
        Prefetch("userTasks", queryset=task.objects.filter(completed=False))
    ).all()
    return render(request, "user_lists.html", {"data": data})


def listly_user_views(request):
    if request.method == "POST":
        form = listly_user_form(request.POST)
        if form.is_valid():
            listly_user.objects.get_or_create(user_name=form.cleaned_data["username"])
            request.session["user_name"] = form.cleaned_data["username"]
    return redirect("active_task")


def listly(request):
    userName = listly_user.objects.get(user_name=request.session["user_name"])
    if request.method == "POST":
        form = newTask(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            if task.objects.filter(
                description=description, completed=False, username=userName
            ).exists():
                messages.warning(
                    request, "⚠️ Task already exists. Please enter a unique task."
                )
                return redirect("active_task")
            task.objects.create(description=description, username=userName)
            messages.success(request, "✅ Task added successfully!")
            return redirect("active_task")
        else:
            messages.error(request, "❌ Invalid input. Please try again.")
            return redirect("active_task")

    data = task.objects.filter(completed=False, username=userName).order_by(
        "-created_at"
    )
    return render(
        request,
        "listly.html",
        {"data": data, "addTask": newTask(), "userName": userName},
    )


def completed_task(request):
    userName = listly_user.objects.get(user_name=request.session["user_name"])
    data = task.objects.filter(completed=True, username=userName).order_by(
        "-created_at"
    )
    return render(request, "completed.html", {"data": data, "addTask": newTask()})


def mark_as_complete(request, pk):
    data = task.objects.get(pk=pk)
    data.completed = True
    data.save()
    messages.success(request, "✅ Task completed!")
    return redirect("active_task")


def delete_single_task(request, pk):
    data = task.objects.get(pk=pk)
    data.delete()
    messages.success(request, "✅ Task deleted successfully!")
    return redirect("completed_task")


def edit_task(request, pk):
    userName = listly_user.objects.get(user_name=request.session["user_name"])
    if request.method == "POST":
        form = newTask(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            obj = task.objects.get(pk=pk)
            if obj.description == description:
                messages.warning(request, "⚠️ didnt change anything")
                return redirect("active_task")
            obj.description = description
            obj.save()
            messages.success(request, "✅ Task updated successfully!")
            return redirect("active_task")
        else:
            messages.error(request, "❌ Invalid input. Please try again.")
            return redirect("active_task")

    data = task.objects.filter(completed=False, username=userName).order_by(
        "-created_at"
    )
    edited_data = task.objects.get(pk=pk)
    form = newTask(initial={"description": edited_data.description})
    return render(
        request,
        "listly.html",
        {"data": data, "addTask": form, "edit_task": edited_data, "userName": userName},
    )


class task_add(generics.CreateAPIView):
    """
    API view to create a new task.
    """

    queryset = task.objects.select_related("username").all()
    serializer_class = UserTaskSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            userName = serializer.validated_data["username"]
            description = serializer.validated_data["description"]
            user, created = listly_user.objects.get_or_create(user_name=userName)
            serializer.save(username=user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class single_task(generics.RetrieveAPIView):
    queryset = task.objects.all()
    serializer_class = UserTaskSerializer
    lookup_field = "pk"

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            return task.objects.get(pk=pk)
        except:
            raise serializers.ValidationError(
                "Task with this id does not exist. Please provide a valid task id."
            )


# @api_view(["POST"])
# def task_add(request) :
#     if request.method == "POST" :
#         serializers = UserTaskSerializer(data = request.data)
#         if serializers.is_valid() :
#             userName = serializers.validated_data["username"]
#             description = serializers.validated_data["description"]
#             user, created = listly_user.objects.get_or_create(user_name = userName)
#             task.objects.create(description = description, username = user)
#             return Response({"message" : "Task created successfully"}, status=201)

#         return Response(serializers.errors, status=400)

# @api_view(["POST"])
# def task_add(request) :
#     if request.method == "POST" :
#         serializer = UserTaskSerializer(data=request.data)
#         if serializer.is_valid():
#             userName = serializer.validated_data["username"]
#             description = serializer.validated_data["description"]
#             user, created = listly_user.objects.get_or_create(user_name=userName)
#             task.objects.create(description=description, username=user)
#             return Response({"message": "Task created successfully"}, status=201)

#         return Response(serializer.errors, status=400)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'step'
    max_page_size = 100

class task_list(generics.ListAPIView):
    # authentication_classes = [
    #     TokenAuth
    # ]
    # permission_classes = [TasksPermission]
    queryset = task.objects.all().order_by("-created_at")
    serializer_class = UserTaskSerializer
    pagination_class = StandardResultsSetPagination

class delete_task(generics.DestroyAPIView):
    queryset = task.objects.all()
    serializer_class = UserTaskSerializer

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound(detail="not Found these task")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({"msg": "sucess"})



@api_view(["GET"])
def UserLists(request):
    if request.method == "GET":
        users = listly_user.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# @api_view(["DELETE"])
# def delete_task(request, pk) :
#     if request.method == "DELETE" :
#         try :
#             task.objects.get(pk = pk).delete()
#             return Response("data is deleted", status=204)
#         except :
#             return Response("no data bsed on pk", status=404)


class edit_task_class(generics.UpdateAPIView):
    queryset = task.objects.all()
    serializer_class = UserTaskSerializer
    lookup_field = "pk"

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound(detail="not Found these task")

    def perform_update(self, serializer):
        username_str = serializer.validated_data.get("username", None)

        if username_str:
            user, created = listly_user.objects.get_or_create(user_name=username_str)
            serializer.save(username=user)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data.pop("created_at", None)
        response.data.pop("updated_at", None)
        return response
