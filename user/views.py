from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import CustomUserSerializer, CustomListUserSerializer
from rest_framework.permissions import DjangoModelPermissions
from traceabilitymatrix.permissions import AdminPermission

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = CustomListUserSerializer
    permission_classes = [DjangoModelPermissions, AdminPermission]

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response(
                data={'message': 'Users retrieved successfully', 'usersData': response.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={'message': f'Error retrieving users: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [DjangoModelPermissions, AdminPermission]

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return Response(
                data={'message': 'User retrieved successfully', 'userData': response.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={'message': f'Error retrieving user: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
            except Exception as e:
                return Response(
                    data={'message': f'Error finding user: {str(e)}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                data={'message': 'User updated successfully', 'userData': serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={'message': f'Error updating user: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
            except Exception as e:
                return Response(
                    data={'message': f'Error finding user: {str(e)}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            self.perform_destroy(instance)
            return Response(
                data={'message': 'User deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                data={'message': f'Error deleting user: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )
