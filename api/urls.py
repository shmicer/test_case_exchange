from django.urls import path
from .views import TransactionCreateView, TransactionDetail, TransactionListView

urlpatterns = [
    path('create_transaction/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/', TransactionListView.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>', TransactionDetail.as_view(), name='transaction-detail'),
]