from django.contrib.auth.decorators import login_required
from django.urls import path

from main.views import (
    RecordCreateView, RecordDeleteView, RecordDetailView, RecordUpdateView, RecordListView, SearchView,
)


urlpatterns = [
    path('', RecordListView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('record/<int:pk>/', RecordDetailView.as_view(), name='record_detail'),
    path('record/create/', login_required(RecordCreateView.as_view()), name='record_create'),
    path('record/<int:pk>/update/', login_required(RecordUpdateView.as_view()), name='record_update'),
    path('record/<int:pk>/delete/', login_required(RecordDeleteView.as_view()), name='record_delete'),
]
