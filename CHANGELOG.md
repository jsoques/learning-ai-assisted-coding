# Changelog

## [Unreleased]

## 2026-06-25

### Issues & Gaps Fixed

#### Security
- **Missing CSRF protection**: Added `CSRFMiddleware` using Double Submit Cookie pattern — validates `X-CSRF-Token` header against `csrf_token` cookie on all mutating HTML routes, skips `/api/*` and auth routes. Sets non-HttpOnly `csrf_token` cookie on every non-API response. Added JS in `base.html` to inject token into HTMX requests (`htmx:configRequest`) and traditional form submissions (`submit` event).
- **Missing JWT expiry on session tokens**: The session cookie JWT token had no `exp` claim, making it valid indefinitely regardless of the cookie's `max_age=86400` browser-side expiry. Added `"exp": datetime.now(timezone.utc) + timedelta(days=1)` to match the cookie lifetime.
- **Hardcoded JWT secret**: `SECRET_KEY` moved from hardcoded string to `os.environ.get("JWT_SECRET", "dev-secret-change-in-production")`.

#### Runtime Errors (500s)
- **500 on cart page**: `cart_data` dict used `"items"` as key, which conflicted with `dict.items()` method in Jinja2 resolution (dict attribute lookup takes priority over key lookup). Renamed to `"cart_items"` in both handler and template.
- **500 on checkout**: `GET /orders/checkout` route was registered after `GET /orders/{order_id}`. FastAPI matched `/orders/checkout` against the parameterized route first with `order_id="checkout"`, causing `uuid.UUID("checkout")` to raise `ValueError`. Reordered routes so specific paths come before parameterized ones.
- **500 on order-related pages**: Multiple templates (`orders/detail.html`, `orders/history.html`, `admin/dashboard.html`, `admin/orders.html`) and an f-string in `admin_update_order_status` used `order.id[:8]` to truncate UUIDs. `uuid.UUID` objects don't support Python slicing. Fixed with `(order.id|string)[:8]` in Jinja2 and `str(order.id)[:8]` in f-strings.

#### Data & Performance
- **N+1 queries**: Added `selectinload(CartModel.items)` and `selectinload(OrderModel.line_items)` to prevent lazy-load N+1 in cart and order repositories. Added `CartModel.items ↔ CartItemModel.cart` relationship.
- **Float monetary columns → Numeric**: Changed `price`, `unit_price`, `total`, `line_total` from `Float` to `Numeric(10,2)` in `models.py`. Generated Alembic migration `0efd7a183e11` with `render_as_batch=True` for SQLite.
- **Cart save rewrite**: `cart_repo.save()` rewritten from delete-all-and-reinsert to diff-based update (delete removed items, update existing quantities/prices, insert new items).

#### Code Quality
- **Deprecated `datetime.utcnow()`**: Replaced with `datetime.now(timezone.utc).replace(tzinfo=None)` across 8 files. Added `utcnow()` helper in `src/domain/__init__.py`.
- **Unused imports**: Removed unused `SessionLocal` imports from `cart_repo.py` and `inventory_repo.py`.
- **Missing EventBus**: Added `EventBus` port (`src/application/ports/event_bus.py`) and `LoggingEventBus` implementation (`src/infra/events/simple_event_bus.py`). Wired `CreateOrderUseCase` to publish `OrderPlaced`, `LowStockAlert`, `StockDepleted` and `TransitionOrderStatusUseCase` to publish `OrderCancelled`.

#### UI/UX
- **Missing `user` in template context**: 8 route handlers (`cart_page`, `orders_page`, `order_detail`, `change_password_page`, `admin_dashboard`, `admin_orders`, `admin_products`, `admin_inventory`) were not passing `user` to templates, causing navbar to always show Login/Register links even when logged in. Cart and Orders links were also hidden.
- **Missing CSRF on form submissions**: 3 traditional forms (change_password, admin products, admin categories) converted from `method=POST` to `hx-post` so they inherit CSRF header injection from base.html JS.

### Tests
- Added 15 new tests: 11 controller tests (health, auth, products, cart, orders) + 4 CSRF-specific tests (missing token, wrong token, header token, API skip).
