from django.db.models.signals import post_delete, pre_delete, pre_save, post_save
from django.dispatch import receiver
from listly_app.models import task


@receiver(pre_save, sender=task)
def check_duplicate_task(sender, instance, **kwargs):
    print("pre save signal triggered for task:", instance.description)


@receiver(post_save, sender=task)
def check_post_save(sender, instance, created, **kwargs):
    print("post save signal triggered for task:", instance.description)


@receiver(pre_delete, sender = task) 
def check_pre_delete(sender, instance, **kwargs) : 
    print("pre delete signal triggered for task:", instance.description)


@receiver(post_delete, sender = task)
def check_post_delete(sender, instance, **kwargs) : 
    print("post delete signal triggered for task:", instance.description)