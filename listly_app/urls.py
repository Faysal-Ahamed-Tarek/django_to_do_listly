from django.urls import include, path
from .views import completed_task, listly_user_views, task_add, task_list, UserLists, single_task, delete_task, edit_task_class, delete_single_task, edit_task, listly, mark_as_complete, to_do_app, user_lists
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", to_do_app, name="welcome"),
    path("user_tasks/", user_lists, name="user_lists"),
    path("active_task/", listly, name="active_task"),
    path("listly_user/", listly_user_views, name="listly_user"),
    path("completed_task/", completed_task, name="completed_task"),
    path("delete_single_task/<int:pk>", delete_single_task, name="delete_single_task"),
    path("completed_task/<int:pk>/", mark_as_complete, name="mark_as_complete"),
    path("edit_task/<int:pk>", edit_task, name = "edit_task"),
    path("api/", include("listly.router"), name="api"),
    # api
    path("tasks/add", task_add.as_view()),
    path("tasks/", task_list.as_view()),
    path("tasks/<int:pk>", single_task.as_view()),
    path("delete/<int:pk>", delete_task.as_view()),
    path("edit/<int:pk>", edit_task_class.as_view()),
    path("users/", UserLists)
    # #token auth
    # path("auth", obtain_auth_token)
]