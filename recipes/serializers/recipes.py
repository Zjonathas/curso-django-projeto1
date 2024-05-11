from rest_framework import serializers
from django.contrib.auth.models import User
from tag.models import Tag
from recipes.models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', ]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description',
                  'is_publish', 'preparation_time',
                  'preparation_time_unit', 'category',
                  'author', 'tags', 'public', 'preparation',
                  'tag_objects', 'tag_links']
    public = serializers.BooleanField(source='is_publish', read_only=True)
    preparation = serializers.SerializerMethodField(
        method_name='get_preparation', read_only=True)
    category = serializers.StringRelatedField()
    tag_objects = TagSerializer(
        many=True, source='tags', read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipe_api_v2_tag',
        read_only=True
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
