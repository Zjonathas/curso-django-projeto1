from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeAPIv2Test(RecipeMixin, test.APITestCase):
    def get_list_url(self):
        return self.client.get(reverse('recipes:recipes-api-list'))

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_list_url()
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_recipes = 7

        self.make_recipe_in_batch(wanted_number_recipes)

        response = self.get_list_url()

        qtd_of_loaded_recipes = len(response.data.get('results'))

        self.assertEqual(qtd_of_loaded_recipes, wanted_number_recipes)

    def test_recipe_api_lis_do_not_show_publish_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_publish = recipes[0]
        recipe_not_publish.is_publish = False
        recipe_not_publish.save()

        response = self.get_list_url()

        self.assertEqual(len(response.data.get('results')), 1)
