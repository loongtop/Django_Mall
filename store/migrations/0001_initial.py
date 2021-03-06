# Generated by Django 4.0.4 on 2022-04-19 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='First Name')),
                ('second_name', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='Second Name')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone')),
                ('age', models.SmallIntegerField(blank=True, default=1, null=True, verbose_name='Age')),
                ('gender', models.SmallIntegerField(choices=[(1, 'male'), (2, 'female')], default=1, verbose_name='Gender')),
                ('company', models.CharField(blank=True, max_length=32, null=True, verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Title')),
            ],
        ),
    ]
