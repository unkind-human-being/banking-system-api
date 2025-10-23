from django.db import models
from django.db import models
from decimal import Decimal


class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    owner_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner_name} ({self.account_number})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]

    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.title()} - {self.amount} ({self.account.owner_name})"



class Transfer(models.Model):
    sender = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='sent_transfers')
    receiver = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.owner_name} ➜ {self.receiver.owner_name} : {self.amount}"

    def save(self, *args, **kwargs):
        if self.sender == self.receiver:
            raise ValueError("Cannot transfer to the same account.")
        if self.sender.balance < self.amount:
            raise ValueError("Insufficient balance.")
        # perform the transfer
        self.sender.balance -= self.amount
        self.receiver.balance += self.amount
        self.sender.save()
        self.receiver.save()
        super().save(*args, **kwargs)