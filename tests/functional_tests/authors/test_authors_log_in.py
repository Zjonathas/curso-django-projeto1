from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from django.urls import reverse
import pytest


@pytest.mark.functional_test
class AuthorLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user',
            password=string_password)

        # User open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User see login form
        login_form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(
            login_form, 'Type your username')
        password_field = self.get_by_placeholder(
            login_form, 'Type your password')

        # User type your username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User send form
        login_form.submit()

        # User see the login message sucess and your name
        self.assertIn(
            f'You are logged in with {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # End test
