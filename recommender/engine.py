import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product

def get_recommendations(target_product):
    all_products = list(Product.objects.all())
    if not all_products:
        return []

    # Upgrade 1: Feature Weighting & Combining Fields
    # We combine name, category, and about_product
    # Upgrade 4: Keyword Boost - Give product_name 3x more importance
    # We repeat the product_name 3 times to boost its weighting in the vectorizer
    content_list = []
    for p in all_products:
        boosted_name = (p.product_name + " ") * 3
        combined_text = f"{boosted_name} {p.category} {p.about_product}"
        content_list.append(combined_text)

    # Upgrade 1: ngram_range=(1, 2) to capture phrases
    tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = tfidf.fit_transform(content_list)

    try:
        target_idx = all_products.index(target_product)
    except ValueError:
        return []

    cosine_sim = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()
    
    # Sort by similarity score and pick top 5 (excluding the target itself)
    similar_indices = cosine_sim.argsort()[::-1]
    
    recommendations = []
    for idx in similar_indices:
        if all_products[idx].id != target_product.id:
            recommendations.append(all_products[idx])
        if len(recommendations) >= 5:
            break
            
    return recommendations
