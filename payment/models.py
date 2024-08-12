from django.db import models

# Create your models here.



class Purchase(models.Model):
    preference_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    input_name = models.CharField(max_length=255, null=True, blank=True)
    input_email = models.EmailField(null=True, blank=True)
    input_cel_phone = models.CharField(max_length=50, null=True, blank=True)
    input_msg = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cardholder_email = models.EmailField(null=True, blank=True)
    cardholder_name = models.CharField(max_length=255, null=True, blank=True)
    count_persons = models.IntegerField(null=True, blank=True)
    style_dessert = models.CharField(max_length=255, null=True, blank=True)
    savor_dessert = models.CharField(max_length=255, null=True, blank=True)
    filling = models.CharField(max_length=255, null=True, blank=True)
    dessert = models.CharField(max_length=255, null=True, blank=True)
    color_of_dessert = models.CharField(max_length=255, null=True, blank=True)
    color_of_border_dessert = models.CharField(max_length=255, null=True, blank=True)
    image_example_dessert = models.URLField(null=True, blank=True)
    date_collect_dessert = models.CharField(max_length=255, null=True, blank=True)
    hour_collect_dessert = models.TimeField(null=True, blank=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Purchase {self.id} - {self.preference_id}"