from rest_framework import serializers
from .models import Category, Tag, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, source="tags", write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "price",
            "rating",
            "image_url",
            "description",
            "category",
            "category_id",
            "sku",
            "in_stock",
            "tags",
            "tag_ids",
        ]
