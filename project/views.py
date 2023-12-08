from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer, DetailProjectSerializer, DetailUsersProjectSerializer
from rest_framework.permissions import DjangoModelPermissions
from traceabilitymatrix.permissions import AdminPermission, TeamMemberPermission, GuestPermission

class ProjectListCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [DjangoModelPermissions, (AdminPermission | TeamMemberPermission | GuestPermission)]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response(
                data={
                    "message": "Project created successfully",
                    "projectData": response.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                data={"message": f"Error creating project: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = DetailProjectSerializer
    permission_classes = [DjangoModelPermissions, (AdminPermission | TeamMemberPermission | GuestPermission)]

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return Response(
                data={
                    "message": "Project retrieved successfully",
                    "projectData": response.data,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionDenied:
            return Response(
                data={"message": "You do not have permission to perform this action. You can not access to this project."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                data={"message": f"Error retrieving project: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def update(self, request, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
            except Exception as e:
                return Response(
                    data={'message': f'Error finding project: {str(e)}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                data={
                    "message": "Project updated successfully",
                    "projectData": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": f"Error updating project: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
            except Exception as e:
                return Response(
                    data={'message': f'Error finding project: {str(e)}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            self.perform_destroy(instance)
            return Response(
                data={"message": "Project deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                data={"message": f"Error deleting project: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class ProjectUsersView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = DetailUsersProjectSerializer
    permission_classes = [DjangoModelPermissions, (AdminPermission | TeamMemberPermission | GuestPermission)]

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return Response(
                data={
                    "message": "Project users retrieved successfully",
                    "projectData": response.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": f"Error retrieving project users: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND,
            )