from django.db import models


class ContactModel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    message = models.TextField(max_length=1500)