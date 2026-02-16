from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Prefetch
from listly_app.forms import listly_user_form, newTask
from listly_app.models import listly_user, task


# Create your views here.
def to_do_app(request):
    return render(request, "welcome.html", {"form" : listly_user_form()})


def user_lists(request) : 
    data = listly_user.objects.prefetch_related(
        Prefetch('userTasks', queryset=task.objects.filter(completed=False))
    ).all()
    return render(request, "user_lists.html", {"data": data})


def listly_user_views(request) : 
    if request.method == "POST" : 
        form = listly_user_form(request.POST)
        if form.is_valid() : 
            listly_user.objects.get_or_create(user_name = form.cleaned_data["username"])
            request.session["user_name"] = form.cleaned_data["username"]
    return redirect("active_task")


def listly(request) :
    userName = listly_user.objects.get(user_name = request.session["user_name"])
    if request.method == "POST" : 
        form = newTask(request.POST)
        if form.is_valid() : 
            description = form.cleaned_data["description"]
            if task.objects.filter(description=description, completed=False, username = userName).exists():
                messages.warning(request, "⚠️ Task already exists. Please enter a unique task.")
                return redirect("active_task")
            task.objects.create(description=description, username = userName)
            messages.success(request, "✅ Task added successfully!")
            return redirect("active_task")
        else :
            messages.error(request, "❌ Invalid input. Please try again.")
            return redirect("active_task")
        
    data = task.objects.filter(completed = False, username = userName).order_by("-created_at")
    return render(request, "listly.html", {"data" : data, "addTask" : newTask(), "userName" : userName})


def completed_task(request) : 
    userName = listly_user.objects.get(user_name = request.session["user_name"])
    data = task.objects.filter(completed = True, username = userName).order_by("-created_at")
    return render(request, "completed.html", {"data" : data, "addTask" : newTask()})


def mark_as_complete(request, pk) : 
    data = task.objects.get(pk = pk)
    data.completed = True
    data.save()
    messages.success(request, "✅ Task completed!")
    return redirect("active_task")


def delete_single_task(request, pk) : 
    data = task.objects.get(pk = pk)
    data.delete()
    messages.success(request, "✅ Task deleted successfully!")
    return redirect("completed_task")


def edit_task(request, pk) : 
    userName = listly_user.objects.get(user_name = request.session["user_name"])
    if request.method == "POST":
        form = newTask(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            obj = task.objects.get(pk=pk)
            if obj.description == description : 
                messages.warning(request, "⚠️ didnt change anything")
                return redirect("active_task")
            obj.description = description
            obj.save()
            messages.success(request, "✅ Task updated successfully!")
            return redirect("active_task")
        else:
            messages.error(request, "❌ Invalid input. Please try again.")
            return redirect("active_task")

    data = task.objects.filter(completed = False, username = userName).order_by("-created_at")
    edited_data = task.objects.get(pk = pk)
    form = newTask(initial={"description": edited_data.description})
    return render(request, "listly.html", {"data" : data, "addTask" : form, "edit_task" : edited_data, "userName" : userName})