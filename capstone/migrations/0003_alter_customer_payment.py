# Generated by Django 3.2.7 on 2021-09-26 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0002_contact_customer_planseguro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='payment',
            field=models.FloatField(blank=True, max_length=10, null=True),
        ),
    ]
