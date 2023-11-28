from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from matrix.models import Matrix
from matrix.serializers import CustomDetailMatrixSerializer, MatrixSerializer
from record.models import Record
from record.serializers import RecordSerializer

class MatrixListView(generics.ListAPIView):
    queryset = Matrix.objects.all()
    serializer_class = MatrixSerializer

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response(
                data={
                    "message": "Matrices retrieved successfully",
                    "matrixData": response.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": f"Error retrieving matrices: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MatrixDetailView(generics.RetrieveAPIView):
    queryset = Matrix.objects.all()
    serializer_class = CustomDetailMatrixSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return Response(
                data={
                    "message": "Matrix retrieved successfully",
                    "matrixData": response.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": f"Error retrieving matrix: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND,
            )
