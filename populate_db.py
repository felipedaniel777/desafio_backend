import os
import sys
import django
import random
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "desafio_backend.settings")
django.setup()  

from django.contrib.auth.models import User
from wallet.models import Wallet, Transaction  

def criar_usuarios():
    usuarios = [
        {"username": "alice", "password": "senha123"},
        {"username": "bob", "password": "senha123"},
        {"username": "carol", "password": "senha123"},
    ]
    for user_data in usuarios:
        if not User.objects.filter(username=user_data["username"]).exists():
            user = User.objects.create_user(
                username=user_data["username"],
                password=user_data["password"]
            )
            print(f"Usuário criado: {user.username}")

def criar_carteiras():
    users = User.objects.all()
    for user in users:
        if not Wallet.objects.filter(user=user).exists():
            Wallet.objects.create(
            user=user,
            balance=Decimal(random.uniform(500, 2000))
        )

            print(f"Carteira criada para {user.username}")

def criar_transferencias():
    wallets = list(Wallet.objects.all())
    for _ in range(5):
        remetente, destinatario = random.sample(wallets, 2)
        valor = Decimal(random.uniform(50, 300))
        if remetente.balance >= valor:
            Transaction.objects.create(
                sender=remetente.user,
                receiver=destinatario.user,
                amount=valor
            )
            remetente.balance -= valor
            destinatario.balance += valor
            remetente.save()
            destinatario.save()
            print(f"Transferência de {remetente.user.username} para {destinatario.user.username} no valor de {valor}")

def popular_banco():
    print("Populando banco de dados...")
    criar_usuarios()
    criar_carteiras()
    criar_transferencias()
    print("Banco de dados populado com sucesso!")

if __name__ == "__main__":
    popular_banco()
