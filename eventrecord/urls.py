from django.urls import path
from .views import EventRecordListView, EventRecordDetailView

urlpatterns = [
    path('', EventRecordListView.as_view(), name='event-record-list'),
    path('<int:pk>', EventRecordDetailView.as_view(), name='event-record-detail'),
]