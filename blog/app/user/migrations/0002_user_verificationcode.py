# Generated by Django 5.0.1 on 2024-02-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verificationcode',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
