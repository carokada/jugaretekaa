# Generated by Django 3.2.4 on 2021-07-03 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tienda', '0002_remove_categoria_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrito',
            name='lista_productos',
        ),
        migrations.AddField(
            model_name='carrito',
            name='lista_productos',
            field=models.ManyToManyField(blank=True, related_name='productos_carrito', to='Tienda.Producto'),
        ),
    ]
