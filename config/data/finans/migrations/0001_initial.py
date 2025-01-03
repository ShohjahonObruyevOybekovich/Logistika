# Generated by Django 5.1.4 on 2024-12-24 11:26

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0001_initial'),
        ('employee', '0001_initial'),
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('action', models.CharField(blank=True, choices=[('INCOME', 'INCOME'), ('OUTCOME', 'OUTCOME')], max_length=20, null=True)),
                ('amount_uzs', models.FloatField(blank=True, null=True)),
                ('amount_usd', models.FloatField(blank=True, null=True)),
                ('kind', models.CharField(blank=True, choices=[('OTHER', 'Boshqa'), ('FIX_CAR', 'Avtomobil tuzatish'), ('PAY_SALARY', 'Oylik berish'), ('FLIGHT', 'FLIGHT')], max_length=20, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.car')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.employee')),
                ('flight', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='flight.flight')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
