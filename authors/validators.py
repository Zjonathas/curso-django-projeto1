from django import forms
from recipes.models import Recipe
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.string_test import is_positive_number

class AuthorRecipeFormValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_preparation_time()
        self.clean_servings()
        cleaned_data = self.data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self.errors['title'].append('Cannot be equal to description.')
            self.errors['description'].append('Cannot be equal to title.')

        if self.errors:
            raise self.ErrorClass(self.errors)


    def validation_simple_is_positive(self, field_name, message_error):
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append(message_error)

        return field_value

    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append('Must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        return self.validation_simple_is_positive(
            'preparation_time',
            'Must be a positive number')

    def clean_servings(self):
        return self.validation_simple_is_positive(
            'servings',
            'Must be a positive number')
