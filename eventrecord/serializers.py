from rest_framework import serializers
from eventrecord.models import EventRecord
from django.contrib.auth import get_user_model
from django_currentuser.middleware import get_current_authenticated_user

User = get_user_model()


class EventRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRecord
        fields = [
            "id",
            "actionType",
            "userFullNameExec",
            "userRoleExec",
            "modelAffected",
            "data",
            "serverTimestamp",
            "clientLocalTimestamp",
        ]

    def create(self, validated_data):
        current_user = get_current_authenticated_user()
        eventRecord = EventRecord.objects.create(
            userFullNameExec=current_user.fullName,
            userRoleExec=current_user.role,
            modelAffected=User.__name__,
            **validated_data
        )

        return eventRecord
