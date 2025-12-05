# beauty-products-catalog-220996-221006

Backend API highlights:
- Endpoints under `/api/`
  - `GET /api/products/` list with filters: `search`, `brand`, `category` (slug or id), `price_min`, `price_max`, `in_stock`, `tags` (comma separated ids)
  - `GET /api/products/{id}/` retrieve
  - `GET /api/products/facets/` brands and categories for UI filter options
  - `GET /api/categories/` and `/api/categories/{slug}/`
  - `GET /api/tags/` and `/api/tags/{id}/`
- Pagination: page size 12 (query param `page=2` etc.)
- CORS: allows http://localhost:3000 by default.

Sample data:
- After migrations, seed with: `python manage.py seed_products`
  - This loads `catalog/fixtures/products.json`.

Notes on environment variables:
- None strictly required for local usage; CORS origins can be adjusted via `CORS_ALLOWED_ORIGINS` in settings.

API docs:
- Swagger UI at `/docs`