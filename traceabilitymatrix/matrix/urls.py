from django.urls import path
from .views import MatrixListView, MatrixDetailView

urlpatterns = [
    path('', MatrixListView.as_view(), name='matrix-list'),
    path('/<int:pk>/', MatrixDetailView.as_view(), name='matrix-detail'),
]