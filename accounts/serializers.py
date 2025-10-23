from rest_framework import serializers
from .models import Account
from .models import Transaction
from .models import Transfer

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'