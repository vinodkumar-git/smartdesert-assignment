# Generated by Django 3.2 on 2021-04-14 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='actual_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
