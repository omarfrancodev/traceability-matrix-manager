# En tu aplicación matrix/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Matrix
from project.models import Project

@receiver(post_save, sender=Project, dispatch_uid="status_new_signal_on_Project_post_save")
def create_matrix_for_project(sender, instance, created, **kwargs):
    if created:
        matrix = Matrix.objects.create(associatedProject=instance)
        instance.associatedMatrix = matrix
        instance.save()