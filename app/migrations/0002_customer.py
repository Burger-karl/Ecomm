# Generated by Django 4.2.2 on 2023-06-27 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('mobile', models.IntegerField(default=0)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(choices=[('Abia', 'Abia'), ('Anambra', 'Anambra'), ('Adamawa', 'Adamawa'), ('Abuja', 'Abuja'), ('Akwa-ibom', 'Akwa-ibom'), ('Benue', 'Benue'), ('Bauchi', 'Bauchi'), ('Calabar', 'Calabar'), ('Delta', 'Delta'), ('Edo', 'Edo'), ('Enugu', 'Enugu'), ('Ebonyi', 'Ebonyi'), ('Imo', 'Imo'), ('Lagos', 'Lagos'), ('Oyo', 'Oyo'), ('Jos', 'Jos'), ('Ogun', 'Ogun'), ('Osun', 'Osun'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Rivers', 'Rivers'), ('Borno', 'Borno'), ('Gombe', 'Gombe'), ('Taraba', 'Taraba'), ('Ondo', 'Ondo')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
