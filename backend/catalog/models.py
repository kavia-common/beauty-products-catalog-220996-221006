from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Represents a product category (e.g., Skincare, Makeup)."""
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, help_text="URL-safe slug for the category.")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # Auto-generate slug if not provided
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Optional tag for products (e.g., Vegan, New, Best Seller)."""
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Core product entity for the catalogue."""
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=120, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, help_text="Average rating from 0.0 to 5.0")
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    sku = models.CharField(max_length=64, unique=True, help_text="Stock keeping unit.")
    in_stock = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["brand"]),
            models.Index(fields=["name"]),
            models.Index(fields=["in_stock"]),
        ]

    def __str__(self) -> str:
        return f"{self.brand} {self.name}"
