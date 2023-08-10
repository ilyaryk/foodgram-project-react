# Generated by Django 3.2 on 2023-08-09 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_remove_recipe_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.AmountOfIngredients', to='recipes.Ingredient', verbose_name='Список ингредиентов'),
        ),
    ]