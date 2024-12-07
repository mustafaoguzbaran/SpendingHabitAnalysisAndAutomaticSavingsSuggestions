from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"

