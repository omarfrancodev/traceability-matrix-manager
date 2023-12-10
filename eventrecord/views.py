from rest_framework.response import Response
from rest_framework import generics, status
from django.utils import timezone
from .models import EventRecord
from .serializers import EventRecordSerializer
from rest_framework.permissions import DjangoModelPermissions
from custompermissions.permissions import AdminPermission, TeamMemberPermission, GuestPermission

class EventRecordListView(generics.ListCreateAPIView):
    queryset = EventRecord.objects.filter(clientLocalTimestamp__gte=timezone.now() - timezone.timedelta(days=3)).order_by('-serverTimestamp')
    serializer_class = EventRecordSerializer
    permission_classes = [DjangoModelPermissions, (AdminPermission | TeamMemberPermission | GuestPermission)]
    
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response(
                data={'message': 'Event Records retrieved successfully', 'data': response.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={'message': f'Error retrieving users: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )