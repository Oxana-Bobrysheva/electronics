from django.db import models


class Contact(models.Model):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.email} ({self.country}, {self.city})"