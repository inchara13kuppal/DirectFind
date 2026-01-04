from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from .engine import get_recommendations
import random

def home(request):
    # Show some random products on the home page so it's not empty
    all_products = Product.objects.all()
    sample_products = random.sample(list(all_products), min(len(all_products), 3)) if all_products.exists() else []
    return render(request, 'recommender/search.html', {'recommendations': sample_products})

def search(request):
    query = request.GET.get('query')
    best_match = None
    recommendations = []
    message = None
    is_fallback = False

    if query:
        # Looking for product_name to match your seed data
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

# --- SEED DATA FUNCTION ---
def seed_data(request):
    # Clear existing data
    Product.objects.all().delete()

    data = [
        {"id": "c1", "n": "4K HDMI Cable", "d": "Gold-plated 6ft cable for ultra HD gaming.", "c": "Electronics", "p": 14.99, "i": "https://images.unsplash.com/photo-1555529731-118a5bb67af7?w=400"},
        {"id": "c2", "n": "USB-C Fast Charger", "d": "Braided 2-meter cable for fast charging.", "c": "Electronics", "p": 19.50, "i": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=400"},
        {"id": "h1", "n": "Wireless Headphones", "d": "Noise cancelling over-ear headphones.", "c": "Tech", "p": 120.00, "i": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"},
        {"id": "m1", "n": "Gaming Mouse", "d": "High precision RGB gaming mouse.", "c": "Tech", "p": 45.00, "i": "https://images.unsplash.com/photo-1527814732105-9d2c5bb71055?w=400"},
    ]

    for item in data:
        Product.objects.create(
            product_id=item['id'],
            product_name=item['n'],
            description=item['d'],
            category=item['c'],
            price=item['p'],
            image_url=item['i']
        )

    return HttpResponse("<h1>Success!</h1><p>DirectFind database has been seeded. <a href='/'>Go to Home</a></p>")