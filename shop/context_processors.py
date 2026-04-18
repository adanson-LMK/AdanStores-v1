from .models import Category
from .cart import Cart

def categories_processor(request):
    return {
        'all_categories': Category.objects.all()
    }

def cart_processor(request):
    return {
        'cart': Cart(request)
    }
