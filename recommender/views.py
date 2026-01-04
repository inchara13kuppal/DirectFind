from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from .engine import get_recommendations
import random
import csv
import os
from django.conf import settings

def home(request):
    """Displays the home page with a few random product suggestions."""
    all_products = Product.objects.all()
    # Safely pick 3 random products if they exist
    sample_products = random.sample(list(all_products), min(len(all_products), 3)) if all_products.exists() else []
    return render(request, 'recommender/search.html', {'recommendations': sample_products})

def search(request):
    """Handles the search logic and ML recommendations."""
    query = request.GET.get('query')
    best_match = None
    recommendations = []
    message = None
    is_fallback = False

    if query:
        # Search using the correct field name: product_name
        best_match = Product.objects.filter(product_name__icontains=query).first()

        if not best_match:
            # Fallback to category search
            best_match = Product.objects.filter(category__icontains=query).first()
            if best_match:
                message = f"We couldn't find an exact match for '{query}', but check this out!"
                is_fallback = True
            else:
                # If nothing found, show random trending items
                all_products = list(Product.objects.all())
                if all_products:
                    recommendations = random.sample(all_products, min(5, len(all_products)))
                    message = f"No results found for '{query}'. Here are some trending products!"
                    is_fallback = True

        # Get ML-based recommendations if we found a match
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
    """Displays the details for a specific product."""
    product = get_object_or_404(Product, product_id=product_id)
    recommendations = get_recommendations(product)
    return render(request, 'recommender/product_detail.html', {
        'product': product,
        'recommendations': recommendations
    })

def seed_data(request):
    """Clears the database and adds fresh sample data matching your models.py."""
    # This deletes old data to prevent duplicates
    Product.objects.all().delete()

    data = [
        {
            "id": "item_001", 
            "name": "4K Ultra HD HDMI Cable", 
            "cat": "Electronics|Accessories|Cables", 
            "price": "₹899", 
            "about": "High-speed 6ft gold-plated HDMI cable for gaming and 4K video.", 
            "img": "https://images.unsplash.com/photo-1555529731-118a5bb67af7?w=500"
        },
        {
            "id": "item_002", 
            "name": "Braided USB-C Fast Charger", 
            "cat": "Electronics|Mobile|Charging", 
            "price": "₹1,200", 
            "about": "Durable 2-meter braided cable supports 65W fast charging.", 
            "img": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=500"
        },
        {
            "id": "item_003", 
            "name": "Noise Cancelling Headphones", 
            "cat": "Electronics|Audio|Headphones", 
            "price": "₹4,999", 
            "about": "Over-ear Bluetooth headphones with active noise cancellation and 40h battery.", 
            "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"
        }
    ]

    for item in data:
        Product.objects.create(
            product_id=item['id'],
            product_name=item['name'],
            category=item['cat'],
            discounted_price=item['price'],
            about_product=item['about'],
            img_link=item['img']
        )

    # .encode() fixes the 'bytes' warning in the Replit editor
    response_html = "<h1>Success!</h1><p>Database seeded successfully. <a href='/'>Go to Home</a></p>"
    return HttpResponse(response_html.encode())

def upload_from_csv(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'attached_assets', 'products.csv')

    if not os.path.exists(csv_file_path):
        return HttpResponse(f"Error: CSV not found at {csv_file_path}".encode())

    Product.objects.all().delete()

    # We'll keep track of IDs we've already added in this run
    processed_ids = set()
    count = 0

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                p_id = row.get('product_id')

                # SKIP if the ID is missing or already processed
                if not p_id or p_id in processed_ids:
                    continue

                Product.objects.create(
                    product_id=p_id,
                    product_name=row.get('product_name'),
                    category=row.get('category'),
                    discounted_price=row.get('discounted_price'),
                    about_product=row.get('about_product'),
                    img_link=row.get('img_link')
                )
                processed_ids.add(p_id)
                count += 1

        return HttpResponse(f"<h1>Success!</h1><p>Uploaded {count} unique products from CSV.</p>".encode())
    except Exception as e:
        return HttpResponse(f"Error processing CSV: {str(e)}".encode())