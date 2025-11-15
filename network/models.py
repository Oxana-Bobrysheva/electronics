from django.db import models


class Contact(models.Model):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.email} ({self.country}, {self.city})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    # Hierarchy levels
    FACTORY = 0
    RETAIL_NETWORK = 1
    INDIVIDUAL_ENTREPRENEUR = 2

    LEVEL_CHOICES = [
        (FACTORY, 'Factory'),
        (RETAIL_NETWORK, 'Retail Network'),
        (INDIVIDUAL_ENTREPRENEUR, 'Individual Entrepreneur'),
    ]

    name = models.CharField(max_length=100)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def level(self):
        """Calculate hierarchy level automatically"""
        if self.supplier is None:
            return self.FACTORY

        if hasattr(self.supplier, 'level'):
            return self.supplier.level + 1
        return self.FACTORY

    def __str__(self):
        return self.name