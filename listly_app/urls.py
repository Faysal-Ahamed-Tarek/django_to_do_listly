from django.urls import path

from .views import all_tasks_api, completed_task,listly_user_views, delete_single_task, edit_task, listly, mark_as_complete, to_do_app, user_lists



urlpatterns = [
    path("", to_do_app, name="welcome"),
    path("user_tasks/", user_lists, name="user_lists"),
    path("active_task/", listly, name="active_task"),
    path("listly_user/", listly_user_views, name="listly_user"),
    path("completed_task/", completed_task, name="completed_task"),
    path("delete_single_task/<int:pk>", delete_single_task, name="delete_single_task"),
    path("completed_task/<int:pk>/", mark_as_complete, name="mark_as_complete"),
    path("edit_task/<int:pk>", edit_task, name = "edit_task"),
    # api
    path("tasks/", all_tasks_api)
]