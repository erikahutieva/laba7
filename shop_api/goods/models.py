from django.db import models
from uuid import uuid4

class Good(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.IntegerField()

    def __str__(self): #для нормального отображения
        return self.name

class Token(models.Model):
    key = models.CharField(max_length=36, unique=True, default=uuid4)#случайная уникльная строка из 36 символов
    
    def __str__(self):
        return self.key
