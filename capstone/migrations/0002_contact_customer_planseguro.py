# Generated by Django 3.2.7 on 2021-09-26 00:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('phone', models.IntegerField(max_length=20)),
                ('email', models.TextField(blank=True, max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_customer', models.BooleanField(default=False)),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='creador', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlanSeguro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.TextField(max_length=50)),
                ('coverage', models.IntegerField(max_length=20)),
                ('deducible', models.IntegerField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timecustomer', models.DateTimeField(auto_now_add=True)),
                ('payment', models.FloatField(max_length=10, null=True)),
                ('age', models.IntegerField(blank=True, max_length=3, null=True)),
                ('contacto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info_contact', to='capstone.contact')),
                ('planes', models.ManyToManyField(blank=True, related_name='customers', to='capstone.PlanSeguro')),
            ],
        ),
    ]
