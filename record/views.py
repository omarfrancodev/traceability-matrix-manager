from rest_framework import generics, status
from rest_framework.response import Response
from .models import Record
from .serializers import RecordSerializer
from rest_framework.permissions import DjangoModelPermissions
from traceabilitymatrix.permissions import AdminPermission, TeamMemberPermission, GuestPermission

class RecordListView(generics.CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [DjangoModelPermissions, (AdminPermission | TeamMemberPermission | GuestPermission)]

    def create(self, request, *args, **kwargs):
        try:
            self.check_permissions(request)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                data={'message': 'Record created successfully', 'recordData': serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            return Response(
                data={'message': f'Error creating record: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class RecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [DjangoModelPermissions, (AdminPermission | TeamMemberPermission | GuestPermission)]

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return Response(
                data={'message': 'Record retrieved successfully', 'recordData': response.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={'message': f'Error retrieving record: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
            except Exception as e:
                return Response(
                    data={'message': f'Error finding record: {str(e)}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                data={'message': 'Record updated successfully', 'recordData': serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={'message': f'Error updating record: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
            except Exception as e:
                return Response(
                    data={'message': f'Error finding record: {str(e)}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            self.perform_destroy(instance)
            return Response(
                data={'message': 'Record deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                data={'message': f'Error deleting record: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )
