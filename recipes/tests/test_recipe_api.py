from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeAPIv2Test(RecipeMixin, test.APITestCase):
    def test_recipe_api_list_returns_status_code_200(self):
        url = reverse('recipes:recipes-api-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_recipes = 7

        self.make_recipe_in_batch(wanted_number_recipes)

        url = reverse('recipes:recipes-api-list')
        response = self.client.get(url)

        qtd_of_loaded_recipes = len(response.data.get('results'))

        self.assertEqual(qtd_of_loaded_recipes, wanted_number_recipes)
