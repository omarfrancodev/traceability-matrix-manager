from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Record
import os
        
@receiver(post_delete, sender=Record)
def delete_record_file(sender, instance, **kwargs):
    if instance.locationResource:
        if os.path.isfile(instance.locationResource.path):
            os.remove(instance.locationResource.path)