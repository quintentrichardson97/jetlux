# Generated by Django 5.2.3 on 2025-06-23 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_rental_jet_ski_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='skibuddy',
            name='user_picture',
            field=models.ImageField(default='No Picture Yet', upload_to=''),
        ),
    ]
