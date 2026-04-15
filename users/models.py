from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GENDER_CHOICES = [('M','Male'),('F','Female'),('O','Other')]
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    id_type = models.CharField(max_length=50, blank=True, help_text="Aadhaar/PAN/Passport")
    id_number = models.CharField(max_length=50, blank=True)
    irctc_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.irctc_id and self.pk:
            self.irctc_id = f"IRCTC{self.pk:07d}"
        super().save(*args, **kwargs)
