from django.db.models.signals import post_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Record
from user.models import User
import os
        
@receiver(post_delete, sender=Record)
def delete_record_file(sender, instance, **kwargs):
    if instance.locationResource:
        if os.path.isfile(instance.locationResource.path):
            os.remove(instance.locationResource.path)

@receiver(pre_save, sender=Record)
def validate_key_relationship(sender, instance, **kwargs):
    if instance.keyRelationship == "NA":
        return

    existingRecords = Record.objects.filter(
        associatedProject=instance.associatedProject
    ).exclude(pk=instance.pk)
    matchingCustomProjectIds = existingRecords.values_list('projectRecordId', flat=True)
    
    if instance.keyRelationship not in matchingCustomProjectIds:
        raise ValidationError('El valor de keyRelationship debe ser igual a uno de los projectRecordId existentes o "NA"')