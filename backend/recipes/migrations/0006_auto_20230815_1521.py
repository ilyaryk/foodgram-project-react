# Generated by Django 3.2 on 2023-08-15 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_recipe_image'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('user', 'item'), name='unique_cart'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='unique_follow'),
        ),
        migrations.AlterModelTable(
            name='cart',
            table='api_cart',
        ),
        migrations.AlterModelTable(
            name='follow',
            table='api_follow',
        ),
    ]