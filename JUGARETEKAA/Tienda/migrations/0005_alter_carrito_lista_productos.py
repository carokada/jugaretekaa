# Generated by Django 3.2.4 on 2021-07-04 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tienda', '0004_alter_carrito_lista_productos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='lista_productos',
            field=models.ManyToManyField(blank=True, related_name='productos_carrito', to='Tienda.Producto'),
        ),
    ]