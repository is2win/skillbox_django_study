# Generated by Django 4.1.7 on 2023-04-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0002_products_created_at_products_discount_products_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
