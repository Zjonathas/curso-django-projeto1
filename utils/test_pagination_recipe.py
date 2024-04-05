from django.test import TestCase
from django.urls import reverse
import pytest
from recipes.tests.test_recipe_base import RecipeTesteBase


class PaginationTestView(TestCase):
    @pytest.mark.django_db
    def test_pagination_view(self):
        # Create 10 recipes
        for i in range(10):
            RecipeTesteBase().make_recipe(
                author_data={'username': f'test{i}'},
                title=f'Recipe {i}',
                slug=f'recipe-{i}',
                is_publish=True,
            )

        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertEqual(len(response.context['recipes']), 9)
