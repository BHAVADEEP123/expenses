from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.category+":"+str(self.amount)
    class Meta:
        ordering : ['-date']

class Category(models.Model):
    category = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.category
    class Meta:
        verbose_name_plural = 'Categories'