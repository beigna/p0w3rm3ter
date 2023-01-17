from django.db import models


class Device(models.Model):
    key = models.CharField(
        max_length=100, unique=True,
        help_text='Llave identificadora del medidor'
    )
    name = models.CharField(max_length=100, help_text='Nombre del medidor')

    def __str__(self):
        return f'{self.key} - {self.name}'


class Metering(models.Model):
    device = models.ForeignKey('core.Device', on_delete=models.CASCADE)
    consumption = models.IntegerField(help_text='Consumo de la medición')
    timestamp = models.DateTimeField(help_text='Fecha de la medición')

    def __str__(self):
        return f'[{self.id}] {self.device}: {self.consumption}kW'
