# Generated by Django 4.0.10 on 2023-08-23 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('fuel_type', models.CharField(choices=[('Gasoline', 'Gasoline'), ('Diesel', 'Diesel')], max_length=20)),
                ('num_of_seats', models.IntegerField()),
                ('fare_price_per_km', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Customer', 'Customer'), ('Driver', 'Driver')], default='Customer', max_length=20)),
                ('contact_number', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RideRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=100)),
                ('dropoff_location', models.CharField(max_length=100)),
                ('pickup_time', models.DateTimeField()),
                ('dropoff_time', models.DateTimeField()),
                ('ride_authorized', models.BooleanField(default=False)),
                ('ride_completed', models.BooleanField(default=False)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ride_request_car', to='rentals.car')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ride_request_customer', to='rentals.profile')),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ride_request_driver', to='rentals.profile')),
            ],
        ),
    ]
