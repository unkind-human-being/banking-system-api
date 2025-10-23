from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer
from .models import Transaction
from .serializers import TransactionSerializer
from .models import Transfer
from .serializers import TransferSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        transaction = serializer.save()
        account = transaction.account
        if transaction.transaction_type == 'deposit':
            account.balance += transaction.amount
        elif transaction.transaction_type == 'withdraw':
            if account.balance >= transaction.amount:
                account.balance -= transaction.amount
            else:
                raise serializers.ValidationError("Insufficient balance.")
        account.save()


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all().order_by('-timestamp')
    serializer_class = TransferSerializer