from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse


class RecipeAPIv2Test(RecipeMixin, test.APITestCase):
    def test_recipe_api_list_returns_status_code_200(self):
        url = reverse('recipes:recipes-api-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
