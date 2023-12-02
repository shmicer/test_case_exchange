from rest_framework import serializers

from .models import Transaction


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['currency_from', 'currency_to', 'amount_from']


class TransactionViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'currency_from', 'currency_to', 'amount_from', 'amount_to', 'exchange_rate', 'timestamp']
        read_only_fields = ['amount_to', 'exchange_rate', 'timestamp']
