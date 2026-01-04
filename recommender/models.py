from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=100, unique=True)
    product_name = models.TextField()
    category = models.TextField()
    discounted_price = models.CharField(max_length=100)
    about_product = models.TextField()
    img_link = models.URLField(max_length=1000)

    @property
    def cleaned_category(self):
        if not self.category:
            return ""
        # Get the last part of the category path
        return str(self.category).split('|')[-1]

    def __str__(self):
        return str(self.product_name)
