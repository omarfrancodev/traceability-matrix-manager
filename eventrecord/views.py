from rest_framework import generics
from django.utils import timezone
from .models import EventRecord
from .serializers import EventRecordSerializer
from rest_framework.permissions import DjangoModelPermissions
from traceabilitymatrix.permissions import AdminPermission, TeamMemberPermission, GuestPermission

class EventRecordListView(generics.ListCreateAPIView):
    queryset = EventRecord.objects.filter(clientLocalTimestamp__gte=timezone.now() - timezone.timedelta(days=3)).order_by('-serverTimestamp')
    serializer_class = EventRecordSerializer
    permission_classes = [DjangoModelPermissions, (AdminPermission | TeamMemberPermission | GuestPermission)]
