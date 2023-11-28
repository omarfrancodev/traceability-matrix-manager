from django.urls import path
from .views import RecordListView, RecordDetailView

urlpatterns = [
    path('', RecordListView.as_view(), name='record-list'),
    path('<int:pk>', RecordDetailView.as_view(), name='record-detail'),
]