# E-Commerce Order & Inventory Management System

A full-stack e-commerce backend built with **FastAPI (Clean Architecture)**, **HTMX** frontend, **SQLite**, **.NET Aspire** orchestration, and **Mailpit** email capture.

---
## How I started
On command prompt, start with: (selected OpenCode and Windsurf, I use Windsurf(devin) later to validate what Opencode/Openspec did)  
```sh
openspec init
```
Then fire up OpenCode:  
```sh
opencode .
```
Then start openspec prompt with /opsx-propose with this:  
```
using knowledge from skill 'clean-architecture-python' create a FastAPI application
to build an e-commerce order and inventory system with full auth. We will start by using SQLite. I want .Net
Aspire to orchestrate and monitor the FastApi application. If emailing will be used, instead if Sendgrid, I would
like to use Mailpit.
```
---
> [!NOTE]
> This is still a work in progress as I am learning this slew of tools that are pouring in our daily feeds for knowledge...
---

## Table of Contents

- [Prompts Given During Development](#prompts-given-during-development)
- [AI Tools Involved](#ai-tools-involved)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Deploying to Azure](#deploying-to-azure)
- [Updating Libraries](#updating-libraries)
- [Suggested Next Steps](#suggested-next-steps)

---

## Prompts Given During Development

All prompts are listed in chronological order as they were issued to the AI assistant:

1. **Design an e-commerce order and inventory management system** — Initial project proposal; the AI designed the system, produced specs (user auth, product catalog, shopping cart, order management, inventory tracking, email notifications, Aspire orchestration), and generated a plan.

2. **"I want to implement it"** — Triggered full implementation of all planned phases.

3. **"archive"** — Archived the completed change after implementation and verification.

4. **"how to run the tests?"** — Asked how to execute the test suite.

5. **"Let's use port 5566 instead of 8000"** — Changed the application port from 8000 to 5566 across all configuration files.

6. **"the docker build is failing"** — Fixed Dockerfile build order (copy `pyproject.toml` before source files for better layer caching).

7. **"Add a frontend with HTMX, Jinja2, Alpine.js, Tailwind CSS"** — Requested a server-rendered HTML frontend; resulted in 27 HTML routes, 14 Jinja2 templates, and a full admin dashboard.

8. **"The admin user should be forced to change password on first login"** — Added `must_change_password` column and Alembic migration, enforced in login flow.

9. **"What did we do so far?"** — Asked for a project status summary and milestone archive.

10. **"Fix two issues: error parameter in Jinja2 templates is not being passed consistently + RedirectResponse in dependencies causes problems"** — Fixed missing `error` context in template rendering and replaced `RedirectResponse` raises with `Response` headers.

11. **"When I access the root, I should see a landing page"** — Created `templates/index.html` with hero section, category grid, and featured products.

12. **Error running the app (Jinja2 TypeError)** — Diagnosed and fixed `TypeError: cannot use 'tuple' as a dict key` caused by incorrect `TemplateResponse` argument order.

13. **Fix TemplateResponse argument order + API prefix + route ordering** — Fixed `(request, name, context)` signature, moved API routes under `/api` prefix, reordered HTML router before API router.

14. **"What is the admin user email and password?"** — Asked for admin credentials (`admin@shop.com` / `admin123`).

15. **"If there are no products, seed with 100 mock products on startup"** — Added 100 products across 8 categories with inventory, seeded at startup if the database is empty.

16. **"Protect the /docs URL, only allow admin role"** — Added middleware to protect `/docs`, `/redoc`, and `/openapi.json`.

17. **"Use HTTP Basic Authentication for the docs"** — Changed docs protection to HTTP Basic Auth verified against the `users` table.

18. **"Can the endpoints be categorized or grouped in Swagger?"** — Added OpenAPI tags to all routes for Swagger/ReDoc grouping.

19. **"Rename the 'default' tag to 'HTMx-FrontEnd'"** — Renamed the default tag to `HTMx-FrontEnd` for clarity.

20. **"Update the Aspire project to start the FastAPI application as a Python project instead of a Docker image"** — Switched from `AddContainer` (Docker) to `AddExecutable` (direct Python process) in `AppHost.cs`.

21. **"Is this OTEL trace export error something to worry about?"** — Confirmed `localhost:4317` connection refused is harmless during local dev without an OpenTelemetry collector.

22. **"Can the authorize method in Swagger ask for user and password instead of bearer?"** — Added HTTP Basic Auth security scheme alongside Bearer in the OpenAPI spec so Swagger's Authorize button accepts email/password.

23. **"Write a README.md with all the prompts I have given to you"** — This document.

24. **"Running tests, I get these warnings: on_event is deprecated, use lifespan event handlers instead"** — Replaced `@app.on_event("startup")` with FastAPI lifespan context manager in `composition_root.py`.

25. **"The app is very slow to start and pages load very slowly"** — Made OpenTelemetry opt-in (conditional on `OTEL_EXPORTER_OTLP_ENDPOINT` being set); added gRPC connection timeout; swapped `SimpleSpanProcessor` for `BatchSpanProcessor`; added SQLite WAL mode + `synchronous=NORMAL` + busy timeout.

---

## AI Tools Involved

| Tool | Role |
|------|------|
| **OpenCode(with openspec)** | Primary AI coding assistant — wrote all code, ran commands, debugged issues across the full stack |
| **GSD Skills** (gsd-new-project, gsd-discuss-phase, gsd-plan-phase, gsd-execute-phase, gsd-verify-work, gsd-archive-change) | Structured development workflow: project initialization, phase discussion, planning, execution, verification, and archiving |
| **brainstorming skill** | Explored design options and requirements before implementation |
| **dotnet-api skill** | Guided .NET Aspire project structure and AppHost configuration |
| **fastapi skill** | Provided FastAPI best practices for route design, dependencies, and middleware |

---

## Technologies Used

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12+ | Runtime |
| **FastAPI** | 0.115+ | Web framework (async, OpenAPI auto-docs) |
| **Uvicorn** | 0.32+ | ASGI server |
| **SQLAlchemy** | 2.0+ | ORM / database access |
| **Alembic** | 1.14+ | Database migrations |
| **Pydantic** | 2.10+ | Data validation / settings management |
| **python-jose** | 3.3+ | JWT encoding/decoding |
| **passlib[bcrypt]** | 1.7+ | Password hashing |
| **Jinja2** | 3.1+ | Server-side HTML template rendering |
| **python-multipart** | 0.0.9+ | Form data parsing for login/register |
| **httpx** | 0.28+ | HTTP client (email sending to Mailpit) |
| **OpenTelemetry** | 1.29+ | Distributed tracing / metrics |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTMX** | AJAX-driven dynamic updates (loaded via CDN) |
| **Alpine.js** | Lightweight JavaScript interactivity (loaded via CDN) |
| **Tailwind CSS** | Utility-first CSS framework (loaded via CDN) |

### Infrastructure / DevOps

| Technology | Purpose |
|------------|---------|
| **SQLite** | Development database (single file, zero config) |
| **Docker** | Containerization (app + Mailpit) |
| **.NET Aspire** | Local orchestration dashboard (OTEL tracing, logs) |
| **Mailpit** | Local email capture (SMTP + web UI on port 8025) |
| **pytest** | Test framework |

---

## Architecture

### Clean Architecture (Hexagonal)

The application follows **Clean Architecture** with strict dependency inversion — inner layers never import from outer layers.

```
┌──────────────────────────────────────────────┐
│              Framework Layer                  │
│  (FastAPI, SQLAlchemy, JWT, Uvicorn, DI)      │
│  src/framework/                                │
│                                                │
│  ┌──────────────────────────────────────────┐  │
│  │       Interface Adapters Layer            │  │
│  │  (REST controllers, serializers)          │  │
│  │  src/interface_adapters/                   │  │
│  │                                            │  │
│  │  ┌──────────────────────────────────────┐ │  │
│  │  │      Application Layer                │ │  │
│  │  │  (Use cases, DTOs, Ports, Result)     │ │  │
│  │  │  src/application/                      │ │  │
│  │  │                                        │ │  │
│  │  │  ┌──────────────────────────────────┐ │ │  │
│  │  │  │       Domain Layer                │ │ │  │
│  │  │  │  (Entities, Value Objects,        │ │ │  │
│  │  │  │   Domain Events)                  │ │ │  │
│  │  │  │  src/domain/                       │ │ │  │
│  │  │  └──────────────────────────────────┘ │ │  │
│  │  └──────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────┘  │
│                                                │
│  ┌──────────────────────────────────────────┐  │
│  │        Infrastructure Layer               │  │
│  │  (SQLAlchemy repos, Mailpit email)        │  │
│  │  src/infra/                                │  │
│  └──────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘

         Frontend Layer (HTMX + Jinja2)
         src/frontend/html_router.py
         templates/
```

### Layer Rules

| Layer | Dependencies | Key Contents |
|-------|-------------|--------------|
| **Domain** | None (pure Python) | `entities/models.py` — User, Product, Order, Cart, Inventory entities; `value_objects/common.py` — Email, Money, Address; `events/events.py` — domain events |
| **Application** | Domain only | `use_cases/` — 5 use case files (auth, cart, inventory, order, product); `dto/dtos.py` — request/response DTOs; `ports/` — 6 repository ABCs; `result/` — Result[T] type |
| **Interface Adapters** | Application | `controllers/api.py` — 24 REST endpoints; serializers |
| **Infrastructure** | Application | `repositories/` — 5 SQLAlchemy repo implementations; `email/mailpit_adapter.py` — Mailpit email sender |
| **Framework** | All above + FastAPI | `auth/` — JWT + dependencies; `db/models.py` — SQLAlchemy ORM models; `db/session.py` — engine + session (WAL mode); `di/composition_root.py` — FastAPI app factory, DI wiring, middleware, lifespan (seed data); `main.py` — entry point, conditional OTEL setup |
| **Frontend** | Application + Jinja2 | `html_router.py` — 27 HTML routes; `templates/` — 14 Jinja2 templates |

### Key Design Decisions

- **Result type over exceptions**: Every use case returns `Result.success(value)` or `Result.failure(error)`. No exception flow for business logic.
- **Session cookie auth for HTML**: JWT-wrapped `session_token` cookie for browser users; Bearer tokens for API clients.
- **Swagger accepts both Bearer and Basic Auth**: The `Authorize` button shows username/password fields (Basic Auth) and a token field (Bearer JWT).
- **HTML routes before API routes**: Router include order prevents path conflicts; API routes live under `/api` prefix.
- **Docs protected by middleware-level HTTP Basic Auth**: Checked against `users` table (admin role only), not route-level dependencies.
- **Auto-seeding on startup**: Admin user + 100 products across 8 categories + inventory records created via FastAPI lifespan context manager.
- **Aspire via AddExecutable**: Python process runs directly (not in Docker) for faster local iteration; environment variables configured inline.
- **OpenTelemetry opt-in**: Only configured when `OTEL_EXPORTER_OTLP_ENDPOINT` is set (no default). Uses `BatchSpanProcessor` over gRPC with 5s connect timeout.
- **SQLite WAL mode**: `PRAGMA journal_mode=WAL` + `synchronous=NORMAL` for concurrent read performance and faster writes.

### Database Schema (SQLAlchemy Models)

- **users** — `id`, `email`, `hashed_password`, `role`, `must_change_password`, timestamps
- **categories** — `id`, `name`, `description`
- **products** — `id`, `sku`, `name`, `description`, `price`, `category_id`, `status`, timestamps
- **carts** — `id`, `user_id`, `session_id`, timestamps
- **cart_items** — `id`, `cart_id`, `product_id`, `quantity`, `unit_price`
- **orders** — `id`, `user_id`, `status`, `total`, timestamps
- **order_line_items** — `id`, `order_id`, `product_id`, `product_name`, `quantity`, `unit_price`, `line_total`
- **inventory** — `product_id`, `on_hand`, `reserved`, `low_stock_threshold`
- **restock_events** — `id`, `product_id`, `quantity`, `timestamp`

### API Endpoints

| Group | Count | Prefix |
|-------|-------|--------|
| Health | 1 | `GET /api/health` |
| Auth | 5 | `POST /api/auth/register, /login, /refresh, /logout`, `GET /me` |
| Categories | 2 | `GET /api/categories`, `GET /api/categories/{id}` |
| Products | 5 | CRUD + `GET /api/products` |
| Cart | 4 | `GET /api/cart`, `POST /api/cart/items`, `PATCH /api/cart/items/{id}`, `DELETE /api/cart/items/{id}` |
| Orders | 4 | `GET /api/orders`, `POST /api/orders`, `GET /api/orders/{id}`, `POST /api/orders/{id}/cancel` |
| Admin | 2 | `POST /api/admin/products`, `PATCH /api/admin/products/{id}` |
| Inventory | 1 | `PATCH /api/inventory/{product_id}` |

Plus **27 HTML routes** under `src/frontend/html_router.py` for the HTMX frontend.

---

## Getting Started

### Prerequisites

- Python 3.12+
- .NET 9+ SDK (only for Aspire orchestration; the app runs without it)
- Docker / Docker Compose (optional, for containerized deployment)
- Mailpit (optional, for email capture — auto-started via Docker or Aspire)

### Quick Start (No Docker, No Aspire)

```bash
# 1. Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -e ".[dev]"

# 3. Copy environment file
cp .env.example .env

# 4. Start Mailpit (optional — in another terminal)
docker run -d -p 8025:8025 -p 1025:1025 axllent/mailpit

# 5. Run the application
python -m src.framework.main
# or: uvicorn src.framework.main:app --reload --port 5566

# 6. Open in browser
# Main app:   http://localhost:5566
# API docs:   http://localhost:5566/docs    (admin admin@shop.com / admin123)
# Mailpit UI: http://localhost:8025
```

### With .NET Aspire Dashboard

```bash
# Stop python app from above if started separately
cd aspire
dotnet run --project ECommerce.AppHost
# Opens dashboard at https://localhost:15888
```

### With Docker Compose

```bash
docker compose up --build
```

### Admin Credentials

| Field | Value |
|-------|-------|
| Email | `admin@shop.com` |
| Password | `admin123` |
| Note | You'll be prompted to change password on first login |

### Running Tests

```bash
pytest                          # All tests with coverage
pytest -v                       # Verbose
pytest --cov=src --cov-report=term-missing  # Coverage report
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# View history
alembic history
```

---

## Deploying to Azure

### Option 1: Azure Container Apps (Recommended)

```bash
# Prerequisites
#   az login
#   az group create --name myEcommerceGroup --location westeurope

# Build and push to Azure Container Registry
az acr create --name myecommerceacr --resource-group myEcommerceGroup --sku Basic
az acr build --registry myecommerceacr --image ecommerce-api:latest .

# Deploy to Container Apps
az containerapp create \
  --name ecommerce-api \
  --resource-group myEcommerceGroup \
  --environment myEnvironment \
  --image myecommerceacr.azurecr.io/ecommerce-api:latest \
  --target-port 5566 \
  --ingress external \
  --query properties.configuration.ingress.fqdn

# Set environment variables
az containerapp update \
  --name ecommerce-api \
  --resource-group myEcommerceGroup \
  --set-env-vars \
    DATABASE_URL="sqlite:///data/ecommerce.db" \
    JWT_SECRET="<secure-random-secret>" \
    OTEL_EXPORTER_OTLP_ENDPOINT="" \  # OTEL opt-in (set endpoint to enable)
    MAILPIT_URL="<your-mailpit-url>"

# Enable file share for SQLite persistence (optional)
az containerapp volume add \
  --name ecommerce-api \
  --resource-group myEcommerceGroup \
  --storage-type AzureFile \
  --mount-path /app/data
```

### Option 2: Azure App Service

```bash
# Create App Service (Linux, Python 3.12)
az webapp create \
  --name ecommerce-api-app \
  --resource-group myEcommerceGroup \
  --runtime PYTHON:3.12 \
  --sku B1

# Deploy via zip or configure CI/CD
az webapp config set \
  --name ecommerce-api-app \
  --resource-group myEcommerceGroup \
  --startup-file "uvicorn src.framework.main:app --host 0.0.0.0 --port 8000"

az webapp config appsettings set \
  --name ecommerce-api-app \
  --resource-group myEcommerceGroup \
  --settings \
    DATABASE_URL="sqlite:///data/ecommerce.db" \
    JWT_SECRET="<secure-random-secret>" \
    OTEL_EXPORTER_OTLP_ENDPOINT=""
    ```

### Option 3: Azure VM with Docker

```bash
# Create VM with Docker
az vm create \
  --name ecommerce-vm \
  --resource-group myEcommerceGroup \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys

# SSH in and run
docker compose up -d
```

### Production Checklist

- [ ] Change `JWT_SECRET` to a strong random value (use `openssl rand -hex 32`)
- [ ] Replace SQLite with PostgreSQL or Azure SQL for production
- [ ] Set up a real email provider (SendGrid, SMTP) instead of Mailpit
- [ ] Disable OpenTelemetry (leave `OTEL_EXPORTER_OTLP_ENDPOINT` unset) unless using an OTLP collector
- [ ] Disable CORS `allow_origins=["*"]` — restrict to your frontend domain
- [ ] Set up proper logging (Azure Monitor / Application Insights)
- [ ] Configure a reverse proxy (Nginx / Caddy) for TLS termination
- [ ] Run database migrations via Alembic before deploying new versions

---

## Updating Libraries

### Python Dependencies

```bash
# Update all pinned dependencies to latest compatible versions
pip install --upgrade -e ".[dev]"

# Or use pip-tools for dependency pinning
pip install pip-tools
pip-compile --upgrade pyproject.toml
pip-sync requirements.txt

# Update a specific package
pip install fastapi@latest

# Check for outdated packages
pip list --outdated
```

### .NET Aspire Dependencies

```bash
cd aspire
# Check for outdated NuGet packages
dotnet list package --outdated

# Update all packages in the solution
dotnet update

# Update a specific package
dotnet add ECommerce.AppHost package Aspire.AppHost.Sdk --version <latest>
dotnet add ECommerce.ServiceDefaults package OpenTelemetry.Exporter.OpenTelemetryProtocol --version <latest>
```

After updating, run the full test suite:

```bash
pytest
```

---

## Suggested Next Steps

### Short-term (1-2 days)

- [ ] **Replace SQLite with PostgreSQL** — Use `asyncpg` + SQLAlchemy async engine for better concurrency and reliability. Add a `docker-compose.yml` service for PostgreSQL.
- [ ] **Add proper password reset flow** — Email-based reset token with expiry, sent via Mailpit/SMTP.
- [ ] **Add pagination to product listing** — `GET /api/products?page=1&per_page=20` with total count and next/prev links.
- [ ] **Add product search/filter** — Full-text search on product name/description, filter by category, price range, sort by price/name.
- [ ] **Add checkout flow** — Address collection, order summary confirmation page, order placement with inventory deduction.

### Medium-term (1-2 weeks)

- [ ] **Replace SQLite with Azure SQL Database or PostgreSQL (Azure Database for PostgreSQL Flexible Server)** — Production-grade database with automated backups, geo-replication, and connection pooling.
- [ ] **Add payment integration** — Stripe Checkout or PayPal integration for order payment.
- [ ] **Add real email provider** — SendGrid, AWS SES, or SMTP2API for transactional emails (order confirmation, shipping updates, password reset).
- [ ] **Add admin product CRUD UI** — Image upload, rich text descriptions, inventory management form in the admin dashboard.
- [ ] **Add user address management** — Multiple saved addresses per user with default shipping/billing selection.
- [ ] **Add order status workflow** — State machine (pending → confirmed → shipped → delivered → cancelled) with validation at each transition.
- [ ] **Add CI/CD pipeline** — GitHub Actions or Azure DevOps for automated testing, linting, and deployment to Azure Container Apps.

### Long-term (1-3 months)

- [ ] **Add caching layer** — Redis via `fastapi-cache` for product catalog, session storage, rate limiting.
- [ ] **Add rate limiting** — `slowapi` or custom middleware to prevent abuse on auth and checkout endpoints.
- [ ] **Add webhook support** — Send order status change webhooks to external systems.
- [ ] **Add admin analytics dashboard** — Sales charts, popular products, revenue trends, customer acquisition metrics.
- [ ] **Add multi-tenant support** — Organization-scoped products, orders, and users.
- [ ] **Add API versioning** — URL-based (`/api/v1/`) or header-based versioning for backwards compatibility.
- [ ] **Add automated E2E tests** — Playwright or Selenium tests for the HTMX frontend.
- [ ] **Add load testing** — Locust or k6 scripts for performance benchmarking.
- [ ] **Add CDN for static assets** — Move Tailwind/Alpine/HTMX from CDN to bundled static files with cache-busting.
- [ ] **Add OpenAPI client generation** — Generate TypeScript/Python client SDKs from the OpenAPI spec.
- [ ] **Add Kubernetes manifests** — Helm charts or Kustomize for production deployment to AKS.
