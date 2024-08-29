from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contract(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="contracts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    fidelity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.user.username}"
