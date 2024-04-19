from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.string import is_positive_number

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover', 'category'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pessoas', 'Pessoas'),
                    ('Pedaços', 'Pedaços'),
                    ('Pratos', 'Pratos'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description.')
            self._my_errors['description'].append('Cannot be equal to title.')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def validation_simple_is_positive(self, field_name, message_error):
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append(message_error)

        return field_value

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        return self.validation_simple_is_positive(
            'preparation_time',
            'Must be a positive number')

    def clean_servings(self):
        return self.validation_simple_is_positive(
            'servings',
            'Must be a positive number')
