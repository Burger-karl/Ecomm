# Generated by Django 3.2 on 2024-08-22 15:28

from django.db import migrations, models
import django.utils.timezone

def populate_emails(apps, schema_editor):
    Payment = apps.get_model('app', 'Payment')
    for payment in Payment.objects.all():
        payment.email = payment.user.email
        payment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20240822_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='email',
            field=models.EmailField(max_length=254, default=''),
        ),
        migrations.AddField(
            model_name='payment',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RunPython(populate_emails),
    ]
