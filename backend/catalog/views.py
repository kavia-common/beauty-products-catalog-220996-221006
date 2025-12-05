from typing import Any
from django.db.models import Q, QuerySet
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Tag, Product
from .serializers import CategorySerializer, TagSerializer, ProductSerializer


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Read-only endpoints for categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Read-only endpoints for tags."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """List and retrieve products with query filtering.

    Supported filters:
    - search: text search across name, description, brand
    - brand: exact brand match
    - category: category slug or id
    - price_min, price_max: decimal ranges
    - in_stock: boolean
    - tags: comma separated tag ids
    """
    serializer_class = ProductSerializer

    def get_queryset(self) -> QuerySet[Product]:
        qs = Product.objects.select_related("category").prefetch_related("tags").all()

        search = self.request.query_params.get("search")
        brand = self.request.query_params.get("brand")
        category = self.request.query_params.get("category")  # slug or id
        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")
        in_stock = self.request.query_params.get("in_stock")
        tags = self.request.query_params.get("tags")

        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(brand__icontains=search)
            )

        if brand:
            qs = qs.filter(brand__iexact=brand)

        if category:
            if category.isdigit():
                qs = qs.filter(category_id=int(category))
            else:
                qs = qs.filter(category__slug=category)

        if price_min:
            try:
                qs = qs.filter(price__gte=float(price_min))
            except ValueError:
                pass

        if price_max:
            try:
                qs = qs.filter(price__lte=float(price_max))
            except ValueError:
                pass

        if in_stock is not None:
            val = in_stock.lower()
            if val in ("true", "1", "yes"):
                qs = qs.filter(in_stock=True)
            elif val in ("false", "0", "no"):
                qs = qs.filter(in_stock=False)

        if tags:
            try:
                tag_ids = [int(t.strip()) for t in tags.split(",") if t.strip().isdigit()]
                if tag_ids:
                    qs = qs.filter(tags__in=tag_ids).distinct()
            except Exception:
                pass

        return qs

    # PUBLIC_INTERFACE
    @action(detail=False, methods=["get"])
    def facets(self, request, *args: Any, **kwargs: Any):
        """Return simple facet counts for UI filters (brands and categories)."""
        brands = (
            Product.objects.values_list("brand", flat=True)
            .order_by("brand")
            .distinct()
        )
        categories = Category.objects.values("id", "name", "slug").order_by("name")
        return Response({"brands": list(brands), "categories": list(categories)})
