# Graph Report

Generated: 2026-06-25

**Summary**: 567 nodes · 2924 edges · 43 communities

## God Nodes

| Rank | Node | Degree | Source | Community |
|------|------|--------|--------|-----------|
| 1 | api.py | 94 | src/interface_adapters/controllers/api.py | C-1 |
| 2 | html_router.py | 86 | src/frontend/html_router.py | C-1 |
| 3 | UUID | 81 |  | C-1 |
| 4 | test_use_cases.py | 79 | tests/test_use_cases.py | C-1 |
| 5 | test_api.py | 71 | tests/test_api.py | C-1 |
| 6 | Money | 69 | src/domain/value_objects/common.py | C-1 |
| 7 | Session | 58 |  | C-1 |
| 8 | InMemoryProductRepo | 57 | tests/test_use_cases.py | C-1 |
| 9 | InMemoryCartRepo | 55 | tests/test_use_cases.py | C-1 |
| 10 | InMemoryInventoryRepo | 55 | tests/test_use_cases.py | C-1 |
| 11 | Cart | 54 | src/domain/entities/models.py | C-1 |
| 12 | ProductStatus | 53 | src/domain/value_objects/common.py | C-1 |
| 13 | InMemoryOrderRepo | 53 | tests/test_use_cases.py | C-1 |
| 14 | Product | 52 | src/domain/entities/models.py | C-1 |
| 15 | InventoryItem | 52 | src/domain/entities/models.py | C-1 |

## Community Structure

### C0 (122 nodes, cohesion 0.095)

- CSRFMiddleware [src/framework/auth/csrf.py]
- BaseHTTPMiddleware []
- add_to_cart() [src/interface_adapters/controllers/api.py]
- record_restock() [src/interface_adapters/controllers/api.py]
- register() [src/interface_adapters/controllers/api.py]
- dtos.py [src/application/dto/dtos.py]
- AddCartItemRequest [src/application/dto/dtos.py]
- CartItemResponse [src/application/dto/dtos.py]
- ... (114 more nodes)

### C1 (76 nodes, cohesion 0.054)

- abc []
- Base []
- check_inventory() [src/interface_adapters/controllers/api.py]
- create_category() [src/interface_adapters/controllers/api.py]
- list_categories() [src/interface_adapters/controllers/api.py]
- datetime []
- models.py [src/framework/db/models.py]
- CategoryModel [src/framework/db/models.py]
- ... (68 more nodes)

### C2 (60 nodes, cohesion 0.108)

- transition_order_status() [src/interface_adapters/controllers/api.py]
- OrderLineItemResponse [src/application/dto/dtos.py]
- OrderResponse [src/application/dto/dtos.py]
- TransitionOrderStatusRequest [src/application/dto/dtos.py]
- Order [src/domain/entities/models.py]
- OrderLineItem [src/domain/entities/models.py]
- events.py [src/domain/events/events.py]
- DomainEvent [src/domain/events/events.py]
- ... (52 more nodes)

### C3 (52 nodes, cohesion 0.069)

- dataclasses []
- decimal []
- models.py [src/domain/entities/models.py]
- .line_total() [src/domain/entities/models.py]
- User [src/domain/entities/models.py]
- Enum []
- UserRepository [src/application/ports/user_repository.py]
- .create() [src/application/ports/user_repository.py]
- ... (44 more nodes)

### C4 (37 nodes, cohesion 0.102)

- clear_cart() [src/interface_adapters/controllers/api.py]
- get_cart() [src/interface_adapters/controllers/api.py]
- remove_from_cart() [src/interface_adapters/controllers/api.py]
- CartItemModel [src/framework/db/models.py]
- CartModel [src/framework/db/models.py]
- Cart [src/domain/entities/models.py]
- CartRepository [src/application/ports/cart_repository.py]
- .create() [src/application/ports/cart_repository.py]
- ... (29 more nodes)

### C5 (35 nodes, cohesion 0.064)

- Alpine.js [templates/base.html]
- CHANGELOG.md [CHANGELOG.md]
- Clean Architecture [README.md]
- CSRF Middleware [CHANGELOG.md]
- docker-compose.yml [docker-compose.yml]
- Double Submit Cookie Pattern [CHANGELOG.md]
- FastAPI [pyproject.toml]
- HTMX Form Conversion [session-ses_0ff1.md]
- ... (27 more nodes)

### C6 (35 nodes, cohesion 0.069)

- builder []
- dependencyinjection []
- Extensions.cs [aspire/ECommerce.ServiceDefaults/Extensions.cs]
- Extensions [aspire/ECommerce.ServiceDefaults/Extensions.cs]
- .AddDefaultHealthChecks() [aspire/ECommerce.ServiceDefaults/Extensions.cs]
- .AddOpenTelemetryExporters() [aspire/ECommerce.ServiceDefaults/Extensions.cs]
- .AddServiceDefaults() [aspire/ECommerce.ServiceDefaults/Extensions.cs]
- .ConfigureOpenTelemetry() [aspire/ECommerce.ServiceDefaults/Extensions.cs]
- ... (27 more nodes)

### C7 (34 nodes, cohesion 0.191)

- fastapi_responses []
- fastapi_templating []
- html_router.py [src/frontend/html_router.py]
- admin_create_category() [src/frontend/html_router.py]
- admin_create_product() [src/frontend/html_router.py]
- admin_dashboard() [src/frontend/html_router.py]
- admin_inventory() [src/frontend/html_router.py]
- admin_orders() [src/frontend/html_router.py]
- ... (26 more nodes)

### C8 (30 nodes, cohesion 0.140)

- E []
- pytest []
- Result [src/application/result/__init__.py]
- .failure() [src/application/result/__init__.py]
- .is_failure() [src/application/result/__init__.py]
- .is_success() [src/application/result/__init__.py]
- .map() [src/application/result/__init__.py]
- .__post_init__() [src/application/result/__init__.py]
- ... (22 more nodes)

### C9 (28 nodes, cohesion 0.103)

- hash_password() [src/framework/auth/jwt.py]
- base64 []
- session.py [src/framework/db/session.py]
- get_db() [src/framework/db/session.py]
- composition_root.py [src/framework/di/composition_root.py]
- create_app() [src/framework/di/composition_root.py]
- seed_admin() [src/framework/di/composition_root.py]
- fastapi_middleware_cors []
- ... (20 more nodes)

### C10 (27 nodes, cohesion 0.123)

- require_admin() [src/framework/auth/dependencies.py]
- api.py [src/interface_adapters/controllers/api.py]
- admin_list_orders() [src/interface_adapters/controllers/api.py]
- create_order() [src/interface_adapters/controllers/api.py]
- create_product() [src/interface_adapters/controllers/api.py]
- delete_product() [src/interface_adapters/controllers/api.py]
- get_order() [src/interface_adapters/controllers/api.py]
- get_product() [src/interface_adapters/controllers/api.py]
- ... (19 more nodes)

### C11 (21 nodes, cohesion 0.124)

- launchSettings.json [aspire/ECommerce.AppHost/Properties/launchSettings.json]
- ASPIRE_ALLOW_UNSECURED_TRANSPORT [aspire/ECommerce.AppHost/Properties/launchSettings.json]
- ASPIRE_DASHBOARD_OTLP_ENDPOINT_URL [aspire/ECommerce.AppHost/Properties/launchSettings.json]
- ASPIRE_RESOURCE_SERVICE_ENDPOINT_URL [aspire/ECommerce.AppHost/Properties/launchSettings.json]
- ASPNETCORE_ENVIRONMENT [aspire/ECommerce.AppHost/Properties/launchSettings.json]
- DOTNET_DASHBOARD_OTLP_API_KEY [aspire/ECommerce.AppHost/Properties/launchSettings.json]
- DOTNET_ENVIRONMENT [aspire/ECommerce.AppHost/Properties/launchSettings.json]
- applicationUrl [aspire/ECommerce.AppHost/Properties/launchSettings.json]
- ... (13 more nodes)

### C12 (17 nodes, cohesion 0.118)

- pkg_alembic []
- ecommerce-api [pyproject.toml]
- pkg_fastapi []
- pkg_httpx []
- pkg_jinja2 []
- pkg_opentelemetry_api []
- pkg_opentelemetry_exporter_otlp []
- pkg_opentelemetry_instrumentation_fastapi []
- ... (9 more nodes)

### C13 (14 nodes, cohesion 0.143)

- ECommerce.slnx [aspire/ECommerce.slnx]
- net10.0 [aspire/ECommerce.AppHost/ECommerce.AppHost.csproj]
- net10.0 [aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj]
- ECommerce.AppHost.csproj [aspire/ECommerce.AppHost/ECommerce.AppHost.csproj]
- ECommerce.ServiceDefaults.csproj [aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj]
- Microsoft.Extensions.Http.Resilience (10.7.0) [aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj]
- Microsoft.Extensions.ServiceDiscovery (10.7.0) [aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj]
- OpenTelemetry.Exporter.OpenTelemetryProtocol (1.16.0) [aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj]
- ... (6 more nodes)

### C14 (12 nodes, cohesion 0.182)

- alembic []
- env.py [alembic/env.py]
- run_migrations_offline() [alembic/env.py]
- run_migrations_online() [alembic/env.py]
- logging_config []
- typing []
- 0efd7a183e11_use_numeric_for_money_columns.py [alembic/versions/0efd7a183e11_use_numeric_for_money_columns.py]
- downgrade() [alembic/versions/0efd7a183e11_use_numeric_for_money_columns.py]
- ... (4 more nodes)

### C15 (12 nodes, cohesion 0.303)

- dependencies.py [src/framework/auth/dependencies.py]
- get_current_user() [src/framework/auth/dependencies.py]
- optional_user() [src/framework/auth/dependencies.py]
- _resolve_user() [src/framework/auth/dependencies.py]
- jwt.py [src/framework/auth/jwt.py]
- decode_token() [src/framework/auth/jwt.py]
- verify_password() [src/framework/auth/jwt.py]
- bcrypt []
- ... (4 more nodes)

### C16 (9 nodes, cohesion 0.278)

- csrf.py [src/framework/auth/csrf.py]
- .dispatch() [src/framework/auth/csrf.py]
- _generate_token() [src/framework/auth/csrf.py]
- _get_cookie_token() [src/framework/auth/csrf.py]
- _get_header_token() [src/framework/auth/csrf.py]
- secrets []
- starlette_middleware_base []
- starlette_requests []
- ... (1 more nodes)

### C17 (8 nodes, cohesion 0.357)

- mailpit_adapter.py [src/infra/email/mailpit_adapter.py]
- MailpitEmailAdapter [src/infra/email/mailpit_adapter.py]
- ._send() [src/infra/email/mailpit_adapter.py]
- .send_low_stock_alert() [src/infra/email/mailpit_adapter.py]
- .send_order_confirmation() [src/infra/email/mailpit_adapter.py]
- .send_shipping_notification() [src/infra/email/mailpit_adapter.py]
- httpx []
- src_application_ports_email_port []

### C18 (6 nodes, cohesion 0.533)

- create_access_token() [src/framework/auth/jwt.py]
- create_refresh_token() [src/framework/auth/jwt.py]
- login() [src/interface_adapters/controllers/api.py]
- refresh() [src/interface_adapters/controllers/api.py]
- TokenResponse [src/application/dto/dtos.py]
- Response []

### C19 (3 nodes, cohesion 0.667)

- otel_wrapper.sh [src/framework/otel_wrapper.sh]
- OTEL_EXPORTER_OTLP_ENDPOINT [src/framework/otel_wrapper.sh]
- otel_wrapper.sh script [src/framework/otel_wrapper.sh]

### C20 (1 nodes, cohesion 1.000)

- __init__.py [src/application/__init__.py]

### C21 (1 nodes, cohesion 1.000)

- appsettings.json [aspire/ECommerce.AppHost/appsettings.json]

### C22 (1 nodes, cohesion 1.000)

- appsettings.Development.json [aspire/ECommerce.AppHost/appsettings.Development.json]

### C23 (1 nodes, cohesion 1.000)

- aspire.config.json [aspire/ECommerce.AppHost/aspire.config.json]

### C24 (1 nodes, cohesion 1.000)

- __init__.py [src/framework/auth/__init__.py]

### C25 (1 nodes, cohesion 1.000)

- __init__.py [src/interface_adapters/controllers/__init__.py]

### C26 (1 nodes, cohesion 1.000)

- __init__.py [src/framework/db/__init__.py]

### C27 (1 nodes, cohesion 1.000)

- __init__.py [src/framework/di/__init__.py]

### C28 (1 nodes, cohesion 1.000)

- __init__.py [src/application/dto/__init__.py]

### C29 (1 nodes, cohesion 1.000)

- AppHost.cs [aspire/ECommerce.AppHost/AppHost.cs]

### C30 (1 nodes, cohesion 1.000)

- __init__.py [src/domain/entities/__init__.py]

### C31 (1 nodes, cohesion 1.000)

- __init__.py [src/framework/__init__.py]

### C32 (1 nodes, cohesion 1.000)

- __init__.py [src/infra/__init__.py]

### C33 (1 nodes, cohesion 1.000)

- __init__.py [src/interface_adapters/__init__.py]

### C34 (1 nodes, cohesion 1.000)

- launchSettings.json [aspire/ECommerce.AppHost/Properties/launchSettings.json]

### C35 (1 nodes, cohesion 1.000)

- __init__.py [src/application/ports/__init__.py]

### C36 (1 nodes, cohesion 1.000)

- __init__.py [src/interface_adapters/serializers/__init__.py]

### C37 (1 nodes, cohesion 1.000)

- __init__.py [src/domain/events/__init__.py]

### C38 (1 nodes, cohesion 1.000)

- __init__.py [src/infra/events/__init__.py]

### C39 (1 nodes, cohesion 1.000)

- __init__.py [src/__init__.py]

### C40 (1 nodes, cohesion 1.000)

- __init__.py [tests/__init__.py]

### C41 (1 nodes, cohesion 1.000)

- __init__.py [src/application/use_cases/__init__.py]

### C42 (1 nodes, cohesion 1.000)

- __init__.py [src/domain/value_objects/__init__.py]

## Suggested Questions

1. What is the overall architecture of this project?
2. How do the god nodes (api.py, html_router.py) connect the system?
3. What are the key domain entities and relationships?
4. How is authentication and authorization handled?
5. What testing patterns are used?
6. How does cart/order/inventory flow work end-to-end?
7. What infrastructure (databases, caching, email) is configured?
