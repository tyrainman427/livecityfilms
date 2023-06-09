# Generated by Django 4.2 on 2023-04-16 14:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70, verbose_name='Product Name')),
                ('description', models.TextField(max_length=800, verbose_name='Description')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(100000)], verbose_name='Price')),
            ],
        ),
    ]
