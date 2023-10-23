# Generated by Django 4.2.6 on 2023-10-23 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveBigIntegerField(),
        ),
    ]