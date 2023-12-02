from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.models import Transaction
from api.serializers import (TransactionCreateSerializer,
                             TransactionViewSerializer)
from api.services import convert


@extend_schema(
    summary='Create a transaction',
)
class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = serializer.validated_data

        from_currency = data['currency_from'].upper()
        to_currency = data['currency_to'].upper()
        exchange_rate = convert(from_currency, to_currency)
        serializer.save(user=self.request.user, exchange_rate=exchange_rate)


@extend_schema(
    summary='List of current user transactions',
)
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

@extend_schema(
    summary='Retrieve, update and delete transaction',
)
class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
