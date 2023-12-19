from django.shortcuts import render



def home(request):
    return render(request, 'pages/home.html', context={
        'name' : 'Jonathas Emanuel'
    })

def recipe(request, id):
    return render(request, 'pages/home.html', context={
        'name' : 'Jonathas Emanuel'
    })