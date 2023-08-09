# Generated by Django 3.2 on 2023-08-08 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20230808_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountofingredients',
            name='ingredient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.ingredient', verbose_name='Список ингредиентов'),
            preserve_default=False,
        ),
    ]
