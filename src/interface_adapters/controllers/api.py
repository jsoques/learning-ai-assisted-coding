from __future__ import annotations

import uuid

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.application.dto.dtos import (
    AddCartItemRequest,
    CartItemResponse,
    CartResponse,
    CreateProductRequest,
    LoginRequest,
    OrderLineItemResponse,
    OrderResponse,
    PaginatedResponse,
    ProductResponse,
    RegisterUserRequest,
    RestockRequest,
    TokenResponse,
    TransitionOrderStatusRequest,
    UpdateProductRequest,
    UserResponse,
)
from src.application.use_cases.auth_use_cases import AuthenticateUserUseCase, RegisterUserUseCase
from src.application.use_cases.cart_use_cases import (
    AddToCartUseCase,
    GetCartUseCase,
    MergeCartOnLoginUseCase,
    RemoveFromCartUseCase,
)
from src.application.use_cases.inventory_use_cases import CheckInventoryUseCase, RecordRestockUseCase
from src.application.use_cases.order_use_cases import (
    CreateOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
    TransitionOrderStatusUseCase,
)
from src.application.use_cases.product_use_cases import (
    CreateProductUseCase,
    DeleteProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
    UpdateProductUseCase,
)
from src.framework.auth.dependencies import get_current_user, optional_user, require_admin
from src.framework.auth.jwt import create_access_token, create_refresh_token, decode_token
from src.framework.db.models import UserModel
from src.framework.db.session import get_db
from src.infra.events.simple_event_bus import LoggingEventBus
from src.infra.repositories.cart_repo import SQLAlchemyCartRepository
from src.infra.repositories.inventory_repo import SQLAlchemyInventoryRepository
from src.infra.repositories.order_repo import SQLAlchemyOrderRepository
from src.infra.repositories.product_repo import SQLAlchemyCategoryRepository, SQLAlchemyProductRepository
from src.infra.repositories.user_repo import SQLAlchemyUserRepository
from src.infra.email.mailpit_adapter import MailpitEmailAdapter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "disconnected"}


@router.post("/auth/register", status_code=201, tags=["Auth"])
def register(request: RegisterUserRequest, db: Session = Depends(get_db)):
    use_case = RegisterUserUseCase(SQLAlchemyUserRepository(db))
    result = use_case.execute(request)
    if result.is_failure:
        if "already" in result.unwrap_error():
            raise HTTPException(status_code=409, detail=result.unwrap_error())
        raise HTTPException(status_code=422, detail=result.unwrap_error())
    return result.unwrap()


@router.post("/auth/login", tags=["Auth"])
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    use_case = AuthenticateUserUseCase(SQLAlchemyUserRepository(db))
    result = use_case.execute(request)
    if result.is_failure:
        raise HTTPException(status_code=401, detail=result.unwrap_error())

    user = result.unwrap()
    access_token = create_access_token(str(user.id), user.role)
    refresh_token = create_refresh_token(str(user.id))
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax")
    return TokenResponse(access_token=access_token)


@router.post("/auth/refresh", tags=["Auth"])
def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Refresh token required")
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    repo = SQLAlchemyUserRepository(db)
    user = repo.find_by_id(uuid.UUID(payload["sub"]))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_access_token(str(user.id), user.role)
    new_refresh = create_refresh_token(str(user.id))
    response.set_cookie(key="refresh_token", value=new_refresh, httponly=True, samesite="lax")
    return TokenResponse(access_token=access_token)


@router.get("/auth/me", tags=["Auth"])
def me(current_user: UserModel = Depends(get_current_user)):
    return UserResponse(
        id=uuid.UUID(current_user.id),
        email=current_user.email,
        role=current_user.role,
        created_at=current_user.created_at,
    )


@router.get("/categories", tags=["Categories"])
def list_categories(db: Session = Depends(get_db)):
    repo = SQLAlchemyCategoryRepository(db)
    categories = repo.list_all()
    return categories


@router.post("/categories", status_code=201, tags=["Categories"])
def create_category(
    name: str,
    description: str = "",
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    from src.domain.entities.models import Category

    repo = SQLAlchemyCategoryRepository(db)
    category = Category(id=uuid.uuid4(), name=name, description=description)
    created = repo.create(category)
    return {"id": str(created.id), "name": created.name, "description": created.description}


@router.get("/products", tags=["Products"])
def list_products(
    q: str | None = None,
    category_id: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    page: int = 1,
    per_page: int = 20,
    db: Session = Depends(get_db),
):
    use_case = ListProductsUseCase(SQLAlchemyProductRepository(db))
    cat_uuid = uuid.UUID(category_id) if category_id else None
    result = use_case.execute(query=q, category_id=cat_uuid, price_min=price_min, price_max=price_max, page=page, per_page=per_page)
    return result.unwrap()


@router.get("/products/{product_id}", tags=["Products"])
def get_product(product_id: str, db: Session = Depends(get_db)):
    use_case = GetProductUseCase(SQLAlchemyProductRepository(db), SQLAlchemyInventoryRepository(db))
    result = use_case.execute(uuid.UUID(product_id))
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.post("/products", status_code=201, tags=["Products"])
def create_product(
    request: CreateProductRequest,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    use_case = CreateProductUseCase(SQLAlchemyProductRepository(db), SQLAlchemyCategoryRepository(db))
    result = use_case.execute(request)
    if result.is_failure:
        if "already" in result.unwrap_error():
            raise HTTPException(status_code=409, detail=result.unwrap_error())
        if "not found" in result.unwrap_error():
            raise HTTPException(status_code=404, detail=result.unwrap_error())
        raise HTTPException(status_code=422, detail=result.unwrap_error())
    return result.unwrap()


@router.patch("/products/{product_id}", tags=["Products"])
def update_product(
    product_id: str,
    request: UpdateProductRequest,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    use_case = UpdateProductUseCase(SQLAlchemyProductRepository(db))
    result = use_case.execute(uuid.UUID(product_id), request)
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.delete("/products/{product_id}", status_code=204, tags=["Products"])
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    use_case = DeleteProductUseCase(SQLAlchemyProductRepository(db))
    result = use_case.execute(uuid.UUID(product_id))
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())


@router.post("/cart/items", tags=["Cart"])
def add_to_cart(
    request: AddCartItemRequest,
    current_user: UserModel | None = Depends(optional_user),
    db: Session = Depends(get_db),
):
    cart_repo = SQLAlchemyCartRepository(db)
    product_repo = SQLAlchemyProductRepository(db)
    use_case = AddToCartUseCase(cart_repo, product_repo)

    session_id = None
    cart_id = None
    user_id = uuid.UUID(current_user.id) if current_user else None

    # If user has a cart, use it
    if user_id:
        existing = cart_repo.find_by_user_id(user_id)
        if existing:
            cart_id = existing.id

    result = use_case.execute(cart_id, user_id, session_id, request)
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.delete("/cart/items/{product_id}", tags=["Cart"])
def remove_from_cart(
    product_id: str,
    cart_id: str,
    db: Session = Depends(get_db),
):
    use_case = RemoveFromCartUseCase(SQLAlchemyCartRepository(db))
    result = use_case.execute(uuid.UUID(cart_id), product_id=uuid.UUID(product_id))
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.delete("/cart", tags=["Cart"])
def clear_cart(
    cart_id: str,
    db: Session = Depends(get_db),
):
    use_case = RemoveFromCartUseCase(SQLAlchemyCartRepository(db))
    result = use_case.execute(uuid.UUID(cart_id), clear=True)
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.get("/cart/{cart_id}", tags=["Cart"])
def get_cart(cart_id: str, db: Session = Depends(get_db)):
    use_case = GetCartUseCase(SQLAlchemyCartRepository(db))
    result = use_case.execute(uuid.UUID(cart_id))
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.post("/cart/merge", tags=["Cart"])
def merge_cart(
    session_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    use_case = MergeCartOnLoginUseCase(SQLAlchemyCartRepository(db))
    result = use_case.execute(uuid.UUID(current_user.id), session_id)
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.post("/orders", status_code=201, tags=["Orders"])
def create_order(
    cart_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    use_case = CreateOrderUseCase(
        SQLAlchemyOrderRepository(db),
        SQLAlchemyCartRepository(db),
        SQLAlchemyInventoryRepository(db),
        SQLAlchemyProductRepository(db),
        MailpitEmailAdapter(),
        LoggingEventBus(),
    )
    result = use_case.execute(uuid.UUID(current_user.id), uuid.UUID(cart_id))
    if result.is_failure:
        detail = result.unwrap_error()
        if "empty" in detail:
            raise HTTPException(status_code=400, detail=detail)
        if "Insufficient" in detail:
            raise HTTPException(status_code=409, detail=detail)
        raise HTTPException(status_code=404, detail=detail)
    return result.unwrap()


@router.get("/orders", tags=["Orders"])
def list_orders(
    status: str | None = None,
    page: int = 1,
    per_page: int = 20,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    use_case = ListOrdersUseCase(SQLAlchemyOrderRepository(db))
    is_admin = current_user.role == "admin"
    result = use_case.execute(
        user_id=uuid.UUID(current_user.id),
        is_admin=is_admin,
        status=status,
        page=page,
        per_page=per_page,
    )
    if result.is_failure:
        raise HTTPException(status_code=401, detail=result.unwrap_error())
    return result.unwrap()


@router.get("/orders/{order_id}", tags=["Orders"])
def get_order(
    order_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    use_case = GetOrderUseCase(SQLAlchemyOrderRepository(db))
    is_admin = current_user.role == "admin"
    result = use_case.execute(uuid.UUID(order_id), uuid.UUID(current_user.id), is_admin)
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.patch("/orders/{order_id}/status", tags=["Orders"])
def transition_order_status(
    order_id: str,
    request: TransitionOrderStatusRequest,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    use_case = TransitionOrderStatusUseCase(SQLAlchemyOrderRepository(db), SQLAlchemyInventoryRepository(db), LoggingEventBus())
    result = use_case.execute(uuid.UUID(order_id), request)
    if result.is_failure:
        detail = result.unwrap_error()
        if "Cannot" in detail:
            raise HTTPException(status_code=409, detail=detail)
        raise HTTPException(status_code=404, detail=detail)
    return result.unwrap()


@router.get("/admin/orders", tags=["Admin"])
def admin_list_orders(
    status: str | None = None,
    page: int = 1,
    per_page: int = 20,
    _: UserModel = Depends(require_admin),
    db: Session = Depends(get_db),
):
    use_case = ListOrdersUseCase(SQLAlchemyOrderRepository(db))
    result = use_case.execute(is_admin=True, status=status, page=page, per_page=per_page)
    return result.unwrap()


@router.get("/inventory/{product_id}", tags=["Inventory"])
def check_inventory(
    product_id: str,
    db: Session = Depends(get_db),
):
    use_case = CheckInventoryUseCase(SQLAlchemyInventoryRepository(db))
    result = use_case.execute(uuid.UUID(product_id))
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()


@router.post("/inventory/{product_id}/restock", tags=["Inventory"])
def record_restock(
    product_id: str,
    request: RestockRequest,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    use_case = RecordRestockUseCase(SQLAlchemyInventoryRepository(db))
    result = use_case.execute(uuid.UUID(product_id), request)
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.unwrap_error())
    return result.unwrap()
