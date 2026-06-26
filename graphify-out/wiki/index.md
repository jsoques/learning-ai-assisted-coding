# Project Knowledge Graph

**567 nodes · 2924 edges · 43 communities**

## God Nodes (Top 15 by Degree)

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

## Communities

| ID | Nodes | Cohesion | Key Files |
|----|-------|----------|-----------|
| C0 | 122 | 0.095 | tests/test_use_cases.py, tests/test_api.py, src/application/use_cases/product_use_cases.py |
| C1 | 76 | 0.054 | src/infra/repositories/product_repo.py, tests/test_use_cases.py, src/infra/repositories/inventory_repo.py |
| C2 | 60 | 0.108 | src/application/use_cases/order_use_cases.py, src/infra/repositories/order_repo.py, src/domain/events/events.py |
| C3 | 52 | 0.069 | tests/test_value_objects.py, src/domain/value_objects/common.py, src/infra/repositories/user_repo.py |
| C4 | 37 | 0.102 | src/infra/repositories/cart_repo.py, tests/test_use_cases.py, src/application/ports/cart_repository.py |
| C5 | 35 | 0.064 | templates/base.html, CHANGELOG.md, pyproject.toml |
| C6 | 35 | 0.069 | aspire/ECommerce.ServiceDefaults/Extensions.cs, src/framework/main.py |
| C7 | 34 | 0.191 | src/frontend/html_router.py |
| C8 | 30 | 0.140 | src/application/result/__init__.py, tests/test_result.py, src/application/use_cases/product_use_cases.py |
| C9 | 28 | 0.103 | tests/test_api.py, src/framework/di/composition_root.py, src/framework/db/session.py |
| C10 | 27 | 0.123 | src/interface_adapters/controllers/api.py, src/infra/repositories/product_repo.py, src/framework/auth/dependencies.py |
| C11 | 21 | 0.124 | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| C12 | 17 | 0.118 | pyproject.toml |
| C13 | 14 | 0.143 | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj, aspire/ECommerce.AppHost/ECommerce.AppHost.csproj, aspire/ECommerce.slnx |
| C14 | 12 | 0.182 | alembic/env.py, alembic/versions/0efd7a183e11_use_numeric_for_money_columns.py, alembic/versions/b6c8a5ea7783_initial_schema.py |
| C15 | 12 | 0.303 | src/framework/auth/dependencies.py, src/framework/auth/jwt.py |
| C16 | 9 | 0.278 | src/framework/auth/csrf.py |
| C17 | 8 | 0.357 | src/infra/email/mailpit_adapter.py |
| C18 | 6 | 0.533 | src/framework/auth/jwt.py, src/interface_adapters/controllers/api.py, src/application/dto/dtos.py |
| C19 | 3 | 0.667 | src/framework/otel_wrapper.sh |
| C20 | 1 | 1.000 | src/application/__init__.py |
| C21 | 1 | 1.000 | aspire/ECommerce.AppHost/appsettings.json |
| C22 | 1 | 1.000 | aspire/ECommerce.AppHost/appsettings.Development.json |
| C23 | 1 | 1.000 | aspire/ECommerce.AppHost/aspire.config.json |
| C24 | 1 | 1.000 | src/framework/auth/__init__.py |
| C25 | 1 | 1.000 | src/interface_adapters/controllers/__init__.py |
| C26 | 1 | 1.000 | src/framework/db/__init__.py |
| C27 | 1 | 1.000 | src/framework/di/__init__.py |
| C28 | 1 | 1.000 | src/application/dto/__init__.py |
| C29 | 1 | 1.000 | aspire/ECommerce.AppHost/AppHost.cs |
| C30 | 1 | 1.000 | src/domain/entities/__init__.py |
| C31 | 1 | 1.000 | src/framework/__init__.py |
| C32 | 1 | 1.000 | src/infra/__init__.py |
| C33 | 1 | 1.000 | src/interface_adapters/__init__.py |
| C34 | 1 | 1.000 | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| C35 | 1 | 1.000 | src/application/ports/__init__.py |
| C36 | 1 | 1.000 | src/interface_adapters/serializers/__init__.py |
| C37 | 1 | 1.000 | src/domain/events/__init__.py |
| C38 | 1 | 1.000 | src/infra/events/__init__.py |
| C39 | 1 | 1.000 | src/__init__.py |
| C40 | 1 | 1.000 | tests/__init__.py |
| C41 | 1 | 1.000 | src/application/use_cases/__init__.py |
| C42 | 1 | 1.000 | src/domain/value_objects/__init__.py |

### Community 0 (122 nodes, cohesion 0.095)

| Node | Label | Type | File |
|------|-------|------|------|
| auth_csrf_csrfmiddleware | CSRFMiddleware | code | src/framework/auth/csrf.py |
| basehttpmiddleware | BaseHTTPMiddleware | code |  |
| controllers_api_add_to_cart | add_to_cart() | code | src/interface_adapters/controllers/api.py |
| controllers_api_record_restock | record_restock() | code | src/interface_adapters/controllers/api.py |
| controllers_api_register | register() | code | src/interface_adapters/controllers/api.py |
| dto_dtos | dtos.py | code | src/application/dto/dtos.py |
| dto_dtos_addcartitemrequest | AddCartItemRequest | code | src/application/dto/dtos.py |
| dto_dtos_cartitemresponse | CartItemResponse | code | src/application/dto/dtos.py |
| dto_dtos_cartresponse | CartResponse | code | src/application/dto/dtos.py |
| dto_dtos_categoryrequest | CategoryRequest | code | src/application/dto/dtos.py |
| dto_dtos_categoryresponse | CategoryResponse | code | src/application/dto/dtos.py |
| dto_dtos_createproductrequest | CreateProductRequest | code | src/application/dto/dtos.py |
| dto_dtos_inventoryresponse | InventoryResponse | code | src/application/dto/dtos.py |
| dto_dtos_loginrequest | LoginRequest | code | src/application/dto/dtos.py |
| dto_dtos_paginatedresponse | PaginatedResponse | code | src/application/dto/dtos.py |
| dto_dtos_productresponse | ProductResponse | code | src/application/dto/dtos.py |
| dto_dtos_registeruserrequest | RegisterUserRequest | code | src/application/dto/dtos.py |
| dto_dtos_restockrequest | RestockRequest | code | src/application/dto/dtos.py |
| dto_dtos_updateproductrequest | UpdateProductRequest | code | src/application/dto/dtos.py |
| entities_models_cartitem | CartItem | code | src/domain/entities/models.py |
| ... | ... (102 more nodes) | ... | ... |

### Community 1 (76 nodes, cohesion 0.054)

| Node | Label | Type | File |
|------|-------|------|------|
| abc | abc |  |  |
| base | Base | code |  |
| controllers_api_check_inventory | check_inventory() | code | src/interface_adapters/controllers/api.py |
| controllers_api_create_category | create_category() | code | src/interface_adapters/controllers/api.py |
| controllers_api_list_categories | list_categories() | code | src/interface_adapters/controllers/api.py |
| datetime | datetime | code |  |
| db_models | models.py | code | src/framework/db/models.py |
| db_models_categorymodel | CategoryModel | code | src/framework/db/models.py |
| db_models_inventorymodel | InventoryModel | code | src/framework/db/models.py |
| db_models_orderlineitemmodel | OrderLineItemModel | code | src/framework/db/models.py |
| db_models_ordermodel | OrderModel | code | src/framework/db/models.py |
| db_models_productmodel | ProductModel | code | src/framework/db/models.py |
| db_models_restockeventmodel | RestockEventModel | code | src/framework/db/models.py |
| db_models_utcnow | _utcnow() | code | src/framework/db/models.py |
| di_composition_root_seed_products | seed_products() | code | src/framework/di/composition_root.py |
| domain_init | __init__.py | code | src/domain/__init__.py |
| domain_init_utcnow | utcnow() | code | src/domain/__init__.py |
| entities_models_category | Category | code | src/domain/entities/models.py |
| entities_models_inventoryitem | InventoryItem | code | src/domain/entities/models.py |
| entities_models_inventoryitem_available | .available() | code | src/domain/entities/models.py |
| ... | ... (56 more nodes) | ... | ... |

### Community 2 (60 nodes, cohesion 0.108)

| Node | Label | Type | File |
|------|-------|------|------|
| controllers_api_transition_order_status | transition_order_status() | code | src/interface_adapters/controllers/api.py |
| dto_dtos_orderlineitemresponse | OrderLineItemResponse | code | src/application/dto/dtos.py |
| dto_dtos_orderresponse | OrderResponse | code | src/application/dto/dtos.py |
| dto_dtos_transitionorderstatusrequest | TransitionOrderStatusRequest | code | src/application/dto/dtos.py |
| entities_models_order | Order | code | src/domain/entities/models.py |
| entities_models_orderlineitem | OrderLineItem | code | src/domain/entities/models.py |
| events_events | events.py | code | src/domain/events/events.py |
| events_events_domainevent | DomainEvent | code | src/domain/events/events.py |
| events_events_lowstockalert | LowStockAlert | code | src/domain/events/events.py |
| events_events_ordercancelled | OrderCancelled | code | src/domain/events/events.py |
| events_events_orderplaced | OrderPlaced | code | src/domain/events/events.py |
| events_events_stockdepleted | StockDepleted | code | src/domain/events/events.py |
| events_simple_event_bus | simple_event_bus.py | code | src/infra/events/simple_event_bus.py |
| events_simple_event_bus_loggingeventbus | LoggingEventBus | code | src/infra/events/simple_event_bus.py |
| events_simple_event_bus_loggingeventbus_publish | .publish() | code | src/infra/events/simple_event_bus.py |
| ports_email_port | email_port.py | code | src/application/ports/email_port.py |
| ports_email_port_emailport | EmailPort | code | src/application/ports/email_port.py |
| ports_email_port_emailport_send_low_stock_alert | .send_low_stock_alert() | code | src/application/ports/email_port.py |
| ports_email_port_emailport_send_order_confirmation | .send_order_confirmation() | code | src/application/ports/email_port.py |
| ports_email_port_emailport_send_shipping_notification | .send_shipping_notification() | code | src/application/ports/email_port.py |
| ... | ... (40 more nodes) | ... | ... |

### Community 3 (52 nodes, cohesion 0.069)

| Node | Label | Type | File |
|------|-------|------|------|
| dataclasses | dataclasses |  |  |
| decimal | decimal |  |  |
| entities_models | models.py | code | src/domain/entities/models.py |
| entities_models_cartitem_line_total | .line_total() | code | src/domain/entities/models.py |
| entities_models_user | User | code | src/domain/entities/models.py |
| enum | Enum | code |  |
| ports_user_repository_userrepository | UserRepository | code | src/application/ports/user_repository.py |
| ports_user_repository_userrepository_create | .create() | code | src/application/ports/user_repository.py |
| ports_user_repository_userrepository_find_by_email | .find_by_email() | code | src/application/ports/user_repository.py |
| ports_user_repository_userrepository_find_by_id | .find_by_id() | code | src/application/ports/user_repository.py |
| re | re |  |  |
| repositories_user_repo | user_repo.py | code | src/infra/repositories/user_repo.py |
| repositories_user_repo_sqlalchemyuserrepository | SQLAlchemyUserRepository | code | src/infra/repositories/user_repo.py |
| repositories_user_repo_sqlalchemyuserrepository_create | .create() | code | src/infra/repositories/user_repo.py |
| repositories_user_repo_sqlalchemyuserrepository_find_by_email | .find_by_email() | code | src/infra/repositories/user_repo.py |
| repositories_user_repo_sqlalchemyuserrepository_find_by_id | .find_by_id() | code | src/infra/repositories/user_repo.py |
| repositories_user_repo_sqlalchemyuserrepository_init | .__init__() | code | src/infra/repositories/user_repo.py |
| repositories_user_repo_sqlalchemyuserrepository_to_domain | ._to_domain() | code | src/infra/repositories/user_repo.py |
| result_init | __init__.py | code | src/application/result/__init__.py |
| src_application_ports_user_repository | src_application_ports_user_repository |  |  |
| ... | ... (32 more nodes) | ... | ... |

### Community 4 (37 nodes, cohesion 0.102)

| Node | Label | Type | File |
|------|-------|------|------|
| controllers_api_clear_cart | clear_cart() | code | src/interface_adapters/controllers/api.py |
| controllers_api_get_cart | get_cart() | code | src/interface_adapters/controllers/api.py |
| controllers_api_remove_from_cart | remove_from_cart() | code | src/interface_adapters/controllers/api.py |
| db_models_cartitemmodel | CartItemModel | code | src/framework/db/models.py |
| db_models_cartmodel | CartModel | code | src/framework/db/models.py |
| entities_models_cart | Cart | code | src/domain/entities/models.py |
| ports_cart_repository_cartrepository | CartRepository | code | src/application/ports/cart_repository.py |
| ports_cart_repository_cartrepository_create | .create() | code | src/application/ports/cart_repository.py |
| ports_cart_repository_cartrepository_delete | .delete() | code | src/application/ports/cart_repository.py |
| ports_cart_repository_cartrepository_find_by_id | .find_by_id() | code | src/application/ports/cart_repository.py |
| ports_cart_repository_cartrepository_find_by_session_id | .find_by_session_id() | code | src/application/ports/cart_repository.py |
| ports_cart_repository_cartrepository_find_by_user_id | .find_by_user_id() | code | src/application/ports/cart_repository.py |
| ports_cart_repository_cartrepository_save | .save() | code | src/application/ports/cart_repository.py |
| repositories_cart_repo | cart_repo.py | code | src/infra/repositories/cart_repo.py |
| repositories_cart_repo_sqlalchemycartrepository | SQLAlchemyCartRepository | code | src/infra/repositories/cart_repo.py |
| repositories_cart_repo_sqlalchemycartrepository_create | .create() | code | src/infra/repositories/cart_repo.py |
| repositories_cart_repo_sqlalchemycartrepository_delete | .delete() | code | src/infra/repositories/cart_repo.py |
| repositories_cart_repo_sqlalchemycartrepository_find_by_id | .find_by_id() | code | src/infra/repositories/cart_repo.py |
| repositories_cart_repo_sqlalchemycartrepository_find_by_session_id | .find_by_session_id() | code | src/infra/repositories/cart_repo.py |
| repositories_cart_repo_sqlalchemycartrepository_find_by_user_id | .find_by_user_id() | code | src/infra/repositories/cart_repo.py |
| ... | ... (17 more nodes) | ... | ... |

### Community 5 (35 nodes, cohesion 0.064)

| Node | Label | Type | File |
|------|-------|------|------|
| alpinejs_frontend | Alpine.js | code | templates/base.html |
| changelog_doc | CHANGELOG.md | document | CHANGELOG.md |
| clean_architecture_pattern | Clean Architecture | document | README.md |
| csrf_middleware_concept | CSRF Middleware | document | CHANGELOG.md |
| docker_compose_config | docker-compose.yml | document | docker-compose.yml |
| double_submit_cookie_pattern | Double Submit Cookie Pattern | document | CHANGELOG.md |
| fastapi_framework | FastAPI | document | pyproject.toml |
| htmx_form_conversion | HTMX Form Conversion | document | session-ses_0ff1.md |
| htmx_frontend | HTMX | code | templates/base.html |
| http_basic_auth_docs | HTTP Basic Auth for Docs | document | part03-session-ses_1392.md |
| jinja2_templating | Jinja2 | document | pyproject.toml |
| jwt_authentication | JWT Authentication | document | CHANGELOG.md |
| mailpit_email | Mailpit | document | docker-compose.yml |
| openapi_tags_grouping | OpenAPI Tag Grouping | document | part03-session-ses_1392.md |
| opentelemetry_tracing | OpenTelemetry | document | pyproject.toml |
| part03_session_doc | part03-session-ses_1392.md | document | part03-session-ses_1392.md |
| pyproject_config | pyproject.toml | document | pyproject.toml |
| readme_doc | README.md | document | README.md |
| session_0ff1_doc | session-ses_0ff1.md | document | session-ses_0ff1.md |
| tailwindcss_frontend | Tailwind CSS | code | templates/base.html |
| ... | ... (15 more nodes) | ... | ... |

### Community 6 (35 nodes, cohesion 0.069)

| Node | Label | Type | File |
|------|-------|------|------|
| builder | builder |  |  |
| dependencyinjection | dependencyinjection |  |  |
| ecommerce_servicedefaults_extensions | Extensions.cs | code | aspire/ECommerce.ServiceDefaults/Extensions.cs |
| ecommerce_servicedefaults_extensions_extensions | Extensions | code | aspire/ECommerce.ServiceDefaults/Extensions.cs |
| ecommerce_servicedefaults_extensions_extensions_adddefaulthealthchecks | .AddDefaultHealthChecks() | code | aspire/ECommerce.ServiceDefaults/Extensions.cs |
| ecommerce_servicedefaults_extensions_extensions_addopentelemetryexporters | .AddOpenTelemetryExporters() | code | aspire/ECommerce.ServiceDefaults/Extensions.cs |
| ecommerce_servicedefaults_extensions_extensions_addservicedefaults | .AddServiceDefaults() | code | aspire/ECommerce.ServiceDefaults/Extensions.cs |
| ecommerce_servicedefaults_extensions_extensions_configureopentelemetry | .ConfigureOpenTelemetry() | code | aspire/ECommerce.ServiceDefaults/Extensions.cs |
| ecommerce_servicedefaults_extensions_extensions_mapdefaultendpoints | .MapDefaultEndpoints() | code | aspire/ECommerce.ServiceDefaults/Extensions.cs |
| framework_main | main.py | code | src/framework/main.py |
| healthchecks | healthchecks |  |  |
| logging | logging |  |  |
| metrics | metrics |  |  |
| opentelemetry | opentelemetry |  |  |
| opentelemetry_exporter_otlp_proto_grpc_log_exporter | opentelemetry_exporter_otlp_proto_grpc_log_exporter |  |  |
| opentelemetry_exporter_otlp_proto_grpc_metric_exporter | opentelemetry_exporter_otlp_proto_grpc_metric_exporter |  |  |
| opentelemetry_exporter_otlp_proto_grpc_trace_exporter | opentelemetry_exporter_otlp_proto_grpc_trace_exporter |  |  |
| opentelemetry_instrumentation_fastapi | opentelemetry_instrumentation_fastapi |  |  |
| opentelemetry_instrumentation_sqlalchemy | opentelemetry_instrumentation_sqlalchemy |  |  |
| opentelemetry_sdk_logs | opentelemetry_sdk_logs |  |  |
| ... | ... (15 more nodes) | ... | ... |

### Community 7 (34 nodes, cohesion 0.191)

| Node | Label | Type | File |
|------|-------|------|------|
| fastapi_responses | fastapi_responses |  |  |
| fastapi_templating | fastapi_templating |  |  |
| frontend_html_router | html_router.py | code | src/frontend/html_router.py |
| frontend_html_router_admin_create_category | admin_create_category() | code | src/frontend/html_router.py |
| frontend_html_router_admin_create_product | admin_create_product() | code | src/frontend/html_router.py |
| frontend_html_router_admin_dashboard | admin_dashboard() | code | src/frontend/html_router.py |
| frontend_html_router_admin_inventory | admin_inventory() | code | src/frontend/html_router.py |
| frontend_html_router_admin_orders | admin_orders() | code | src/frontend/html_router.py |
| frontend_html_router_admin_products | admin_products() | code | src/frontend/html_router.py |
| frontend_html_router_admin_restock | admin_restock() | code | src/frontend/html_router.py |
| frontend_html_router_admin_update_order_status | admin_update_order_status() | code | src/frontend/html_router.py |
| frontend_html_router_auth_check | _auth_check() | code | src/frontend/html_router.py |
| frontend_html_router_cart_add | cart_add() | code | src/frontend/html_router.py |
| frontend_html_router_cart_clear | cart_clear() | code | src/frontend/html_router.py |
| frontend_html_router_cart_page | cart_page() | code | src/frontend/html_router.py |
| frontend_html_router_cart_remove | cart_remove() | code | src/frontend/html_router.py |
| frontend_html_router_change_password_page | change_password_page() | code | src/frontend/html_router.py |
| frontend_html_router_change_password_post | change_password_post() | code | src/frontend/html_router.py |
| frontend_html_router_checkout | checkout() | code | src/frontend/html_router.py |
| frontend_html_router_get_session_user | get_session_user() | code | src/frontend/html_router.py |
| ... | ... (14 more nodes) | ... | ... |

### Community 8 (30 nodes, cohesion 0.140)

| Node | Label | Type | File |
|------|-------|------|------|
| e | E | code |  |
| pytest | pytest |  |  |
| result_init_result | Result | code | src/application/result/__init__.py |
| result_init_result_failure | .failure() | code | src/application/result/__init__.py |
| result_init_result_is_failure | .is_failure() | code | src/application/result/__init__.py |
| result_init_result_is_success | .is_success() | code | src/application/result/__init__.py |
| result_init_result_map | .map() | code | src/application/result/__init__.py |
| result_init_result_post_init | .__post_init__() | code | src/application/result/__init__.py |
| result_init_result_success | .success() | code | src/application/result/__init__.py |
| result_init_result_unwrap | .unwrap() | code | src/application/result/__init__.py |
| result_init_result_unwrap_error | .unwrap_error() | code | src/application/result/__init__.py |
| src_application_result | src_application_result |  |  |
| t | T | code |  |
| tests_test_result | test_result.py | code | tests/test_result.py |
| tests_test_result_test_failure_result | test_failure_result() | code | tests/test_result.py |
| tests_test_result_test_map_failure | test_map_failure() | code | tests/test_result.py |
| tests_test_result_test_map_success | test_map_success() | code | tests/test_result.py |
| tests_test_result_test_result_cannot_have_both | test_result_cannot_have_both() | code | tests/test_result.py |
| tests_test_result_test_result_must_have_one | test_result_must_have_one() | code | tests/test_result.py |
| tests_test_result_test_success_result | test_success_result() | code | tests/test_result.py |
| ... | ... (10 more nodes) | ... | ... |

### Community 9 (28 nodes, cohesion 0.103)

| Node | Label | Type | File |
|------|-------|------|------|
| auth_jwt_hash_password | hash_password() | code | src/framework/auth/jwt.py |
| base64 | base64 |  |  |
| db_session | session.py | code | src/framework/db/session.py |
| db_session_get_db | get_db() | code | src/framework/db/session.py |
| di_composition_root | composition_root.py | code | src/framework/di/composition_root.py |
| di_composition_root_create_app | create_app() | code | src/framework/di/composition_root.py |
| di_composition_root_seed_admin | seed_admin() | code | src/framework/di/composition_root.py |
| fastapi_middleware_cors | fastapi_middleware_cors |  |  |
| fastapi_testclient | fastapi_testclient |  |  |
| sqlalchemy | sqlalchemy |  |  |
| sqlalchemy_orm | SQLAlchemy | document | pyproject.toml |
| sqlalchemy_pool | sqlalchemy_pool |  |  |
| src_application_dto_dtos | src_application_dto_dtos |  |  |
| src_application_use_cases_auth_use_cases | src_application_use_cases_auth_use_cases |  |  |
| src_application_use_cases_cart_use_cases | src_application_use_cases_cart_use_cases |  |  |
| src_application_use_cases_inventory_use_cases | src_application_use_cases_inventory_use_cases |  |  |
| src_application_use_cases_order_use_cases | src_application_use_cases_order_use_cases |  |  |
| src_application_use_cases_product_use_cases | src_application_use_cases_product_use_cases |  |  |
| src_framework_auth_csrf | src_framework_auth_csrf |  |  |
| src_framework_auth_jwt | src_framework_auth_jwt |  |  |
| ... | ... (8 more nodes) | ... | ... |

### Community 10 (27 nodes, cohesion 0.123)

| Node | Label | Type | File |
|------|-------|------|------|
| auth_dependencies_require_admin | require_admin() | code | src/framework/auth/dependencies.py |
| controllers_api | api.py | code | src/interface_adapters/controllers/api.py |
| controllers_api_admin_list_orders | admin_list_orders() | code | src/interface_adapters/controllers/api.py |
| controllers_api_create_order | create_order() | code | src/interface_adapters/controllers/api.py |
| controllers_api_create_product | create_product() | code | src/interface_adapters/controllers/api.py |
| controllers_api_delete_product | delete_product() | code | src/interface_adapters/controllers/api.py |
| controllers_api_get_order | get_order() | code | src/interface_adapters/controllers/api.py |
| controllers_api_get_product | get_product() | code | src/interface_adapters/controllers/api.py |
| controllers_api_health | health() | code | src/interface_adapters/controllers/api.py |
| controllers_api_list_orders | list_orders() | code | src/interface_adapters/controllers/api.py |
| controllers_api_list_products | list_products() | code | src/interface_adapters/controllers/api.py |
| controllers_api_me | me() | code | src/interface_adapters/controllers/api.py |
| controllers_api_merge_cart | merge_cart() | code | src/interface_adapters/controllers/api.py |
| controllers_api_update_product | update_product() | code | src/interface_adapters/controllers/api.py |
| db_models_usermodel | UserModel | code | src/framework/db/models.py |
| dto_dtos_userresponse | UserResponse | code | src/application/dto/dtos.py |
| repositories_product_repo_sqlalchemyproductrepository | SQLAlchemyProductRepository | code | src/infra/repositories/product_repo.py |
| repositories_product_repo_sqlalchemyproductrepository_init | .__init__() | code | src/infra/repositories/product_repo.py |
| repositories_product_repo_sqlalchemyproductrepository_update | .update() | code | src/infra/repositories/product_repo.py |
| src_framework_auth_dependencies | src_framework_auth_dependencies |  |  |
| ... | ... (7 more nodes) | ... | ... |

### Community 11 (21 nodes, cohesion 0.124)

| Node | Label | Type | File |
|------|-------|------|------|
| properties_launchsettings | launchSettings.json | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_environmentvariables_aspire_allow_unsecured_transport | ASPIRE_ALLOW_UNSECURED_TRANSPORT | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_environmentvariables_aspire_dashboard_otlp_endpoint_url | ASPIRE_DASHBOARD_OTLP_ENDPOINT_URL | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_environmentvariables_aspire_resource_service_endpoint_url | ASPIRE_RESOURCE_SERVICE_ENDPOINT_URL | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_environmentvariables_aspnetcore_environment | ASPNETCORE_ENVIRONMENT | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_environmentvariables_dotnet_dashboard_otlp_api_key | DOTNET_DASHBOARD_OTLP_API_KEY | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_environmentvariables_dotnet_environment | DOTNET_ENVIRONMENT | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_http_applicationurl | applicationUrl | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_http_commandname | commandName | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_http_dotnetrunmessages | dotnetRunMessages | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_http_environmentvariables | environmentVariables | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_http_launchbrowser | launchBrowser | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_https_applicationurl | applicationUrl | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_https_commandname | commandName | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_https_dotnetrunmessages | dotnetRunMessages | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_https_environmentvariables | environmentVariables | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_https_launchbrowser | launchBrowser | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_profiles | profiles | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_profiles_http | http | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| properties_launchsettings_profiles_https | https | code | aspire/ECommerce.AppHost/Properties/launchSettings.json |
| ... | ... (1 more nodes) | ... | ... |

### Community 12 (17 nodes, cohesion 0.118)

| Node | Label | Type | File |
|------|-------|------|------|
| pkg_alembic | pkg_alembic |  |  |
| pkg_ecommerce_api | ecommerce-api | code | pyproject.toml |
| pkg_fastapi | pkg_fastapi |  |  |
| pkg_httpx | pkg_httpx |  |  |
| pkg_jinja2 | pkg_jinja2 |  |  |
| pkg_opentelemetry_api | pkg_opentelemetry_api |  |  |
| pkg_opentelemetry_exporter_otlp | pkg_opentelemetry_exporter_otlp |  |  |
| pkg_opentelemetry_instrumentation_fastapi | pkg_opentelemetry_instrumentation_fastapi |  |  |
| pkg_opentelemetry_instrumentation_sqlalchemy | pkg_opentelemetry_instrumentation_sqlalchemy |  |  |
| pkg_opentelemetry_sdk | pkg_opentelemetry_sdk |  |  |
| pkg_passlib | pkg_passlib |  |  |
| pkg_pydantic | pkg_pydantic |  |  |
| pkg_pydantic_settings | pkg_pydantic_settings |  |  |
| pkg_python_jose | pkg_python_jose |  |  |
| pkg_python_multipart | pkg_python_multipart |  |  |
| pkg_sqlalchemy | pkg_sqlalchemy |  |  |
| pkg_uvicorn | pkg_uvicorn |  |  |

### Community 13 (14 nodes, cohesion 0.143)

| Node | Label | Type | File |
|------|-------|------|------|
| aspire_ecommerce | ECommerce.slnx | code | aspire/ECommerce.slnx |
| aspire_ecommerce_apphost_ecommerce_apphost_csproj_framework_net10_0 | net10.0 | concept | aspire/ECommerce.AppHost/ECommerce.AppHost.csproj |
| aspire_ecommerce_servicedefaults_ecommerce_servicedefaults_csproj_framework_net10_0 | net10.0 | concept | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| ecommerce_apphost_ecommerce_apphost | ECommerce.AppHost.csproj | code | aspire/ECommerce.AppHost/ECommerce.AppHost.csproj |
| ecommerce_servicedefaults_ecommerce_servicedefaults | ECommerce.ServiceDefaults.csproj | code | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| nuget_microsoft_extensions_http_resilience | Microsoft.Extensions.Http.Resilience (10.7.0) | code | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| nuget_microsoft_extensions_servicediscovery | Microsoft.Extensions.ServiceDiscovery (10.7.0) | code | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| nuget_opentelemetry_exporter_opentelemetryprotocol | OpenTelemetry.Exporter.OpenTelemetryProtocol (1.16.0) | code | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| nuget_opentelemetry_extensions_hosting | OpenTelemetry.Extensions.Hosting (1.16.0) | code | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| nuget_opentelemetry_instrumentation_aspnetcore | OpenTelemetry.Instrumentation.AspNetCore (1.16.0) | code | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| nuget_opentelemetry_instrumentation_http | OpenTelemetry.Instrumentation.Http (1.16.0) | code | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| nuget_opentelemetry_instrumentation_runtime | OpenTelemetry.Instrumentation.Runtime (1.15.1) | code | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |
| sdk_aspire_apphost_sdk_13_4_6 | Aspire.AppHost.Sdk/13.4.6 | concept | aspire/ECommerce.AppHost/ECommerce.AppHost.csproj |
| sdk_microsoft_net_sdk | Microsoft.NET.Sdk | concept | aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj |

### Community 14 (12 nodes, cohesion 0.182)

| Node | Label | Type | File |
|------|-------|------|------|
| alembic | alembic |  |  |
| alembic_env | env.py | code | alembic/env.py |
| alembic_env_run_migrations_offline | run_migrations_offline() | code | alembic/env.py |
| alembic_env_run_migrations_online | run_migrations_online() | code | alembic/env.py |
| logging_config | logging_config |  |  |
| typing | typing |  |  |
| versions_0efd7a183e11_use_numeric_for_money_columns | 0efd7a183e11_use_numeric_for_money_columns.py | code | alembic/versions/0efd7a183e11_use_numeric_for_money_columns.py |
| versions_0efd7a183e11_use_numeric_for_money_columns_downgrade | downgrade() | code | alembic/versions/0efd7a183e11_use_numeric_for_money_columns.py |
| versions_0efd7a183e11_use_numeric_for_money_columns_upgrade | upgrade() | code | alembic/versions/0efd7a183e11_use_numeric_for_money_columns.py |
| versions_b6c8a5ea7783_initial_schema | b6c8a5ea7783_initial_schema.py | code | alembic/versions/b6c8a5ea7783_initial_schema.py |
| versions_b6c8a5ea7783_initial_schema_downgrade | downgrade() | code | alembic/versions/b6c8a5ea7783_initial_schema.py |
| versions_b6c8a5ea7783_initial_schema_upgrade | upgrade() | code | alembic/versions/b6c8a5ea7783_initial_schema.py |

### Community 15 (12 nodes, cohesion 0.303)

| Node | Label | Type | File |
|------|-------|------|------|
| auth_dependencies | dependencies.py | code | src/framework/auth/dependencies.py |
| auth_dependencies_get_current_user | get_current_user() | code | src/framework/auth/dependencies.py |
| auth_dependencies_optional_user | optional_user() | code | src/framework/auth/dependencies.py |
| auth_dependencies_resolve_user | _resolve_user() | code | src/framework/auth/dependencies.py |
| auth_jwt | jwt.py | code | src/framework/auth/jwt.py |
| auth_jwt_decode_token | decode_token() | code | src/framework/auth/jwt.py |
| auth_jwt_verify_password | verify_password() | code | src/framework/auth/jwt.py |
| bcrypt | bcrypt |  |  |
| fastapi_security | fastapi_security |  |  |
| httpauthorizationcredentials | HTTPAuthorizationCredentials | code |  |
| jose | jose |  |  |
| src_framework_db_session | src_framework_db_session |  |  |

### Community 16 (9 nodes, cohesion 0.278)

| Node | Label | Type | File |
|------|-------|------|------|
| auth_csrf | csrf.py | code | src/framework/auth/csrf.py |
| auth_csrf_csrfmiddleware_dispatch | .dispatch() | code | src/framework/auth/csrf.py |
| auth_csrf_generate_token | _generate_token() | code | src/framework/auth/csrf.py |
| auth_csrf_get_cookie_token | _get_cookie_token() | code | src/framework/auth/csrf.py |
| auth_csrf_get_header_token | _get_header_token() | code | src/framework/auth/csrf.py |
| secrets | secrets |  |  |
| starlette_middleware_base | starlette_middleware_base |  |  |
| starlette_requests | starlette_requests |  |  |
| starlette_responses | starlette_responses |  |  |

### Community 17 (8 nodes, cohesion 0.357)

| Node | Label | Type | File |
|------|-------|------|------|
| email_mailpit_adapter | mailpit_adapter.py | code | src/infra/email/mailpit_adapter.py |
| email_mailpit_adapter_mailpitemailadapter | MailpitEmailAdapter | code | src/infra/email/mailpit_adapter.py |
| email_mailpit_adapter_mailpitemailadapter_send | ._send() | code | src/infra/email/mailpit_adapter.py |
| email_mailpit_adapter_mailpitemailadapter_send_low_stock_alert | .send_low_stock_alert() | code | src/infra/email/mailpit_adapter.py |
| email_mailpit_adapter_mailpitemailadapter_send_order_confirmation | .send_order_confirmation() | code | src/infra/email/mailpit_adapter.py |
| email_mailpit_adapter_mailpitemailadapter_send_shipping_notification | .send_shipping_notification() | code | src/infra/email/mailpit_adapter.py |
| httpx | httpx |  |  |
| src_application_ports_email_port | src_application_ports_email_port |  |  |

### Community 18 (6 nodes, cohesion 0.533)

| Node | Label | Type | File |
|------|-------|------|------|
| auth_jwt_create_access_token | create_access_token() | code | src/framework/auth/jwt.py |
| auth_jwt_create_refresh_token | create_refresh_token() | code | src/framework/auth/jwt.py |
| controllers_api_login | login() | code | src/interface_adapters/controllers/api.py |
| controllers_api_refresh | refresh() | code | src/interface_adapters/controllers/api.py |
| dto_dtos_tokenresponse | TokenResponse | code | src/application/dto/dtos.py |
| response | Response | code |  |

### Community 19 (3 nodes, cohesion 0.667)

| Node | Label | Type | File |
|------|-------|------|------|
| framework_otel_wrapper | otel_wrapper.sh | code | src/framework/otel_wrapper.sh |
| framework_otel_wrapper_otel_exporter_otlp_endpoint | OTEL_EXPORTER_OTLP_ENDPOINT | code | src/framework/otel_wrapper.sh |
| media_jsoques_data_projects_learning_ai_assisted_coding_src_framework_otel_wrapper_sh__entry | otel_wrapper.sh script | code | src/framework/otel_wrapper.sh |

### Community 20 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| application_init | __init__.py | code | src/application/__init__.py |

### Community 21 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| appsettings_config | appsettings.json | document | aspire/ECommerce.AppHost/appsettings.json |

### Community 22 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| appsettings_dev_config | appsettings.Development.json | document | aspire/ECommerce.AppHost/appsettings.Development.json |

### Community 23 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| aspire_config | aspire.config.json | document | aspire/ECommerce.AppHost/aspire.config.json |

### Community 24 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| auth_init | __init__.py | code | src/framework/auth/__init__.py |

### Community 25 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| controllers_init | __init__.py | code | src/interface_adapters/controllers/__init__.py |

### Community 26 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| db_init | __init__.py | code | src/framework/db/__init__.py |

### Community 27 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| di_init | __init__.py | code | src/framework/di/__init__.py |

### Community 28 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| dto_init | __init__.py | code | src/application/dto/__init__.py |

### Community 29 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| ecommerce_apphost_apphost | AppHost.cs | code | aspire/ECommerce.AppHost/AppHost.cs |

### Community 30 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| entities_init | __init__.py | code | src/domain/entities/__init__.py |

### Community 31 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| framework_init | __init__.py | code | src/framework/__init__.py |

### Community 32 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| infra_init | __init__.py | code | src/infra/__init__.py |

### Community 33 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| interface_adapters_init | __init__.py | code | src/interface_adapters/__init__.py |

### Community 34 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| launch_settings_config | launchSettings.json | document | aspire/ECommerce.AppHost/Properties/launchSettings.json |

### Community 35 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| ports_init | __init__.py | code | src/application/ports/__init__.py |

### Community 36 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| serializers_init | __init__.py | code | src/interface_adapters/serializers/__init__.py |

### Community 37 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| src_domain_events_init_py_events_init | __init__.py | code | src/domain/events/__init__.py |

### Community 38 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| src_infra_events_init_py_events_init | __init__.py | code | src/infra/events/__init__.py |

### Community 39 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| src_init | __init__.py | code | src/__init__.py |

### Community 40 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| tests_init | __init__.py | code | tests/__init__.py |

### Community 41 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| use_cases_init | __init__.py | code | src/application/use_cases/__init__.py |

### Community 42 (1 nodes, cohesion 1.000)

| Node | Label | Type | File |
|------|-------|------|------|
| value_objects_init | __init__.py | code | src/domain/value_objects/__init__.py |

## File Index

- **CHANGELOG.md**: CHANGELOG.md, Double Submit Cookie Pattern, JWT Authentication, CSRF Middleware
- **README.md**: README.md, Clean Architecture
- **alembic/env.py**: env.py, run_migrations_offline(), run_migrations_online()
- **alembic/versions/0efd7a183e11_use_numeric_for_money_columns.py**: 0efd7a183e11_use_numeric_for_money_columns.py, upgrade(), downgrade()
- **alembic/versions/b6c8a5ea7783_initial_schema.py**: b6c8a5ea7783_initial_schema.py, upgrade(), downgrade()
- **aspire/ECommerce.AppHost/AppHost.cs**: AppHost.cs
- **aspire/ECommerce.AppHost/ECommerce.AppHost.csproj**: ECommerce.AppHost.csproj, net10.0, Aspire.AppHost.Sdk/13.4.6
- **aspire/ECommerce.AppHost/Properties/launchSettings.json**: launchSettings.json, $schema, profiles, https, commandName...
- **aspire/ECommerce.AppHost/appsettings.Development.json**: appsettings.Development.json
- **aspire/ECommerce.AppHost/appsettings.json**: appsettings.json
- **aspire/ECommerce.AppHost/aspire.config.json**: aspire.config.json
- **aspire/ECommerce.ServiceDefaults/ECommerce.ServiceDefaults.csproj**: ECommerce.ServiceDefaults.csproj, net10.0, Microsoft.Extensions.Http.Resilience (10.7.0), Microsoft.Extensions.ServiceDiscovery (10.7.0), OpenTelemetry.Exporter.OpenTelemetryProtocol (1.16.0)...
- **aspire/ECommerce.ServiceDefaults/Extensions.cs**: Extensions.cs, Extensions, .AddServiceDefaults(), .ConfigureOpenTelemetry(), .AddOpenTelemetryExporters()...
- **aspire/ECommerce.slnx**: ECommerce.slnx
- **docker-compose.yml**: docker-compose.yml, Mailpit
- **part03-session-ses_1392.md**: part03-session-ses_1392.md, HTTP Basic Auth for Docs, OpenAPI Tag Grouping
- **pyproject.toml**: ecommerce-api, pyproject.toml, FastAPI, SQLAlchemy, Jinja2...
- **session-ses_0ff1.md**: session-ses_0ff1.md, HTMX Form Conversion
- **src/__init__.py**: __init__.py
- **src/application/__init__.py**: __init__.py
- **src/application/dto/__init__.py**: __init__.py
- **src/application/dto/dtos.py**: dtos.py, RegisterUserRequest, LoginRequest, TokenResponse, UserResponse...
- **src/application/ports/__init__.py**: __init__.py
- **src/application/ports/cart_repository.py**: cart_repository.py, CartRepository, .create(), .find_by_id(), .find_by_user_id()...
- **src/application/ports/email_port.py**: email_port.py, EmailPort, .send_order_confirmation(), .send_shipping_notification(), .send_low_stock_alert()
- **src/application/ports/event_bus.py**: event_bus.py, EventBus, .publish()
- **src/application/ports/inventory_repository.py**: inventory_repository.py, InventoryRepository, .find_by_product_id(), .save(), .reserve()...
- **src/application/ports/order_repository.py**: order_repository.py, OrderRepository, .create(), .find_by_id(), .find_by_user_id()...
- **src/application/ports/product_repository.py**: product_repository.py, ProductRepository, .create(), .find_by_id(), .find_by_sku()...
- **src/application/ports/user_repository.py**: user_repository.py, UserRepository, .create(), .find_by_email(), .find_by_id()
- **src/application/result/__init__.py**: __init__.py, Result, .__post_init__(), .success(), .failure()...
- **src/application/use_cases/__init__.py**: __init__.py
- **src/application/use_cases/auth_use_cases.py**: auth_use_cases.py, RegisterUserUseCase, .__init__(), .execute(), AuthenticateUserUseCase...
- **src/application/use_cases/cart_use_cases.py**: cart_use_cases.py, AddToCartUseCase, .__init__(), .execute(), ._cart_to_response()...
- **src/application/use_cases/inventory_use_cases.py**: inventory_use_cases.py, CheckInventoryUseCase, .__init__(), .execute(), RecordRestockUseCase...
- **src/application/use_cases/order_use_cases.py**: order_use_cases.py, CreateOrderUseCase, .__init__(), .execute(), ._to_response()...
- **src/application/use_cases/product_use_cases.py**: product_use_cases.py, CreateProductUseCase, .__init__(), .execute(), ._to_response()...
- **src/domain/__init__.py**: __init__.py, utcnow()
- **src/domain/entities/__init__.py**: __init__.py
- **src/domain/entities/models.py**: models.py, User, Category, Product, CartItem...
- **src/domain/events/__init__.py**: __init__.py
- **src/domain/events/events.py**: events.py, DomainEvent, OrderPlaced, OrderCancelled, StockDepleted...
- **src/domain/value_objects/__init__.py**: __init__.py
- **src/domain/value_objects/common.py**: common.py, Money, .__post_init__(), .__add__(), .__mul__()...
- **src/framework/__init__.py**: __init__.py
- **src/framework/auth/__init__.py**: __init__.py
- **src/framework/auth/csrf.py**: csrf.py, _generate_token(), _get_cookie_token(), _get_header_token(), CSRFMiddleware...
- **src/framework/auth/dependencies.py**: dependencies.py, _resolve_user(), get_current_user(), require_admin(), optional_user()
- **src/framework/auth/jwt.py**: jwt.py, create_access_token(), create_refresh_token(), decode_token(), hash_password()...
- **src/framework/db/__init__.py**: __init__.py
- **src/framework/db/models.py**: models.py, _utcnow(), UserModel, CategoryModel, ProductModel...
- **src/framework/db/session.py**: session.py, get_db()
- **src/framework/di/__init__.py**: __init__.py
- **src/framework/di/composition_root.py**: composition_root.py, seed_admin(), seed_products(), create_app()
- **src/framework/main.py**: main.py
- **src/framework/otel_wrapper.sh**: otel_wrapper.sh, otel_wrapper.sh script, OTEL_EXPORTER_OTLP_ENDPOINT
- **src/frontend/html_router.py**: html_router.py, get_session_user(), login_page(), login_post(), register_page()...
- **src/infra/__init__.py**: __init__.py
- **src/infra/email/mailpit_adapter.py**: mailpit_adapter.py, MailpitEmailAdapter, .send_order_confirmation(), .send_shipping_notification(), .send_low_stock_alert()...
- **src/infra/events/__init__.py**: __init__.py
- **src/infra/events/simple_event_bus.py**: simple_event_bus.py, LoggingEventBus, .publish()
- **src/infra/repositories/cart_repo.py**: cart_repo.py, SQLAlchemyCartRepository, .__init__(), ._load_cart(), .create()...
- **src/infra/repositories/inventory_repo.py**: inventory_repo.py, SQLAlchemyInventoryRepository, .__init__(), .find_by_product_id(), .save()...
- **src/infra/repositories/order_repo.py**: order_repo.py, SQLAlchemyOrderRepository, .__init__(), ._query(), .create()...
- **src/infra/repositories/product_repo.py**: product_repo.py, SQLAlchemyProductRepository, .__init__(), .create(), .find_by_id()...
- **src/infra/repositories/user_repo.py**: user_repo.py, SQLAlchemyUserRepository, .__init__(), .create(), .find_by_email()...
- **src/interface_adapters/__init__.py**: __init__.py
- **src/interface_adapters/controllers/__init__.py**: __init__.py
- **src/interface_adapters/controllers/api.py**: api.py, health(), register(), login(), refresh()...
- **src/interface_adapters/serializers/__init__.py**: __init__.py
- **templates/admin/dashboard.html**: templates/admin/dashboard.html
- **templates/admin/inventory.html**: templates/admin/inventory.html
- **templates/admin/orders.html**: templates/admin/orders.html
- **templates/admin/products.html**: templates/admin/products.html
- **templates/auth/login.html**: templates/auth/login.html
- **templates/auth/profile.html**: templates/auth/profile.html
- **templates/auth/register.html**: templates/auth/register.html
- **templates/base.html**: templates/base.html, HTMX, Alpine.js, Tailwind CSS
- **templates/cart/cart.html**: templates/cart/cart.html
- **templates/index.html**: templates/index.html
- **templates/orders/detail.html**: templates/orders/detail.html
- **templates/orders/history.html**: templates/orders/history.html
- **templates/products/_list_items.html**: templates/products/_list_items.html
- **templates/products/detail.html**: templates/products/detail.html
- **templates/products/list.html**: templates/products/list.html
- **tests/__init__.py**: __init__.py
- **tests/test_api.py**: test_api.py, db_session(), client(), admin_token(), TestHealthEndpoint...
- **tests/test_result.py**: test_result.py, test_success_result(), test_failure_result(), test_result_cannot_have_both(), test_result_must_have_one()...
- **tests/test_use_cases.py**: test_use_cases.py, user(), admin(), category(), product()...
- **tests/test_value_objects.py**: test_value_objects.py, TestMoney, .test_create(), .test_negative_amount_raises(), .test_addition()...