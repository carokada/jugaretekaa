# Generated by Django 3.2.4 on 2021-07-07 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tienda', '0002_auto_20210707_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='total_carrito',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]