from __future__ import annotations

import uuid
from contextlib import asynccontextmanager

import base64

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.framework.auth.csrf import CSRFMiddleware
from src.framework.auth.jwt import hash_password, verify_password
from src.framework.db.models import Base, CategoryModel, InventoryModel, ProductModel, UserModel
from src.framework.db.session import SessionLocal, engine
from src.frontend.html_router import router as html_router
from src.interface_adapters.controllers.api import router

MOCK_PRODUCTS = [
    ("Electronics", "Wireless Bluetooth Headphones", "Premium noise-cancelling headphones with 30hr battery", 89.99),
    ("Electronics", "USB-C Hub 7-in-1", "Multi-port adapter with HDMI, USB-A, SD card reader", 34.99),
    ("Electronics", "Portable Power Bank 20000mAh", "High-capacity fast-charging power bank", 49.99),
    ("Electronics", "Mechanical Keyboard RGB", "Cherry MX switches, full-size RGB backlit", 79.99),
    ("Electronics", "Wireless Mouse Ergonomic", "Vertical design, rechargeable, silent clicks", 29.99),
    ("Electronics", "4K Webcam Auto-Focus", "Ultra HD 4K webcam with built-in microphone", 69.99),
    ("Electronics", "Smart Speaker Alexa", "Voice-controlled speaker with Dolby Audio", 59.99),
    ("Electronics", "27-inch 4K Monitor", "IPS panel, USB-C, 99% sRGB coverage", 349.99),
    ("Electronics", "Noise-Cancelling Earbuds", "True wireless, ANC, IPX5 waterproof", 129.99),
    ("Electronics", "Wi-Fi 6 Router", "AX5400 dual-band, mesh-compatible", 99.99),
    ("Clothing", "Men's Classic Fit Polo", "100% cotton, pique knit, 6 color options", 34.99),
    ("Clothing", "Women's Running Leggings", "High-waist, moisture-wicking, 4-way stretch", 44.99),
    ("Clothing", "Unisex Hoodie Fleece", "Soft brushed fleece, kangaroo pocket", 49.99),
    ("Clothing", "Men's Denim Jacket", "Classic trucker style, 100% cotton", 69.99),
    ("Clothing", "Women's Cashmere Sweater", "Luxurious cashmere, crew neck, machine washable", 89.99),
    ("Clothing", "Athletic Shorts Quick-Dry", "Lightweight, elastic waist, 7-inch inseam", 24.99),
    ("Clothing", "Formal Dress Shirt", "Non-iron wrinkle-free, slim fit, 5 colors", 39.99),
    ("Clothing", "Winter Puffer Jacket", "Water-resistant, down-alternative, hooded", 119.99),
    ("Clothing", "Cotton T-Shirt Pack 3", "Preshrunk, ring-spun, soft-touch fabric", 29.99),
    ("Clothing", "Leather Belt Classic", "Full-grain leather, brass buckle, 1.5 inch", 34.99),
    ("Home", "Stainless Steel Water Bottle", "Double-wall vacuum insulated, 32oz", 24.99),
    ("Home", "Scented Soy Candle Set", "Hand-poured, essential oils, 3-pack", 19.99),
    ("Home", "Bamboo Cutting Board", "Organic bamboo, large 18x12 inch", 22.99),
    ("Home", "Microfiber Cleaning Cloths", "Ultra-absorbent, lint-free, 12-pack", 14.99),
    ("Home", "Cast Iron Skillet 12-inch", "Pre-seasoned, oven-safe to 500F", 39.99),
    ("Home", "Memory Foam Pillow", "Cooling gel, contoured neck support", 44.99),
    ("Home", "Indoor Herb Garden Kit", "Self-watering, LED grow light, 6 pods", 34.99),
    ("Home", "Smart LED Light Bulbs", "WiFi color-changing, works with Alexa, 4-pack", 29.99),
    ("Home", "French Press Coffee Maker", "34oz stainless steel, double-wall", 32.99),
    ("Home", "Weighted Blanket 15lbs", "Cotton cover, glass bead fill, queen size", 59.99),
    ("Sports", "Yoga Mat Premium", "Non-slip, 6mm thick, carry strap included", 29.99),
    ("Sports", "Resistance Bands Set", "5 levels, latex-free, with door anchor", 19.99),
    ("Sports", "Adjustable Dumbbells", "5-52.5lbs per pair, space-saving rack", 249.99),
    ("Sports", "Jump Rope Speed", "Ball-bearing, adjustable cable, foam handles", 12.99),
    ("Sports", "Foam Roller High-Density", "36 inch, trigger point relief", 24.99),
    ("Sports", "Insulated Water Bottle 64oz", "Half-gallon, straw lid, leak-proof", 19.99),
    ("Sports", "Tennis Racket Pro", "Lightweight graphite, vibration dampener", 89.99),
    ("Sports", "Cycling Gloves Padded", "Gel padding, breathable mesh, touchscreen", 22.99),
    ("Sports", "Swim Goggles Anti-Fog", "UV protection, adjustable strap, 6 colors", 15.99),
    ("Sports", "Hiking Backpack 40L", "Water-resistant, padded straps, rain cover", 69.99),
    ("Books", "The Art of Clean Code", "Best practices for writing maintainable software", 29.99),
    ("Books", "Designing Data-Intensive Applications", "Distributed systems fundamentals", 39.99),
    ("Books", "Atomic Habits", "An Easy & Proven Way to Build Good Habits", 16.99),
    ("Books", "The Pragmatic Programmer", "Timeless tips for software engineers", 34.99),
    ("Books", "Deep Work", "Rules for focused success in a distracted world", 15.99),
    ("Books", "System Design Interview", "An insider's guide to acing interviews", 29.99),
    ("Books", "Clean Architecture", "A craftsman's guide to software structure", 35.99),
    ("Books", "The Psychology of Money", "Timeless lessons on wealth and greed", 14.99),
    ("Books", "JavaScript: The Good Parts", "Unearthing the excellence in JavaScript", 25.99),
    ("Books", "Thinking, Fast and Slow", "Two systems that drive the way we think", 18.99),
    ("Toys", "Building Blocks 1000 pc", "STEM educational, compatible with major brands", 34.99),
    ("Toys", "Remote Control Car", "4WD off-road, rechargeable, 30min runtime", 39.99),
    ("Toys", "Board Game Strategy", "Award-winning family board game, ages 10+", 29.99),
    ("Toys", "Puzzle 3D Model Kit", "Metal assembly, Eiffel Tower, 150 pieces", 24.99),
    ("Toys", "Science Experiment Kit", "50 chemistry experiments, ages 8-14", 32.99),
    ("Toys", "Plush Teddy Bear", "Hypoallergenic, 18 inches, machine washable", 22.99),
    ("Toys", "Card Game Party Pack", "Family-friendly, 300 cards, 15 min play", 14.99),
    ("Toys", "Drone with Camera", "720p HD, altitude hold, one-key takeoff", 59.99),
    ("Toys", "Watercolor Paint Set", "24 vibrant colors, brush set, pad included", 19.99),
    ("Toys", "Musical Keyboard Toy", "37 keys, microphone, 10 demo songs", 44.99),
    ("Food", "Premium Coffee Beans", "Single origin, medium roast, 12oz bag", 18.99),
    ("Food", "Dark Chocolate Collection", "72% cacao, assorted flavors, 6-pack", 24.99),
    ("Food", "Organic Green Tea", "Japanese sencha, loose leaf, 4oz tin", 14.99),
    ("Food", "Mixed Nuts Deluxe", "Roasted, salted, cashews/almonds/pecans, 2lb", 22.99),
    ("Food", "Artisan Honey Jar", "Raw wildflower honey, 12oz glass jar", 12.99),
    ("Food", "Hot Sauce Variety Pack", "6 handcrafted sauces, mild to extreme", 29.99),
    ("Food", "Trail Mix Energy", "Almonds, cranberries, dark chocolate, 1lb", 11.99),
    ("Food", "Maple Syrup Pure", "Grade A amber, Vermont sourced, 8.5oz", 15.99),
    ("Food", "Protein Bars 12-pack", "20g protein, gluten-free, 3 flavors", 24.99),
    ("Food", "Olive Oil Extra Virgin", "Cold-pressed, first harvest, 500ml tin", 19.99),
    ("Electronics", "Tablet Stand Adjustable", "Aluminum alloy, foldable, universal fit", 22.99),
    ("Electronics", "LED Desk Lamp", "Touch control, 5 brightness levels, USB port", 34.99),
    ("Electronics", "Wireless Charger Pad", "15W fast charge, Qi-compatible, thin design", 19.99),
    ("Electronics", "External SSD 1TB", "USB-C, 1050MB/s read, portable", 89.99),
    ("Electronics", "Smart Plug Mini", "WiFi, energy monitoring, voice control, 4-pack", 29.99),
    ("Clothing", "Beanie Winter Knit", "Acrylic-wool blend, unisex, 8 colors", 14.99),
    ("Clothing", "Sunglasses Polarized", "UV400 protection, lightweight, sport frame", 24.99),
    ("Clothing", "Canvas Backpack Casual", "Waxed canvas, leather trim, laptop sleeve", 54.99),
    ("Clothing", "Silk Scarf Luxury", "100% mulberry silk, 35x35 inch", 39.99),
    ("Clothing", "Waterproof Rain Jacket", "Breathable, taped seams, packable hood", 89.99),
    ("Home", "Electric Kettle Gooseneck", "Variable temp, 1L, pour-over ready", 49.99),
    ("Home", "Plant Pot Set Ceramic", "Modern design, drainage hole, 3 sizes", 34.99),
    ("Home", "Wall Clock Minimalist", "Silent quartz, 12 inch, matte black", 24.99),
    ("Home", "Storage Baskets Woven", "Handwoven seagrass, set of 3, with handles", 29.99),
    ("Home", "Air Purifier HEPA", "Covers 500sqft, quiet mode, auto sensor", 149.99),
    ("Sports", "Kettlebell Cast Iron", "35lbs, flat base, powder coated", 44.99),
    ("Sports", "Running Shoes Lightweight", "Breathable mesh, responsive cushion", 74.99),
    ("Sports", "Waterproof Fitness Tracker", "Heart rate, SpO2, GPS, 14-day battery", 69.99),
    ("Sports", "Skipping Rope Speed", "Ball bearings, adjustable cable, steel core", 9.99),
    ("Sports", "Pull-Up Bar Doorway", "No-drill install, padded grips, 300lb max", 34.99),
    ("Books", "Domain-Driven Design", "Tackling complexity in the heart of software", 44.99),
    ("Books", "Refactoring", "Improving the design of existing code", 39.99),
    ("Books", "Working Effectively with Legacy Code", "Safe techniques for difficult codebases", 42.99),
    ("Books", "Code Complete 2nd Edition", "A practical handbook of software construction", 49.99),
    ("Books", "The Mythical Man-Month", "Essays on software engineering management", 24.99),
    ("Toys", "Nerf Blaster", "Motorized, 20 dart drum, ages 8+", 34.99),
    ("Toys", "Lego Classic Set", "1100 pieces, creative building bricks", 49.99),
    ("Toys", "Kite Large Delta", "Easy flyer, ripstop nylon, 60-inch wingspan", 19.99),
    ("Toys", "Magnetic Tiles 100pc", "STEM learning, colorful, compatible 3D shapes", 39.99),
    ("Toys", "Slime Making Kit", "15 colors, glow-in-the-dark, 5 add-ins", 17.99),
]


def seed_admin():
    db: Session = SessionLocal()
    try:
        existing = db.query(UserModel).filter(UserModel.email == "admin@shop.com").first()
        if existing is None:
            admin = UserModel(
                email="admin@shop.com",
                hashed_password=hash_password("admin123"),
                role="admin",
                must_change_password=1,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


def seed_products():
    db: Session = SessionLocal()
    try:
        existing = db.query(ProductModel).first()
        if existing is not None:
            return

        cat_names = sorted({c for c, _, _, _ in MOCK_PRODUCTS})
        cat_map = {}
        for name in cat_names:
            cat = CategoryModel(id=str(uuid.uuid4()), name=name, description=f"{name} products")
            db.add(cat)
            cat_map[name] = cat.id

        for i, (cat_name, pname, desc, price) in enumerate(MOCK_PRODUCTS):
            pid = str(uuid.uuid4())
            product = ProductModel(
                id=pid,
                sku=f"SKU-{i+1:04d}",
                name=pname,
                description=desc,
                price=price,
                category_id=cat_map[cat_name],
            )
            inventory = InventoryModel(
                product_id=pid,
                on_hand=50,
                low_stock_threshold=5,
            )
            db.add(product)
            db.add(inventory)

        db.commit()
    finally:
        db.close()


PROTECTED_PATHS = ("/docs", "/redoc", "/openapi.json")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_admin()
    seed_products()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="E-Commerce API", version="0.1.0", lifespan=lifespan)

    class DocsAuthMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            if request.url.path in PROTECTED_PATHS:
                auth = request.headers.get("Authorization")
                if not auth or not auth.startswith("Basic "):
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Unauthorized"},
                        headers={"WWW-Authenticate": "Basic realm=\"Admin docs\""},
                    )
                try:
                    decoded = base64.b64decode(auth.removeprefix("Basic ")).decode()
                    email, password = decoded.split(":", 1)
                except Exception:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid credentials"},
                        headers={"WWW-Authenticate": "Basic realm=\"Admin docs\""},
                    )
                db = SessionLocal()
                try:
                    user = db.query(UserModel).filter(UserModel.email == email).first()
                    if not user or not user.role or (user.role != "admin") or not verify_password(password, user.hashed_password):
                        return JSONResponse(
                            status_code=401,
                            content={"detail": "Unauthorized"},
                            headers={"WWW-Authenticate": "Basic realm=\"Admin docs\""},
                        )
                finally:
                    db.close()
            return await call_next(request)

    app.add_middleware(DocsAuthMiddleware)
    app.add_middleware(CSRFMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(html_router)
    app.include_router(router, prefix="/api")

    return app
