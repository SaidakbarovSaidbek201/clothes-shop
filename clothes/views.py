from django.shortcuts import render
from .models import Category, Clothes
# Create your views here.
def clothes_page(request):
    category = Category.objects.all()
    foods = Clothes.objects.all()
    context = {
        'kategoriya' : category,
        'kiyim' : foods
    }
    return render(request, template_name='index.html', context=context)