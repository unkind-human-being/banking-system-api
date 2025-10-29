from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from django.db import connection
from .models import Account, Transaction, Transfer
from .serializers import AccountSerializer, TransactionSerializer, TransferSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        transaction_obj = serializer.save()
        account_id = transaction_obj.account.id
        amount = transaction_obj.amount
        txn_type = transaction_obj.transaction_type

        try:
            with connection.cursor() as cursor:
                # 🟢 Begin a manual PostgreSQL transaction
                cursor.execute("BEGIN;")

                # Lock the account row to prevent race conditions
                cursor.execute(
                    "SELECT balance FROM accounts_account WHERE id = %s FOR UPDATE;",
                    [account_id],
                )
                balance = cursor.fetchone()[0]

                # Deposit or Withdraw logic
                if txn_type == 'deposit':
                    new_balance = balance + amount
                elif txn_type == 'withdraw':
                    if balance < amount:
                        raise Exception("Insufficient balance.")
                    new_balance = balance - amount
                else:
                    raise Exception("Invalid transaction type.")

                # Update balance
                cursor.execute(
                    "UPDATE accounts_account SET balance = %s WHERE id = %s;",
                    [new_balance, account_id],
                )

                # ✅ Commit only if all SQL succeeded
                cursor.execute("COMMIT;")

        except Exception as e:
            # 🔴 Rollback any changes if something fails
            with connection.cursor() as cursor:
                cursor.execute("ROLLBACK;")
            raise serializers.ValidationError(str(e))


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all().order_by('-timestamp')
    serializer_class = TransferSerializer

    def perform_create(self, serializer):
        transfer = serializer.save()
        from_id = transfer.from_account.id
        to_id = transfer.to_account.id
        amount = transfer.amount

        try:
            with connection.cursor() as cursor:
                cursor.execute("BEGIN;")

                # Lock both accounts
                cursor.execute(
                    "SELECT balance FROM accounts_account WHERE id = %s FOR UPDATE;",
                    [from_id],
                )
                from_balance = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT balance FROM accounts_account WHERE id = %s FOR UPDATE;",
                    [to_id],
                )
                to_balance = cursor.fetchone()[0]

                # Validation
                if from_balance < amount:
                    raise Exception("Insufficient funds for transfer.")

                new_from = from_balance - amount
                new_to = to_balance + amount

                # Update both
                cursor.execute(
                    "UPDATE accounts_account SET balance = %s WHERE id = %s;",
                    [new_from, from_id],
                )
                cursor.execute(
                    "UPDATE accounts_account SET balance = %s WHERE id = %s;",
                    [new_to, to_id],
                )

                cursor.execute("COMMIT;")

        except Exception as e:
            with connection.cursor() as cursor:
                cursor.execute("ROLLBACK;")
            raise serializers.ValidationError(str(e))
