from django.db import models

# Create your models here.


class Client(models.Model):
    """
    Client
    """
    first_name = models.CharField(verbose_name='First Name', max_length=32, null=True, blank=True, default=None)
    second_name = models.CharField(verbose_name='Second Name', max_length=32, null=True, blank=True, default=None)
    phone = models.CharField(verbose_name='Phone', max_length=32, null=True, blank=True)
    age = models.SmallIntegerField(verbose_name='Age', null=True, blank=True, default=1)

    GENDER_CHOICES = (
        (1, 'male'), (2, 'female')
    )
    gender = models.SmallIntegerField(verbose_name='Gender', choices=GENDER_CHOICES, default=1)
    company = models.CharField(verbose_name='Company', max_length=32, null=True, blank=True)

    def __str__(self):
        return self.first_name


class Department(models.Model):
    title = models.CharField(verbose_name='Title', max_length=32)
