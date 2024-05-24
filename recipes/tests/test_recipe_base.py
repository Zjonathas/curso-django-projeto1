from django.test import TestCase
from recipes.models import Category, Recipe, User, Tag


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
            self,
            first_name='teste',
            last_name='teste',
            username='teste',
            password='teste',
            email='teste',):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,)

    def make_recipe(
            self,
            category_data=None,
            author_data=None,
            title='Recipe Title',
            description='Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe preparations steps',
            preparation_steps_html=False,
            is_publish=True,
    ):
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_html=preparation_steps_html,
            is_publish=is_publish,
        )

    def make_recipe_in_batch(self, qtd=10):
        """
        Make multiple recipes

        :param qtd: int

        qtd = quantity
        """
        recipes = []
        for i in range(qtd):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'},
                }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes

    def make_tag(self,):
        tag = Tag.objects.create(name='Tag')
        return tag


class RecipeTesteBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
