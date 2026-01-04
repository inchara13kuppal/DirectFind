from django.shortcuts import render, get_object_or_404
from .models import Product
from .engine import get_recommendations
import random

def home(request):
    return render(request, 'recommender/search.html')

def search(request):
    query = request.GET.get('query')
    best_match = None
    recommendations = []
    message = None
    is_fallback = False
    
    if query:
        best_match = Product.objects.filter(product_name__icontains=query).first()
        
        if not best_match:
            best_match = Product.objects.filter(category__icontains=query).first()
            if best_match:
                message = f"We couldn't find an exact match for '{query}', but here is a possible match from a similar category."
                is_fallback = True
            else:
                all_products = list(Product.objects.all())
                if all_products:
                    recommendations = random.sample(all_products, min(5, len(all_products)))
                    message = f"No results found for '{query}'. Check out these trending products instead!"
                    is_fallback = True
        
        if best_match and not recommendations:
            recommendations = get_recommendations(best_match)
            
    return render(request, 'recommender/search.html', {
        'best_match': best_match,
        'recommendations': recommendations,
        'query': query,
        'message': message,
        'is_fallback': is_fallback
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    recommendations = get_recommendations(product)
    return render(request, 'recommender/product_detail.html', {
        'product': product,
        'recommendations': recommendations
    })
