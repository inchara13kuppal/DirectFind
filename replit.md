# Product Recommender System

## Overview

This is a Django-based product recommendation system designed to manage and display product data. The application imports product information from CSV files (specifically Amazon product data) and stores them in a database for use in a recommendation engine. The project is in early development stages with the data model and import functionality established, but the recommendation logic and user-facing views are yet to be implemented.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Framework and Structure
- **Framework**: Django 5.0 with a standard project layout
- **Main Project**: `django_project/` contains settings, URLs, and WSGI/ASGI configurations
- **App**: `recommender/` is the core application handling product data and recommendations

### Data Model
The system uses a single `Product` model with the following fields:
- `product_id`: Unique identifier for products
- `product_name`: Name/title of the product
- `category`: Product category classification
- `discounted_price`: Price stored as string (allows currency symbols)
- `about_product`: Product description
- `img_link`: URL to product image

### Data Import
- `import_data.py` handles CSV imports using pandas
- Uses Django's `update_or_create` for idempotent imports
- Source data comes from CSV files in `attached_assets/` directory

### Current State
- Database migrations are set up
- Product model is defined
- CSV import utility is functional
- Views and URL routing for the recommender app are not yet implemented
- No recommendation algorithm implemented yet

## External Dependencies

### Python Packages
- **Django 5.0+**: Web framework
- **pandas**: CSV data processing for imports

### Database
- Uses Django's default SQLite database (no explicit database configuration visible)
- May need PostgreSQL for production scaling

### Environment Configuration
- Relies on `REPLIT_DOMAINS` environment variable for allowed hosts and CSRF trusted origins
- Configured specifically for Replit deployment environment

### Data Sources
- Amazon product CSV files stored in `attached_assets/` directory
- Expected CSV columns: `product_id`, `product_name`, `category`, `discounted_price`, `about_product`, `img_link`