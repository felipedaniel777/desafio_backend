from decimal import Decimal
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    criar e listar usuários.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Qualquer pessoa pode criar um usuário

class WalletViewSet(viewsets.ModelViewSet):
    """
    consultar e adicionar saldo à carteira
    """
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)  

    serializer_class = WalletSerializer  

    @action(detail=False, methods=['get'])
    def saldo(self, request):
        """
        Retorna o saldo da carteira do usuário autenticado
        """
        wallet = request.user.wallet
        return Response({'saldo': wallet.balance})

    @action(detail=False, methods=['post'])
    def adicionar_saldo(self, request):
        """
        Adiciona saldo à carteira do usuário autenticado
        """
        wallet = request.user.wallet
        valor = request.data.get('valor')

        if not valor or float(valor) <= 0:
            return Response({'erro': 'O valor precisa ser maior que zero'}, status=400)

        wallet.balance += Decimal(valor)
        wallet.save()
        return Response({'mensagem': 'Saldo adicionado com sucesso', 'saldo_atual': wallet.balance})



class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para criar e listar transferências.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        """
        Cria uma transferência entre usuários.
        """
        remetente = request.user.wallet  
        destinatario_id = request.data.get('destinatario')
        valor = request.data.get('valor')

        if not destinatario_id or not valor:
            return Response({'erro': 'Destinatário e valor são obrigatórios'}, status=400)

        try:
            destinatario = Wallet.objects.get(user_id=destinatario_id)
        except Wallet.DoesNotExist:
            return Response({'erro': 'Destinatário não encontrado'}, status=404)

        if remetente.balance < float(valor):
            return Response({'erro': 'Saldo insuficiente'}, status=400)

        remetente.balance -= Decimal(valor)
        destinatario.balance += Decimal(valor)
        remetente.save()
        destinatario.save()

        transaction = Transaction.objects.create(
            sender=remetente.user,  
            receiver=destinatario.user, 
            amount=Decimal(valor) 
        )

        return Response(TransactionSerializer(transaction).data, status=201)