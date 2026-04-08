from rest_framework import permissions


class TasksPermission(permissions.DjangoModelPermissions) : 
    def has_permission(self, request, view) : 
        if request.user.is_staff :
            if request.user.has_perm("listly_app.view_task") :
                return True
        return False