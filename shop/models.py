from django.db import models

# Create your models here.


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='Department', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    UserInfo
    """
    name = models.CharField(verbose_name='Name', max_length=32)

    gender_choices = (
        (1, 'mail'),
        (2, 'female'),
    )
    gender = models.IntegerField(verbose_name='Gender', choices=gender_choices, default=1)

    classes_choice = (
        (11, 'full stack Phase 1'),
        (12, 'full stack Phase 2'),
        (11, 'full stack Phase 3'),
    )
    classes = models.IntegerField(verbose_name='Class', choices=classes_choice, default=11)

    age = models.CharField(verbose_name='Age', max_length=32)
    email = models.CharField(verbose_name='Email', max_length=32)
    # depart = models.ManyToManyField(verbose_name='Department', to='Department')
    depart = models.ForeignKey(verbose_name='Department', to='Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Deploy(models.Model):
    title = models.CharField(verbose_name='Title', max_length=32)
    status_choices = (
        (1, 'on line'),
        (2, 'off line'),
    )
    status = models.IntegerField(verbose_name='Status', choices=status_choices)
