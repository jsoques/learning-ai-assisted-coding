from __future__ import annotations

import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt
from sqlalchemy.orm import Session

from src.application.dto.dtos import (
    AddCartItemRequest,
    CreateProductRequest,
    LoginRequest,
    RegisterUserRequest,
    RestockRequest,
    TransitionOrderStatusRequest,
)
from src.application.use_cases.auth_use_cases import AuthenticateUserUseCase, RegisterUserUseCase
from src.application.use_cases.cart_use_cases import AddToCartUseCase, RemoveFromCartUseCase
from src.application.use_cases.inventory_use_cases import CheckInventoryUseCase, RecordRestockUseCase
from src.application.use_cases.order_use_cases import (
    CreateOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
    TransitionOrderStatusUseCase,
)
from src.application.use_cases.product_use_cases import (
    CreateProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
)
from src.framework.auth.jwt import (
    SECRET_KEY,
    ALGORITHM,
    decode_token,
    hash_password,
    verify_password,
)
from src.framework.db.models import CategoryModel, InventoryModel, ProductModel, UserModel
from src.framework.db.session import get_db
from src.infra.email.mailpit_adapter import MailpitEmailAdapter
from src.infra.repositories.cart_repo import SQLAlchemyCartRepository
from src.infra.repositories.inventory_repo import SQLAlchemyInventoryRepository
from src.infra.repositories.order_repo import SQLAlchemyOrderRepository
from src.infra.repositories.product_repo import SQLAlchemyCategoryRepository, SQLAlchemyProductRepository
from src.infra.repositories.user_repo import SQLAlchemyUserRepository

templates = Jinja2Templates(directory="templates")
router = APIRouter()


def get_session_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session_token")
    if not token:
        return None
    payload = decode_token(token)
    if not payload or payload.get("type") != "session":
        return None
    return db.query(UserModel).filter(UserModel.id == payload["sub"]).first()


@router.get("/auth/login", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def login_page(request: Request):
    err = request.query_params.get("error")
    return templates.TemplateResponse(request,"auth/login.html", {"request": request, "error": err})


@router.post("/auth/login", tags=["HTMx-FrontEnd"])
def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    repo = SQLAlchemyUserRepository(db)
    uc = AuthenticateUserUseCase(repo)
    result = uc.execute(LoginRequest(email=email, password=password))
    if result.is_failure:
        return templates.TemplateResponse(request,"auth/login.html", {"request": request, "error": "Invalid email or password"}, status_code=401)

    user = db.query(UserModel).filter(UserModel.email == email).first()
    session_token = jwt.encode(
        {"sub": user.id, "role": user.role, "type": "session"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    resp = RedirectResponse(url="/auth/profile", status_code=303)
    resp.set_cookie(key="session_token", value=session_token, httponly=True, max_age=86400)
    return resp


@router.get("/auth/register", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def register_page(request: Request):
    err = request.query_params.get("error")
    return templates.TemplateResponse(request,"auth/register.html", {"request": request, "error": err})


@router.post("/auth/register", tags=["HTMx-FrontEnd"])
def register_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    repo = SQLAlchemyUserRepository(db)
    uc = RegisterUserUseCase(repo)
    result = uc.execute(RegisterUserRequest(email=email, password=password))
    if result.is_failure:
        return templates.TemplateResponse(request,"auth/register.html", {"request": request, "error": result.unwrap_error()}, status_code=400)
    return RedirectResponse(url="/auth/login?registered=1", status_code=303)


@router.get("/auth/logout", tags=["HTMx-FrontEnd"])
def logout():
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("session_token")
    return resp


def _auth_check(request: Request, db: Session):
    user = get_session_user(request, db)
    if not user:
        return None
    return user


@router.get("/auth/profile", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def profile_page(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    return templates.TemplateResponse(request,"auth/profile.html", {"request": request, "user": user, "must_change_password": bool(user.must_change_password)})


@router.get("/auth/change-password", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def change_password_page(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    err = request.query_params.get("error")
    msg = request.query_params.get("message")
    return templates.TemplateResponse(request,"auth/change_password.html", {"request": request, "error": err, "message": msg})


@router.post("/auth/change-password", tags=["HTMx-FrontEnd"])
def change_password_post(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    if not verify_password(current_password, user.hashed_password):
        return RedirectResponse(url="/auth/change-password?error=Current+password+is+incorrect", status_code=303)
    if len(new_password) < 8:
        return RedirectResponse(url="/auth/change-password?error=New+password+must+be+at+least+8+characters", status_code=303)
    user.hashed_password = hash_password(new_password)
    user.must_change_password = 0
    db.commit()
    return RedirectResponse(url="/auth/change-password?message=Password+changed+successfully", status_code=303)


@router.get("/", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def home(request: Request, db: Session = Depends(get_db)):
    user = _auth_check(request, db)
    categories = db.query(CategoryModel).all()
    uc = ListProductsUseCase(SQLAlchemyProductRepository(db))
    result = uc.execute(page=1, per_page=20)
    products = result.unwrap().items if result.is_success else []
    return templates.TemplateResponse(request,"index.html", {
        "request": request,
        "user": user,
        "products": products,
        "categories": categories,
    })


@router.get("/products", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def products_page(
    request: Request,
    page: int = 1,
    q: str = "",
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    repo = SQLAlchemyProductRepository(db)
    uc = ListProductsUseCase(repo)
    result = uc.execute(query=q or None, page=page, per_page=20)
    categories = db.query(CategoryModel).all()
    if result.is_success:
        data = result.unwrap()
        return templates.TemplateResponse(request,"products/list.html", {
            "request": request,
            "user": user,
            "products": data.items,
            "categories": categories,
            "page": data.page,
            "total_pages": data.total_pages,
        })
    return templates.TemplateResponse(request,"products/list.html", {"request": request, "user": user, "products": [], "categories": categories, "page": 1, "total_pages": 1})


@router.get("/products/search", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def products_search(
    request: Request,
    q: str = "",
    category_id: str = "",
    page: int = 1,
    db: Session = Depends(get_db),
):
    repo = SQLAlchemyProductRepository(db)
    uc = ListProductsUseCase(repo)
    cat_uuid = uuid.UUID(category_id) if category_id else None
    result = uc.execute(query=q or None, category_id=cat_uuid, page=page, per_page=20)
    items = result.unwrap().items if result.is_success else []
    return templates.TemplateResponse(request,"products/_list_items.html", {"request": request, "products": items})


@router.get("/products/{product_id}", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def product_detail(
    request: Request,
    product_id: str,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    uc = GetProductUseCase(SQLAlchemyProductRepository(db), SQLAlchemyInventoryRepository(db))
    result = uc.execute(uuid.UUID(product_id))
    if result.is_failure:
        return RedirectResponse(url="/products", status_code=303)
    inv_uc = CheckInventoryUseCase(SQLAlchemyInventoryRepository(db))
    inv_result = inv_uc.execute(uuid.UUID(product_id))
    inventory = inv_result.unwrap() if inv_result.is_success else None
    return templates.TemplateResponse(request,"products/detail.html", {
        "request": request,
        "user": user,
        "product": result.unwrap(),
        "inventory": inventory,
    })


@router.post("/cart/add/{product_id}", tags=["HTMx-FrontEnd"])
def cart_add(
    request: Request,
    product_id: str,
    quantity: int = 1,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return HTMLResponse('<div class="bg-red-500 text-white px-4 py-2 rounded shadow">Please login first</div>')
    cart_repo = SQLAlchemyCartRepository(db)
    product_repo = SQLAlchemyProductRepository(db)
    uc = AddToCartUseCase(cart_repo, product_repo)
    cart = cart_repo.find_by_user_id(uuid.UUID(user.id))
    result = uc.execute(cart.id if cart else None, uuid.UUID(user.id), None, AddCartItemRequest(product_id=uuid.UUID(product_id), quantity=quantity))
    if result.is_success:
        return HTMLResponse('<div class="bg-green-500 text-white px-4 py-2 rounded shadow">Added to cart!</div>')
    return HTMLResponse(f'<div class="bg-red-500 text-white px-4 py-2 rounded shadow">{result.unwrap_error()}</div>')


@router.get("/cart", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def cart_page(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    cart_repo = SQLAlchemyCartRepository(db)
    cart = cart_repo.find_by_user_id(uuid.UUID(user.id))
    cart_data = None
    if cart:
        product_repo = SQLAlchemyProductRepository(db)
        items = []
        total = Decimal("0")
        for ci in cart.items:
            p = product_repo.find_by_id(ci.product_id)
            name = p.name if p else "Unknown"
            unit_total = ci.unit_price.amount * ci.quantity
            total += unit_total
            items.append({
                "product_id": str(ci.product_id),
                "product_name": name,
                "quantity": ci.quantity,
                "unit_price": float(ci.unit_price.amount),
                "line_total": float(unit_total),
            })
        cart_data = {"items": items, "total": float(total)}
    return templates.TemplateResponse(request,"cart/cart.html", {"request": request, "cart": cart_data})


@router.delete("/cart/items/{product_id}", tags=["HTMx-FrontEnd"])
def cart_remove(
    request: Request,
    product_id: str,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return HTMLResponse("")
    cart_repo = SQLAlchemyCartRepository(db)
    cart = cart_repo.find_by_user_id(uuid.UUID(user.id))
    if cart:
        uc = RemoveFromCartUseCase(cart_repo)
        uc.execute(cart.id, product_id=uuid.UUID(product_id))
    return HTMLResponse("")


@router.delete("/cart/clear", tags=["HTMx-FrontEnd"])
def cart_clear(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return HTMLResponse("")
    cart_repo = SQLAlchemyCartRepository(db)
    cart = cart_repo.find_by_user_id(uuid.UUID(user.id))
    if cart:
        uc = RemoveFromCartUseCase(cart_repo)
        uc.execute(cart.id, clear=True)
    return HTMLResponse(
        '<div class="text-center py-12"><p class="text-gray-500 text-lg">Your cart is empty.</p>'
        '<a href="/products" class="text-indigo-600 hover:underline mt-2 inline-block">Browse Products</a></div>'
    )


@router.get("/orders", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def orders_page(
    request: Request,
    status: str = "",
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    uc = ListOrdersUseCase(SQLAlchemyOrderRepository(db))
    result = uc.execute(user_id=uuid.UUID(user.id), status=status or None)
    orders = result.unwrap().items if result.is_success else []
    return templates.TemplateResponse(request,"orders/history.html", {"request": request, "orders": orders})


@router.get("/orders/{order_id}", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def order_detail(
    request: Request,
    order_id: str,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    uc = GetOrderUseCase(SQLAlchemyOrderRepository(db))
    result = uc.execute(uuid.UUID(order_id), uuid.UUID(user.id), user.role == "admin")
    if result.is_failure:
        return RedirectResponse(url="/orders", status_code=303)
    return templates.TemplateResponse(request,"orders/detail.html", {"request": request, "order": result.unwrap()})


@router.get("/orders/checkout", tags=["HTMx-FrontEnd"])
def checkout(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    cart_repo = SQLAlchemyCartRepository(db)
    cart = cart_repo.find_by_user_id(uuid.UUID(user.id))
    if not cart or not cart.items:
        return RedirectResponse(url="/cart", status_code=303)
    uc = CreateOrderUseCase(
        SQLAlchemyOrderRepository(db),
        SQLAlchemyCartRepository(db),
        SQLAlchemyInventoryRepository(db),
        SQLAlchemyProductRepository(db),
        MailpitEmailAdapter(),
    )
    result = uc.execute(uuid.UUID(user.id), cart.id)
    if result.is_success:
        return RedirectResponse(url=f"/orders/{result.unwrap().id}", status_code=303)
    return RedirectResponse(url="/cart", status_code=303)


@router.get("/admin", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user or user.role != "admin":
        return RedirectResponse(url="/auth/login", status_code=303)
    order_count = db.query(ProductModel).count()
    product_count = db.query(ProductModel).count()
    low_stock_count = db.query(InventoryModel).filter(
        (InventoryModel.on_hand - InventoryModel.reserved) <= InventoryModel.low_stock_threshold
    ).count()
    uc = ListOrdersUseCase(SQLAlchemyOrderRepository(db))
    result = uc.execute(is_admin=True, per_page=5)
    orders = result.unwrap().items if result.is_success else []
    return templates.TemplateResponse(request,"admin/dashboard.html", {
        "request": request,
        "stats": {"order_count": order_count, "product_count": product_count, "low_stock_count": low_stock_count},
        "orders": orders,
    })


@router.get("/admin/orders", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def admin_orders(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user or user.role != "admin":
        return RedirectResponse(url="/auth/login", status_code=303)
    uc = ListOrdersUseCase(SQLAlchemyOrderRepository(db))
    result = uc.execute(is_admin=True)
    orders = result.unwrap().items if result.is_success else []
    return templates.TemplateResponse(request,"admin/orders.html", {"request": request, "orders": orders})


@router.patch("/admin/orders/{order_id}/status", tags=["HTMx-FrontEnd"])
def admin_update_order_status(
    request: Request,
    order_id: str,
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user or user.role != "admin":
        return HTMLResponse("Unauthorized")
    uc = TransitionOrderStatusUseCase(SQLAlchemyOrderRepository(db), SQLAlchemyInventoryRepository(db))
    result = uc.execute(uuid.UUID(order_id), TransitionOrderStatusRequest(status=status))
    if result.is_failure:
        return HTMLResponse(f'<div class="text-red-600">{result.unwrap_error()}</div>')
    order = result.unwrap()
    cls = "bg-yellow-100 text-yellow-800" if order.status == "pending" else "bg-blue-100 text-blue-800" if order.status == "paid" else "bg-purple-100 text-purple-800" if order.status == "shipped" else "bg-green-100 text-green-800" if order.status == "delivered" else "bg-red-100 text-red-800"
    opts = ""
    for s in ["pending", "paid", "shipped", "delivered", "cancelled"]:
        sel = "selected" if s == order.status else ""
        opts += f'<option value="{s}" {sel}>{s.capitalize()}</option>'
    return HTMLResponse(f'''
    <tr class="border-b" id="order-row-{order.id}">
        <td class="py-2 text-sm">{order.id[:8]}...</td>
        <td class="py-2 text-sm">{order.user_id[:8]}...</td>
        <td class="py-2"><span class="px-2 py-1 rounded text-xs font-medium {cls}">{order.status}</span></td>
        <td class="py-2">${order.total}</td>
        <td class="py-2"><select class="border rounded px-2 py-1 text-sm" hx-patch="/admin/orders/{order.id}/status" hx-target="#order-row-{order.id}" hx-swap="outerHTML" name="status">{opts}</select></td>
    </tr>
    ''')


@router.get("/admin/products", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def admin_products(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user or user.role != "admin":
        return RedirectResponse(url="/auth/login", status_code=303)
    products = db.query(ProductModel).all()
    categories = db.query(CategoryModel).all()
    return templates.TemplateResponse(request,"admin/products.html", {"request": request, "products": products, "categories": categories})


@router.post("/admin/products", tags=["HTMx-FrontEnd"])
def admin_create_product(
    request: Request,
    name: str = Form(...),
    sku: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    category_id: str = Form(""),
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user or user.role != "admin":
        return RedirectResponse(url="/auth/login", status_code=303)
    if category_id:
        cat_uuid = uuid.UUID(category_id)
    else:
        cat_uuid = uuid.uuid4()
        cat = CategoryModel(id=str(cat_uuid), name="General", description="")
        db.add(cat)
        db.commit()
    uc = CreateProductUseCase(SQLAlchemyProductRepository(db), SQLAlchemyCategoryRepository(db))
    uc.execute(CreateProductRequest(sku=sku, name=name, description=description, price=Decimal(str(price)), category_id=cat_uuid))
    return RedirectResponse(url="/admin/products", status_code=303)


@router.post("/admin/categories", tags=["HTMx-FrontEnd"])
def admin_create_category(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user or user.role != "admin":
        return RedirectResponse(url="/auth/login", status_code=303)
    cat = CategoryModel(id=str(uuid.uuid4()), name=name, description=description)
    db.add(cat)
    db.commit()
    return RedirectResponse(url="/admin/products", status_code=303)


@router.get("/admin/inventory", response_class=HTMLResponse, tags=["HTMx-FrontEnd"])
def admin_inventory(
    request: Request,
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user or user.role != "admin":
        return RedirectResponse(url="/auth/login", status_code=303)
    inventory_items = db.query(InventoryModel).all()
    items = []
    for inv in inventory_items:
        product = db.query(ProductModel).filter(ProductModel.id == inv.product_id).first()
        available = inv.on_hand - inv.reserved
        items.append({
            "product_id": inv.product_id,
            "product_name": product.name if product else "Unknown",
            "on_hand": inv.on_hand,
            "reserved": inv.reserved,
            "available": available,
            "low_stock_threshold": inv.low_stock_threshold,
            "is_low_stock": available <= inv.low_stock_threshold,
        })
    return templates.TemplateResponse(request,"admin/inventory.html", {"request": request, "inventory_items": items})


@router.post("/admin/inventory/{product_id}/restock", tags=["HTMx-FrontEnd"])
def admin_restock(
    request: Request,
    product_id: str,
    quantity: int = Form(...),
    db: Session = Depends(get_db),
):
    user = _auth_check(request, db)
    if not user or user.role != "admin":
        return HTMLResponse("Unauthorized")
    uc = RecordRestockUseCase(SQLAlchemyInventoryRepository(db))
    result = uc.execute(uuid.UUID(product_id), RestockRequest(quantity=quantity))
    if result.is_failure:
        return HTMLResponse(f'<div class="text-red-600">{result.unwrap_error()}</div>')
    inv = result.unwrap()
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    cls = "text-red-600 font-bold" if inv.is_low_stock else ""
    return HTMLResponse(f'''
    <tr class="border-b" id="inv-row-{inv.product_id}">
        <td class="py-2">{product.name if product else "Unknown"}</td>
        <td class="py-2">{inv.on_hand}</td>
        <td class="py-2">{inv.reserved}</td>
        <td class="py-2 {cls}">{inv.available}</td>
        <td class="py-2">{inv.low_stock_threshold}</td>
        <td class="py-2">
            <input type="number" id="restock-qty-{inv.product_id}" value="10" min="1" class="border rounded px-2 py-1 w-20 text-sm">
            <button class="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700" hx-post="/admin/inventory/{inv.product_id}/restock" hx-vals=\'{{"quantity": document.getElementById("restock-qty-{inv.product_id}").value}}\' hx-target="#inv-row-{inv.product_id}" hx-swap="outerHTML">Restock</button>
        </td>
    </tr>
    ''')
