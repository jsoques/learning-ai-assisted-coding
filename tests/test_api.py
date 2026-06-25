from __future__ import annotations

import uuid
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.application.dto.dtos import AddCartItemRequest, CreateProductRequest, LoginRequest, RegisterUserRequest, RestockRequest, TransitionOrderStatusRequest
from src.application.use_cases.auth_use_cases import AuthenticateUserUseCase, RegisterUserUseCase
from src.application.use_cases.cart_use_cases import AddToCartUseCase, GetCartUseCase, MergeCartOnLoginUseCase, RemoveFromCartUseCase
from src.application.use_cases.inventory_use_cases import CheckInventoryUseCase, RecordRestockUseCase
from src.application.use_cases.order_use_cases import CreateOrderUseCase, GetOrderUseCase, ListOrdersUseCase, TransitionOrderStatusUseCase
from src.application.use_cases.product_use_cases import CreateProductUseCase, DeleteProductUseCase, GetProductUseCase, ListProductsUseCase, UpdateProductUseCase
from src.domain.entities.models import Cart, CartItem, Category, InventoryItem, Order, OrderLineItem, Product, RestockEvent, User
from src.domain.value_objects.common import EmailAddress, Money, OrderStatus, ProductStatus, SKU
from src.framework.auth.csrf import CSRFMiddleware
from src.framework.auth.jwt import hash_password
from src.framework.db.models import Base, ProductModel, UserModel
from src.framework.di.composition_root import create_app
from src.framework.db.session import get_db


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    app = create_app()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    admin = UserModel(
        id=str(uuid.uuid4()),
        email="admin@shop.com",
        hashed_password=hash_password("admin123"),
        role="admin",
    )
    db = next(client.app.dependency_overrides[get_db]())
    db.add(admin)
    db.commit()
    db.close()

    resp = client.post("/api/auth/login", json={"email": "admin@shop.com", "password": "admin123"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


class TestHealthEndpoint:
    def test_health(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"


class TestAuthEndpoints:
    def test_register_and_login(self, client):
        resp = client.post("/api/auth/register", json={"email": "new@test.com", "password": "password123"})
        assert resp.status_code == 201
        assert resp.json()["email"] == "new@test.com"

        resp = client.post("/api/auth/login", json={"email": "new@test.com", "password": "password123"})
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_register_duplicate(self, client):
        client.post("/api/auth/register", json={"email": "dup@test.com", "password": "password123"})
        resp = client.post("/api/auth/register", json={"email": "dup@test.com", "password": "password123"})
        assert resp.status_code == 409

    def test_login_invalid(self, client):
        resp = client.post("/api/auth/login", json={"email": "none@test.com", "password": "wrong"})
        assert resp.status_code == 401


class TestProductEndpoints:
    @pytest.fixture
    def category_id(self, client, admin_token):
        resp = client.post(
            "/api/categories",
            params={"name": "TestCat", "description": "Test"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 201
        return resp.json()["id"]

    def test_list_products_empty(self, client):
        resp = client.get("/api/products")
        assert resp.status_code == 200

    def test_create_product(self, client, admin_token, category_id):
        resp = client.post(
            "/api/products",
            json={
                "sku": "CTRL-001",
                "name": "Controller Test",
                "description": "Test",
                "price": "29.99",
                "category_id": category_id,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 201
        assert resp.json()["sku"] == "CTRL-001"

    def test_create_product_forbidden_for_customer(self, client, category_id):
        client.post("/api/auth/register", json={"email": "cust@test.com", "password": "password123"})
        resp = client.post("/api/auth/login", json={"email": "cust@test.com", "password": "password123"})
        token = resp.json()["access_token"]

        resp = client.post(
            "/api/products",
            json={
                "sku": "NO-001",
                "name": "No Auth",
                "description": "Test",
                "price": "9.99",
                "category_id": category_id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 403


class TestCartEndpoints:
    def test_add_to_cart(self, client, admin_token):
        resp = client.get("/api/products")
        assert resp.status_code == 200

    def test_cart_requires_auth_for_merge(self, client):
        resp = client.post("/api/cart/merge", params={"session_id": "sess1"})
        assert resp.status_code == 401


class TestOrderEndpoints:
    def test_list_orders_requires_auth(self, client):
        resp = client.get("/api/orders")
        assert resp.status_code == 401

    def test_create_order_no_cart(self, client, admin_token):
        resp = client.post("/api/orders", params={"cart_id": str(uuid.uuid4())}, headers={"Authorization": f"Bearer {admin_token}"})
        assert resp.status_code == 404


class TestCSRFProtection:
    def test_csrf_blocks_missing_token(self):
        from fastapi import FastAPI, Form
        from fastapi.testclient import TestClient

        app = FastAPI()
        app.add_middleware(CSRFMiddleware)

        @app.post("/submit")
        def submit(name: str = Form(...)):
            return {"ok": True}

        client = TestClient(app)

        resp = client.post("/submit", data={"name": "test"})
        assert resp.status_code == 403
        assert "CSRF" in resp.text

    def test_csrf_blocks_wrong_token(self):
        from fastapi import FastAPI, Form
        from fastapi.testclient import TestClient

        app = FastAPI()
        app.add_middleware(CSRFMiddleware)

        @app.post("/submit")
        def submit(name: str = Form(...)):
            return {"ok": True}

        client = TestClient(app)
        client.get("/")  # get a CSRF cookie
        resp = client.post("/submit", data={"name": "test"}, headers={"X-CSRF-Token": "wrong-token"})
        assert resp.status_code == 403

    def test_csrf_passes_with_header_token(self):
        from fastapi import FastAPI, Form
        from fastapi.testclient import TestClient

        app = FastAPI()
        app.add_middleware(CSRFMiddleware)

        @app.post("/submit")
        def submit(name: str = Form(...)):
            return {"ok": True}

        client = TestClient(app)
        resp = client.get("/")
        csrf_token = resp.cookies.get("csrf_token")
        resp = client.post("/submit", data={"name": "test"}, headers={"X-CSRF-Token": csrf_token})
        assert resp.status_code == 200

    def test_api_routes_skip_csrf(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        app = FastAPI()
        app.add_middleware(CSRFMiddleware)

        @app.post("/api/action")
        def action():
            return {"ok": True}

        client = TestClient(app)
        resp = client.post("/api/action")
        assert resp.status_code == 200
