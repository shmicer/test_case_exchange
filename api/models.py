from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_from = models.CharField(max_length=3)
    currency_to = models.CharField(max_length=3)
    amount_from = models.DecimalField(max_digits=15, decimal_places=2)
    amount_to = models.DecimalField(max_digits=15, decimal_places=2)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=5)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_from} {self.currency_from} to {self.amount_to} {self.currency_to}"

    def save(self, *args, **kwargs):
        self.amount_to = self.amount_from * Decimal(str(self.exchange_rate))
        super().save(*args, **kwargs)

