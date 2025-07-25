# Generated by Django 5.2.3 on 2025-06-24 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0008_jetski'),
    ]

    operations = [
        migrations.AddField(
            model_name='jetski',
            name='fuel_capacity_gal',
            field=models.DecimalField(decimal_places=2, default=18.5, max_digits=5),
        ),
        migrations.AddField(
            model_name='jetski',
            name='has_audio',
            field=models.BooleanField(default=False, verbose_name='Premium Sound System'),
        ),
        migrations.AddField(
            model_name='jetski',
            name='has_brake_reverse',
            field=models.BooleanField(default=True, verbose_name='Brake & Reverse'),
        ),
        migrations.AddField(
            model_name='jetski',
            name='has_display',
            field=models.BooleanField(default=True, verbose_name='Touch Display'),
        ),
        migrations.AddField(
            model_name='jetski',
            name='horsepower',
            field=models.PositiveIntegerField(default=300),
        ),
        migrations.AddField(
            model_name='jetski',
            name='rider_capacity',
            field=models.PositiveIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='jetski',
            name='storage_capacity_gal',
            field=models.DecimalField(decimal_places=2, default=42.5, max_digits=5),
        ),
        migrations.AddField(
            model_name='jetski',
            name='top_speed_mph',
            field=models.PositiveIntegerField(default=65),
        ),
        migrations.AddField(
            model_name='jetski',
            name='weight_capacity_lb',
            field=models.PositiveIntegerField(default=600),
        ),
        migrations.AlterField(
            model_name='jetski',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='jetski',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='jetski_images/'),
        ),
    ]
