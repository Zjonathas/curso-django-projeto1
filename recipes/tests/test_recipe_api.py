from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeAPIv2Test(RecipeMixin, test.APITestCase):
    def get_list_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        return response

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

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # Create recipes
        recipes = self.make_recipe_in_batch(qtd=10)

        # Create categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # Change all recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # Change the first recipe to the not wanted category
        # As a result, this recipe should NOT show in the page
        recipes[0].category = category_not_wanted
        recipes[0].save()

        # Action: get recipes by category_id
        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.get_list_url(reverse_result=api_url)

        # We should onle see recipes from the wanted category
        self.assertEqual(len(response.data.get('results')), 9)

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.post(api_url, data={})
        self.assertEqual(response.status_code, 401)
