import os
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm, LoginForm, AuthorRecipeForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from utils.pagination import make_pagination


PER_PAGE = int(os.environ.get('PER_PAGE', 9))


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')

        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
                  'form': form,
                  'form_action': reverse('authors:login_create'),
                  })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')
    return redirect('authors:dashboard')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))

    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboar_view(request):
    recipes = Recipe.objects.filter(
        is_publish=False,
        author=request.user,
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'authors/pages/dashboard.html', {
            'recipes': page_obj,
            'pages': pagination_range,
            }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit_view(request, id):
    recipe = Recipe.objects.filter(
        is_publish=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_publish = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso.')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'authors/pages/dashboard_recipe.html', {
            'form': form,
            }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_create_recipe_view(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe: Recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Salvo com sucesso!')
        return redirect(
            reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
        )

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form,
            'form_action': reverse('authors:dashboard_recipe_create')
        }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete_view(request, id):
    recipe = Recipe.objects.filter(
        is_publish=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404

    recipe.delete()
    messages.success(request, 'Delete successfully')
    return redirect(reverse('authors:dashboard'))
