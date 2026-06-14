from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

import pytest

from src.application.dto.dtos import (
    AddCartItemRequest,
    CreateProductRequest,
    LoginRequest,
    RegisterUserRequest,
    RestockRequest,
    TransitionOrderStatusRequest,
    UpdateProductRequest,
)
from src.application.ports.cart_repository import CartRepository
from src.application.ports.email_port import EmailPort
from src.application.ports.inventory_repository import InventoryRepository
from src.application.ports.order_repository import OrderRepository
from src.application.ports.product_repository import CategoryRepository, ProductRepository
from src.application.ports.user_repository import UserRepository
from src.application.use_cases.auth_use_cases import AuthenticateUserUseCase, RegisterUserUseCase
from src.application.use_cases.cart_use_cases import AddToCartUseCase, GetCartUseCase, MergeCartOnLoginUseCase, RemoveFromCartUseCase
from src.application.use_cases.inventory_use_cases import CheckInventoryUseCase, RecordRestockUseCase
from src.application.use_cases.order_use_cases import CreateOrderUseCase, GetOrderUseCase, ListOrdersUseCase, TransitionOrderStatusUseCase
from src.application.use_cases.product_use_cases import CreateProductUseCase, DeleteProductUseCase, GetProductUseCase, ListProductsUseCase, UpdateProductUseCase
from src.domain.entities.models import Cart, CartItem, Category, InventoryItem, Order, OrderLineItem, Product, RestockEvent, User
from src.domain.value_objects.common import EmailAddress, Money, OrderStatus, ProductStatus, SKU


@pytest.fixture
def user() -> User:
    return User(
        id=uuid.uuid4(),
        email=EmailAddress("test@example.com"),
        hashed_password="hashedpass",
        role="customer",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def admin() -> User:
    return User(
        id=uuid.uuid4(),
        email=EmailAddress("admin@example.com"),
        hashed_password="hashedpass",
        role="admin",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def category() -> Category:
    return Category(id=uuid.uuid4(), name="Test", description="Test category")


@pytest.fixture
def product(category: Category) -> Product:
    return Product(
        id=uuid.uuid4(),
        sku=SKU("TST-001"),
        name="Test Product",
        description="A test product",
        price=Money(Decimal("19.99")),
        category_id=category.id,
        status=ProductStatus.ACTIVE,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def inventory(product: Product) -> InventoryItem:
    return InventoryItem(
        product_id=product.id,
        on_hand=100,
        reserved=0,
        low_stock_threshold=5,
    )


class InMemoryUserRepo(UserRepository):
    def __init__(self):
        self._users: dict[str, User] = {}

    def create(self, user: User) -> User:
        self._users[str(user.id)] = user
        return user

    def find_by_email(self, email: str) -> User | None:
        return next((u for u in self._users.values() if str(u.email) == email), None)

    def find_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._users.get(str(user_id))


class InMemoryProductRepo(ProductRepository):
    def __init__(self):
        self._products: dict[str, Product] = {}

    def create(self, product: Product) -> Product:
        self._products[str(product.id)] = product
        return product

    def find_by_id(self, product_id: uuid.UUID) -> Product | None:
        return self._products.get(str(product_id))

    def find_by_sku(self, sku: str) -> Product | None:
        return next((p for p in self._products.values() if p.sku == sku), None)

    def search(self, query=None, category_id=None, price_min=None, price_max=None, page=1, per_page=20):
        results = list(self._products.values())
        if query:
            results = [p for p in results if query.lower() in p.name.lower()]
        total = len(results)
        return results[(page - 1) * per_page : page * per_page], total

    def update(self, product: Product) -> Product:
        self._products[str(product.id)] = product
        return product

    def soft_delete(self, product_id: uuid.UUID) -> None:
        p = self._products.get(str(product_id))
        if p:
            p.status = ProductStatus.INACTIVE


class InMemoryCategoryRepo(CategoryRepository):
    def __init__(self):
        self._categories: dict[str, Category] = {}

    def create(self, category: Category) -> Category:
        self._categories[str(category.id)] = category
        return category

    def list_all(self) -> list[Category]:
        return list(self._categories.values())

    def find_by_id(self, category_id: uuid.UUID) -> Category | None:
        return self._categories.get(str(category_id))

    def update(self, category: Category) -> Category:
        self._categories[str(category.id)] = category
        return category


class InMemoryCartRepo(CartRepository):
    def __init__(self):
        self._carts: dict[str, Cart] = {}

    def create(self, cart: Cart) -> Cart:
        self._carts[str(cart.id)] = cart
        return cart

    def find_by_id(self, cart_id: uuid.UUID) -> Cart | None:
        return self._carts.get(str(cart_id))

    def find_by_user_id(self, user_id: uuid.UUID) -> Cart | None:
        return next((c for c in self._carts.values() if c.user_id == user_id), None)

    def find_by_session_id(self, session_id: str) -> Cart | None:
        return next((c for c in self._carts.values() if c.session_id == session_id), None)

    def save(self, cart: Cart) -> None:
        self._carts[str(cart.id)] = cart

    def delete(self, cart_id: uuid.UUID) -> None:
        self._carts.pop(str(cart_id), None)


class InMemoryOrderRepo(OrderRepository):
    def __init__(self):
        self._orders: dict[str, Order] = {}

    def create(self, order: Order) -> Order:
        self._orders[str(order.id)] = order
        return order

    def find_by_id(self, order_id: uuid.UUID) -> Order | None:
        return self._orders.get(str(order_id))

    def find_by_user_id(self, user_id, status=None, page=1, per_page=20):
        results = [o for o in self._orders.values() if o.user_id == user_id]
        if status:
            results = [o for o in results if o.status.value == status]
        results.sort(key=lambda o: o.created_at, reverse=True)
        total = len(results)
        return results[(page - 1) * per_page : page * per_page], total

    def update_status(self, order_id, status):
        o = self._orders.get(str(order_id))
        if o:
            o.status = OrderStatus(status)
        return o

    def list_all(self, status=None, page=1, per_page=20):
        results = list(self._orders.values())
        if status:
            results = [o for o in results if o.status.value == status]
        results.sort(key=lambda o: o.created_at, reverse=True)
        total = len(results)
        return results[(page - 1) * per_page : page * per_page], total


class InMemoryInventoryRepo(InventoryRepository):
    def __init__(self):
        self._items: dict[str, InventoryItem] = {}

    def find_by_product_id(self, product_id):
        return self._items.get(str(product_id))

    def save(self, item):
        self._items[str(item.product_id)] = item

    def reserve(self, product_id, quantity):
        item = self._items.get(str(product_id))
        if item:
            item.reserved += quantity
        return item

    def release(self, product_id, quantity):
        item = self._items.get(str(product_id))
        if item:
            item.reserved = max(0, item.reserved - quantity)
        return item

    def record_restock(self, event):
        item = self._items.get(str(event.product_id))
        if item:
            item.on_hand += event.quantity
        return item


class SpyEmailPort(EmailPort):
    def __init__(self):
        self.sent: list[dict] = []

    def send_order_confirmation(self, to_email, order_id, total):
        self.sent.append({"type": "order_confirmation", "to": to_email, "order_id": order_id})

    def send_shipping_notification(self, to_email, order_id):
        self.sent.append({"type": "shipping", "to": to_email, "order_id": order_id})

    def send_low_stock_alert(self, to_email, product_name, sku, available):
        self.sent.append({"type": "low_stock", "to": to_email})


class TestRegisterUser:
    def test_register_success(self):
        repo = InMemoryUserRepo()
        uc = RegisterUserUseCase(repo)
        result = uc.execute(RegisterUserRequest(email="new@test.com", password="password123"))
        assert result.is_success
        assert result.unwrap().email == "new@test.com"

    def test_register_duplicate(self):
        repo = InMemoryUserRepo()
        uc = RegisterUserUseCase(repo)
        uc.execute(RegisterUserRequest(email="dup@test.com", password="password123"))
        result = uc.execute(RegisterUserRequest(email="dup@test.com", password="password123"))
        assert result.is_failure

    def test_short_password(self):
        repo = InMemoryUserRepo()
        uc = RegisterUserUseCase(repo)
        result = uc.execute(RegisterUserRequest(email="test@test.com", password="short"))
        assert result.is_failure


class TestCreateProductUseCase:
    def test_create_success(self, category):
        product_repo = InMemoryProductRepo()
        cat_repo = InMemoryCategoryRepo()
        cat_repo.create(category)
        uc = CreateProductUseCase(product_repo, cat_repo)
        result = uc.execute(CreateProductRequest(
            sku="NEW-001", name="New", description="New prod",
            price=Decimal("9.99"), category_id=category.id,
        ))
        assert result.is_success
        assert result.unwrap().sku == "NEW-001"

    def test_duplicate_sku(self, category):
        product_repo = InMemoryProductRepo()
        cat_repo = InMemoryCategoryRepo()
        cat_repo.create(category)
        uc = CreateProductUseCase(product_repo, cat_repo)
        uc.execute(CreateProductRequest(
            sku="DUP", name="A", description="A",
            price=Decimal("1"), category_id=category.id,
        ))
        result = uc.execute(CreateProductRequest(
            sku="DUP", name="B", description="B",
            price=Decimal("2"), category_id=category.id,
        ))
        assert result.is_failure


class TestAddToCartUseCase:
    def test_add_item(self, product):
        cart_repo = InMemoryCartRepo()
        product_repo = InMemoryProductRepo()
        product_repo.create(product)
        uc = AddToCartUseCase(cart_repo, product_repo)
        result = uc.execute(None, None, "sess1", AddCartItemRequest(product_id=product.id, quantity=2))
        assert result.is_success
        assert len(result.unwrap().items) == 1


class TestCreateOrderUseCase:
    def test_create_order_success(self, user, product, inventory):
        cart_repo = InMemoryCartRepo()
        product_repo = InMemoryProductRepo()
        order_repo = InMemoryOrderRepo()
        inv_repo = InMemoryInventoryRepo()
        email_port = SpyEmailPort()

        product_repo.create(product)
        inv_repo.save(inventory)

        now = datetime.utcnow()
        cart = Cart(id=uuid.uuid4(), user_id=user.id, session_id=None,
                     items=[CartItem(product_id=product.id, quantity=2, unit_price=product.price)],
                     created_at=now, updated_at=now)
        cart_repo.create(cart)

        uc = CreateOrderUseCase(order_repo, cart_repo, inv_repo, product_repo, email_port)
        result = uc.execute(user.id, cart.id)
        assert result.is_success
        assert result.unwrap().status == "pending"
        assert len(email_port.sent) == 1

    def test_empty_cart_fails(self, user):
        cart_repo = InMemoryCartRepo()
        product_repo = InMemoryProductRepo()
        order_repo = InMemoryOrderRepo()
        inv_repo = InMemoryInventoryRepo()
        email_port = SpyEmailPort()

        now = datetime.utcnow()
        cart = Cart(id=uuid.uuid4(), user_id=user.id, session_id=None, items=[],
                     created_at=now, updated_at=now)
        cart_repo.create(cart)

        uc = CreateOrderUseCase(order_repo, cart_repo, inv_repo, product_repo, email_port)
        result = uc.execute(user.id, cart.id)
        assert result.is_failure


class TestInventoryUseCases:
    def test_check_inventory(self, product, inventory):
        inv_repo = InMemoryInventoryRepo()
        inv_repo.save(inventory)
        uc = CheckInventoryUseCase(inv_repo)
        result = uc.execute(product.id)
        assert result.is_success
        assert result.unwrap().available == 100

    def test_restock(self, product, inventory):
        inv_repo = InMemoryInventoryRepo()
        inv_repo.save(inventory)
        uc = RecordRestockUseCase(inv_repo)
        result = uc.execute(product.id, RestockRequest(quantity=50))
        assert result.is_success
        assert result.unwrap().on_hand == 150
