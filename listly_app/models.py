from django.db import models


class listly_user(models.Model):
    user_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user_name
    
    class Meta : 
        verbose_name = "user"
        verbose_name_plural = "users"        


class task(models.Model):
    description = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(
        listly_user, related_name="userTasks", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.description