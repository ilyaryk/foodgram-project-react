from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import MinValueValidator
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404

from .models import Favorite, Follow, User, Cart
from users.serializers import UserSerializer
from recipes.models import Recipe, Ingredient, Tag, AmountOfIngredients


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'color', 'slug')
        model = Tag


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Favorite


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""
    user = SlugRelatedField(slug_field='username',
                            read_only=True,
                            default=serializers.CurrentUserDefault())
    following = SlugRelatedField(slug_field='username',
                                 queryset=User.objects.all())

    def validate_following(self, data):
        if self.context['request'].user == data:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.')
        return data

    class Meta:
        fields = '__all__'
        model = Follow
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Вы уже подписаны!')
            ),
        )


class CartSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='buyer',
                            read_only=True,
                            default=serializers.CurrentUserDefault())
    item = SlugRelatedField(slug_field='item',
                            queryset=Recipe.objects.all())

    class Meta:
        fields = '__all__'
        model = Cart
        validators = (
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('user', 'following'),
                message=('Предмет уже в корзине)')
            ),
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'measurement_unit')
        model = Ingredient


class IngredientsCreateOrUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(MinValueValidator(1),)
    )

    class Meta:
        model = AmountOfIngredients
        fields = (
            'id',
            'amount',
        )

    def create(self):
        AmountOfIngredients.objects.get_or_create(
            amount=self.amount,
            ingredient=Ingredient.objects.get(id=self.id)
        )


class IngredientsReadOnlySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = AmountOfIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeCreateOrUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
 #   image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(MinValueValidator(1),)
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
           # 'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                'Для рецепта нужен хотя бы один тег!'
            )
        return tags

    def validate_cooking_time(self, cooking_time):
        if int(cooking_time) < 1:
            raise serializers.ValidationError(
                'Время приготовления меньше 1 минуты!'
            )
        return cooking_time

    def create_ingredients_amounts(self, ingredients, recipe):
        for ingredient in ingredients:
            print('____TUT____________')
            AmountOfIngredients.objects.get_or_create(
                ingredient=get_object_or_404(
                    Ingredient.objects.filter(id=ingredient['id'])
                ),
                amount=ingredient['amount'],
                recipe=recipe
            )


class RecipeReadOnlySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
 #   image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
   #         'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorite.objects.filter(user=user, recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Cart.objects.filter(user=user, item=recipe).exists()

    def get_ingredients(self, recipe):
        data = AmountOfIngredients.objects.filter(recipe=recipe)
        ingredients = []
        for i in data:
            data = IngredientsReadOnlySerializer(i).data
            ingredients.append(data)
        return ingredients