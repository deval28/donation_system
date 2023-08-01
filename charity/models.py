from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)
    one_time_password = models.IntegerField(verbose_name="One Time Password", null=True, blank=True)

    def __str__(self):
        return f'{self.username} - {self.phone_number} - {self.is_verified}'


class Charity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.description}'


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Donor")
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, verbose_name="Receiver")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('COMPLETED', 'Completed'),
            ('FAILED', 'Failed'),
        ],
        default='PENDING'
    )

    def __str__(self):
        return f'{self.user.username} - {self.charity.name} - {self.amount} - {self.payment_status}'
