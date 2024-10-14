
# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Mesa(models.Model):
    numero = models.IntegerField(unique=True)  # Número da mesa
    capacidade = models.IntegerField()  # Capacidade da mesa

    def __str__(self):
        return f'Mesa {self.numero} (Capacidade: {self.capacidade})'


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relaciona a reserva com o cliente
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)  # Relaciona a reserva com a mesa
    data_reserva = models.DateField()
    hora_reserva = models.TimeField()
    num_pessoas = models.IntegerField()

    def __str__(self):
        return f'Reserva de {self.cliente} na {self.mesa} para {self.num_pessoas} pessoas'

    
