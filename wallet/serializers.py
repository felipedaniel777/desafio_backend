from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']
        read_only_fields = ['user', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'timestamp']
