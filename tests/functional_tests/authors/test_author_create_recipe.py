from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from django.urls import reverse
import pytest


@pytest.mark.functional_test
class AuthorCreateRecipeTest(AuthorsBaseTest):
    def fill_dummy_form_recipe(self):
        self.create_form = self.browser.find_element(
            By.CLASS_NAME,
            'main-form'
        )

        title_recipe = self.get_by_id(self.create_form, 'id_title')
        description_recipe = self.get_by_id(self.create_form, 'id_description')
        preparation_time_recipe = self.get_by_id(
            self.create_form,
            'id_preparation_time')
        servings_recipe = self.get_by_id(self.create_form, 'id_servings')
        preparations_steps_recipe = self.get_by_id(
            self.create_form,
            'id_preparation_steps')

        title_recipe.send_keys('TESTE TESTE')
        description_recipe.send_keys('TESTE TESTE - description')
        preparation_time_recipe.send_keys('21')
        servings_recipe.send_keys('21')
        preparations_steps_recipe.send_keys('TESTE TESTE TESTE')

    def test_create_recipe_is_working(self):
        self.longin()

        # User goes to the recipe creation page
        self.browser.get(
            self.live_server_url +
            reverse('authors:dashboard_recipe_create'))

        # User fills in the form
        self.fill_dummy_form_recipe()

        # User send recipe
        self.create_form.submit()

        # Test
        self.assertIn(
            'Sua receita foi salva com sucesso.',
            self.browser.find_element(
                By.TAG_NAME,
                'body'
            ).text
        )

    def test_recipe_has_the_same_title_as_the_description(self):
        # User logs in
        self.longin()

        # User goes to the recipe creation page
        self.browser.get(
            self.live_server_url +
            reverse('authors:dashboard_recipe_create'))
        create_form = self.browser.find_element(
            By.CLASS_NAME,
            'main-form'
        )

        # User fills in the form
        self.fill_dummy_form_recipe()

        title_recipe = self.get_by_id(create_form, 'id_title')
        description_recipe = self.get_by_id(create_form, 'id_description')

        title_recipe.clear()
        description_recipe.clear()
        title_recipe.send_keys('TESTE TESTE')
        description_recipe.send_keys('TESTE TESTE')

        create_form.submit()

        self.assertIn(
            'Cannot be equal to description.',
            self.browser.find_element(
                By.TAG_NAME,
                'body'
            ).text
        )

        self.assertIn(
            'Cannot be equal to title.',
            self.browser.find_element(
                By.TAG_NAME,
                'body'
            ).text
        )
