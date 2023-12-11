from django.urls import path
from .views import EventRecordListView

urlpatterns = [
    path('', EventRecordListView.as_view(), name='event-record-list'),
]