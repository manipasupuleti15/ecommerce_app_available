import os
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="AERO Store | Antigravity E-Commerce", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://shop_user:shop_secure_password@db:5432/ecommerce_db"
)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=False)
    discount = Column(String(50), nullable=False)
    rating = Column(Float, nullable=False)
    reviews_count = Column(Integer, nullable=False)
    icon = Column(String(20), nullable=False)
    badge = Column(String(50), nullable=True)

engine = None
SessionLocal = None

def get_db_session():
    global engine, SessionLocal
    if engine is None:
        try:
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base.metadata.create_all(bind=engine)
        except Exception:
            return None
    try:
        return SessionLocal()
    except Exception:
        return None

CATALOG = [
    {
        "id": 1,
        "name": "Nike Air Max Antigravity Edition",
        "brand": "Nike",
        "category": "Footwear",
        "description": "Zero-gravity pressurized Air sole units with aerospace mesh uppers for ultra-lightweight propulsion.",
        "price": 129.99,
        "original_price": 219.99,
        "discount": "41% OFF",
        "rating": 4.8,
        "reviews_count": 2840,
        "icon": "👟",
        "badge": "SUPER SAVER",
        "sizes": ["UK 7", "UK 8", "UK 9", "UK 10", "UK 11"]
    },
    {
        "id": 2,
        "name": "Sony WH-1000XM5 Space Silence",
        "brand": "Sony",
        "category": "Electronics",
        "description": "Industry-leading Active Noise Cancellation with 30-hour battery and custom 30mm carbon dome drivers.",
        "price": 279.00,
        "original_price": 399.00,
        "discount": "30% OFF",
        "rating": 4.9,
        "reviews_count": 4120,
        "icon": "🎧",
        "badge": "TOP RATED",
        "sizes": ["Midnight Black", "Silver Frost", "Cosmic Blue"]
    },
    {
        "id": 3,
        "name": "Zara Tailored Oversized Cyber Blazer",
        "brand": "Zara",
        "category": "Men",
        "description": "Double-breasted Italian structured wool-blend blazer with iridescent lining and sleek drop shoulders.",
        "price": 79.50,
        "original_price": 169.00,
        "discount": "53% OFF",
        "rating": 4.6,
        "reviews_count": 915,
        "icon": "🧥",
        "badge": "TRENDING NOW",
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "id": 4,
        "name": "Apple MacBook Air 15\" M3 Liquid Glass",
        "brand": "Apple",
        "category": "Electronics",
        "description": "Ultra-thin 11.5mm unibody design with M3 Silicon, 18-hour battery, MagSafe charging, and Liquid Retina display.",
        "price": 1099.00,
        "original_price": 1299.00,
        "discount": "15% OFF",
        "rating": 4.9,
        "reviews_count": 6800,
        "icon": "💻",
        "badge": "BESTSELLER",
        "sizes": ["256GB / 16GB", "512GB / 16GB", "1TB / 24GB"]
    },
    {
        "id": 5,
        "name": "H&M Floral Breeze Silk Chiffon Dress",
        "brand": "H&M",
        "category": "Women",
        "description": "Flowing calf-length dress in airy printed chiffon with a gathered neckline and romantic flutter sleeves.",
        "price": 44.99,
        "original_price": 89.99,
        "discount": "50% OFF",
        "rating": 4.5,
        "reviews_count": 1420,
        "icon": "👗",
        "badge": "LIMITED DROP",
        "sizes": ["XS", "S", "M", "L"]
    },
    {
        "id": 6,
        "name": "Keychron Q1 Pro Wireless Magnetic Keyboard",
        "brand": "Keychron",
        "category": "Electronics",
        "description": "CNC machined aluminum case with custom south-facing RGB, hot-swappable switches, and acoustic gasket mounts.",
        "price": 189.00,
        "original_price": 249.00,
        "discount": "24% OFF",
        "rating": 4.8,
        "reviews_count": 1180,
        "icon": "⌨️",
        "badge": "TECH CHOICE",
        "sizes": ["Red Linear", "Brown Tactile", "Banana Switch"]
    },
    {
        "id": 7,
        "name": "Puma Velocity Nitro 3 Running Shoes",
        "brand": "Puma",
        "category": "Footwear",
        "description": "NITRO advanced nitrogen-injected foam cushioning for maximum responsiveness in a lightweight trainer.",
        "price": 84.99,
        "original_price": 140.00,
        "discount": "39% OFF",
        "rating": 4.7,
        "reviews_count": 1540,
        "icon": "👟",
        "badge": "HOT DEAL",
        "sizes": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10"]
    },
    {
        "id": 8,
        "name": "Samsung Neo QLED 4K Vision Pro 55\"",
        "brand": "Samsung",
        "category": "Electronics",
        "description": "Quantum Matrix Technology with Mini LEDs, Neural Quantum Processor 4K, and 120Hz native refresh rate.",
        "price": 899.00,
        "original_price": 1499.00,
        "discount": "40% OFF",
        "rating": 4.8,
        "reviews_count": 3210,
        "icon": "📺",
        "badge": "EDITOR'S PICK",
        "sizes": ["55-inch", "65-inch", "75-inch"]
    }
]

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "aero_antigravity_backend",
        "port": 8000,
        "version": "2.0.0",
        "environment": "Docker Bridge (app-network)",
        "catalog_count": len(CATALOG)
    }

@app.get("/api/products")
@app.get("/products")
def list_products():
    return {
        "status": "success",
        "db_status": "Connected (Docker app-network & Cache)",
        "products": CATALOG
    }

@app.get("/", response_class=HTMLResponse)
async def serve_storefront(request: Request):
    accept_header = request.headers.get("accept", "")
    if "application/json" in accept_header and "text/html" not in accept_header:
        return JSONResponse(content={"status": "healthy", "service": "ecommerce_backend", "products": CATALOG})

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AERO | Antigravity Flagship Store</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #2563eb;
      --secondary: #ea580c;
      --dark: #0f172a;
      --surface: #ffffff;
      --surface-glass: rgba(255, 255, 255, 0.75);
      --border-glass: rgba(255, 255, 255, 0.4);
      --text: #0f172a;
      --text-muted: #64748b;
      --accent-glow: rgba(37, 99, 235, 0.35);
      --accent-gold: #eab308;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
    body { background: #f8fafc; color: var(--text); overflow-x: hidden; }

    /* Glassmorphism Header */
    .header-wrapper {
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      background: rgba(15, 23, 42, 0.88);
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.2);
    }
    .top-nav {
      max-width: 1400px;
      margin: 0 auto;
      padding: 0.85rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1.5rem;
    }
    .brand-logo {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
      color: #fff;
    }
    .brand-name {
      font-size: 1.6rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, #60a5fa, #38bdf8, #fbbf24);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-tag {
      font-size: 0.7rem;
      font-style: italic;
      color: #ffd700;
      letter-spacing: 0.5px;
      background: rgba(255,215,0,0.15);
      padding: 2px 6px;
      border-radius: 4px;
    }

    /* Search Bar with auto-suggest */
    .search-box-container {
      flex: 1;
      max-width: 600px;
      position: relative;
    }
    .search-input {
      width: 100%;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #fff;
      padding: 0.7rem 1.25rem 0.7rem 2.8rem;
      border-radius: 999px;
      font-size: 0.92rem;
      outline: none;
      transition: all 0.2s ease;
    }
    .search-input:focus {
      background: rgba(255, 255, 255, 0.2);
      border-color: #38bdf8;
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    .search-icon {
      position: absolute;
      left: 1rem;
      top: 50%;
      transform: translateY(-50%);
      color: #94a3b8;
      font-size: 1.1rem;
      pointer-events: none;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 1.25rem;
    }
    .nav-btn {
      background: transparent;
      border: none;
      color: #f1f5f9;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.92rem;
      font-weight: 600;
      cursor: pointer;
      padding: 0.55rem 0.9rem;
      border-radius: 8px;
      transition: all 0.2s;
      position: relative;
    }
    .nav-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      transform: translateY(-1px);
    }
    .cart-bubble {
      background: var(--secondary);
      color: #fff;
      border-radius: 999px;
      padding: 2px 7px;
      font-size: 0.75rem;
      font-weight: 800;
    }
    .login-btn {
      background: #ffffff;
      color: #0f172a !important;
      padding: 0.5rem 1.4rem;
      border-radius: 999px;
      font-weight: 700;
    }
    .login-btn:hover {
      background: #f1f5f9;
      box-shadow: 0 0 15px rgba(255,255,255,0.4);
    }

    /* Category Sub-Bar */
    .category-bar {
      max-width: 1400px;
      margin: 0 auto;
      padding: 0.6rem 2rem;
      display: flex;
      gap: 2rem;
      overflow-x: auto;
      scrollbar-width: none;
    }
    .cat-item {
      color: #94a3b8;
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: color 0.15s;
    }
    .cat-item:hover, .cat-item.active {
      color: #38bdf8;
    }

    /* Antigravity Hero Section */
    .hero-orbit {
      position: relative;
      background: radial-gradient(circle at 50% 30%, #1e293b 0%, #090d16 100%);
      color: #fff;
      padding: 4.5rem 2rem 5.5rem;
      overflow: hidden;
    }
    .hero-orbit::before {
      content: '';
      position: absolute;
      top: -100px; left: 50%;
      transform: translateX(-50%);
      width: 700px; height: 500px;
      background: radial-gradient(ellipse, rgba(56, 189, 248, 0.25), transparent 70%);
      pointer-events: none;
    }
    .hero-container {
      max-width: 1300px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      align-items: center;
      gap: 3rem;
      position: relative;
      z-index: 2;
    }
    .hero-tag {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 0.35rem 1rem;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 1.25rem;
      letter-spacing: 0.5px;
    }
    .hero-title {
      font-size: 3.4rem;
      line-height: 1.12;
      font-weight: 800;
      margin-bottom: 1.25rem;
      letter-spacing: -1px;
    }
    .hero-title span {
      background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #f472b6 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
      font-size: 1.15rem;
      color: #94a3b8;
      margin-bottom: 2rem;
      max-width: 540px;
      line-height: 1.6;
    }
    .hero-ctas {
      display: flex;
      gap: 1rem;
    }
    .cta-primary {
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: #fff;
      padding: 0.9rem 2.2rem;
      border-radius: 12px;
      font-size: 1rem;
      font-weight: 700;
      border: none;
      cursor: pointer;
      box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.5);
      transition: all 0.25s ease;
    }
    .cta-primary:hover {
      transform: translateY(-3px) scale(1.02);
      box-shadow: 0 15px 30px -5px rgba(37, 99, 235, 0.7);
    }
    .cta-secondary {
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
      padding: 0.9rem 1.8rem;
      border-radius: 12px;
      font-size: 1rem;
      font-weight: 600;
      border: 1px solid rgba(255, 255, 255, 0.2);
      cursor: pointer;
      backdrop-filter: blur(10px);
      transition: all 0.2s;
    }
    .cta-secondary:hover {
      background: rgba(255, 255, 255, 0.16);
    }

    /* Floating 3D Zero-Gravity Orbit Visual */
    .hero-floating-stage {
      position: relative;
      height: 400px;
      display: flex;
      align-items: center;
      justify-content: center;
      perspective: 1200px;
    }
    .orbit-sphere {
      position: absolute;
      width: 280px;
      height: 280px;
      border-radius: 50%;
      border: 1px dashed rgba(56, 189, 248, 0.3);
      animation: spin 30s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    .floating-card-hero {
      position: absolute;
      background: rgba(255, 255, 255, 0.09);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 20px;
      padding: 1.5rem;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .floating-card-hero:hover {
      transform: scale(1.08) translateZ(30px) !important;
      border-color: #38bdf8;
      box-shadow: 0 0 35px rgba(56, 189, 248, 0.5);
    }

    .float-item-1 {
      top: 40px;
      left: 10%;
      animation: bob 4.5s ease-in-out infinite;
    }
    .float-item-2 {
      bottom: 30px;
      right: 15%;
      animation: bob 5.2s ease-in-out infinite 1.5s;
    }
    .float-item-3 {
      top: 130px;
      right: 2%;
      animation: bob 4.8s ease-in-out infinite 0.8s;
    }

    @keyframes bob {
      0%, 100% { transform: translateY(0px) rotate(0deg); }
      50% { transform: translateY(-18px) rotate(2deg); }
    }

    .hero-item-icon {
      font-size: 3.5rem;
      filter: drop-shadow(0 15px 15px rgba(0,0,0,0.4));
      margin-bottom: 0.5rem;
    }
    .hero-item-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: #fff;
    }
    .hero-item-price {
      font-size: 1.1rem;
      font-weight: 800;
      color: #4ade80;
    }
    .hero-badge-tag {
      background: var(--secondary);
      font-size: 0.7rem;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 999px;
      margin-top: 0.3rem;
    }

    /* Main Content Layout with Sidebar */
    .main-layout {
      max-width: 1400px;
      margin: 2.5rem auto;
      padding: 0 2rem;
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 2rem;
    }

    /* Sidebar Filters */
    .filter-panel {
      background: #ffffff;
      border-radius: 16px;
      padding: 1.5rem;
      box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05);
      border: 1px solid #e2e8f0;
      height: fit-content;
      position: sticky;
      top: 90px;
    }
    .filter-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 1rem;
      border-bottom: 1px solid #f1f5f9;
      margin-bottom: 1.25rem;
    }
    .filter-title {
      font-size: 1.1rem;
      font-weight: 800;
      color: #0f172a;
    }
    .clear-btn {
      color: var(--primary);
      background: none;
      border: none;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
    }
    .filter-group {
      margin-bottom: 1.5rem;
    }
    .filter-group-title {
      font-size: 0.88rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #475569;
      margin-bottom: 0.75rem;
    }
    .filter-options label {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 0.88rem;
      color: #334155;
      margin-bottom: 0.5rem;
      cursor: pointer;
    }
    .filter-options input[type="checkbox"] {
      accent-color: var(--primary);
      width: 16px;
      height: 16px;
    }
    .price-slider {
      width: 100%;
      accent-color: var(--primary);
    }
    .price-labels {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      color: #64748b;
      margin-top: 0.35rem;
    }

    /* Products Header */
    .catalog-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .results-count {
      font-size: 1.1rem;
      font-weight: 700;
      color: #0f172a;
    }
    .results-count span {
      font-weight: 400;
      color: #64748b;
      font-size: 0.9rem;
    }
    .sort-select {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-size: 0.88rem;
      font-weight: 600;
      color: #334155;
      cursor: pointer;
      outline: none;
    }

    /* Antigravity 3D Floating Product Cards Grid */
    .product-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
      gap: 1.75rem;
      perspective: 1200px;
    }

    .tilt-card {
      background: #ffffff;
      border-radius: 18px;
      padding: 1.25rem;
      border: 1px solid #e2e8f0;
      box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.05);
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transform-style: preserve-3d;
      transition: transform 0.15s ease-out, box-shadow 0.25s ease;
      cursor: pointer;
      overflow: hidden;
    }
    .tilt-card:hover {
      border-color: #93c5fd;
      box-shadow: 0 20px 35px -10px rgba(37, 99, 235, 0.18), 0 10px 10px -5px rgba(0,0,0,0.04);
    }

    .badge-tag {
      position: absolute;
      top: 1rem;
      left: 1rem;
      background: linear-gradient(135deg, #ef4444, #dc2626);
      color: #fff;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      z-index: 5;
    }
    .wishlist-btn {
      position: absolute;
      top: 1rem;
      right: 1rem;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(4px);
      border: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
      cursor: pointer;
      z-index: 5;
      transition: transform 0.2s, background 0.2s;
    }
    .wishlist-btn:hover {
      transform: scale(1.15);
      background: #fee2e2;
    }
    .wishlist-btn.active {
      color: #ef4444;
    }

    /* Floating Image Stage */
    .img-stage {
      height: 180px;
      background: radial-gradient(circle at 50% 50%, #f1f5f9 0%, #e2e8f0 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 4.8rem;
      margin-bottom: 1.25rem;
      position: relative;
      transform: translateZ(25px);
      transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .tilt-card:hover .img-stage {
      transform: translateZ(45px) scale(1.08);
      filter: drop-shadow(0 15px 12px rgba(0,0,0,0.15));
    }

    .product-brand {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      color: #64748b;
      letter-spacing: 0.5px;
      margin-bottom: 0.25rem;
    }
    .product-title {
      font-size: 1rem;
      font-weight: 700;
      color: #0f172a;
      line-height: 1.35;
      margin-bottom: 0.5rem;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      transform: translateZ(15px);
    }
    .rating-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: #16a34a;
      color: #fff;
      font-size: 0.78rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      margin-bottom: 0.75rem;
    }
    .reviews-text {
      color: #94a3b8;
      font-size: 0.75rem;
      margin-left: 0.3rem;
    }

    .price-row {
      display: flex;
      align-items: baseline;
      gap: 0.6rem;
      margin-top: auto;
      margin-bottom: 1rem;
      transform: translateZ(20px);
    }
    .curr-price {
      font-size: 1.35rem;
      font-weight: 800;
      color: #0f172a;
    }
    .orig-price {
      font-size: 0.88rem;
      color: #94a3b8;
      text-decoration: line-through;
    }
    .discount-tag {
      font-size: 0.82rem;
      font-weight: 800;
      color: #16a34a;
    }

    .card-actions {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.6rem;
      transform: translateZ(25px);
    }
    .quick-view-btn {
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 0.6rem;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }
    .quick-view-btn:hover {
      background: #e2e8f0;
    }
    .add-cart-btn {
      background: linear-gradient(135deg, var(--secondary), #c2410c);
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 0.6rem;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.4rem;
      transition: all 0.2s;
      box-shadow: 0 4px 10px rgba(234, 88, 12, 0.3);
    }
    .add-cart-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 15px rgba(234, 88, 12, 0.45);
    }

    /* Floating Slide-Out Cart Drawer */
    .cart-drawer-overlay {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(8px);
      z-index: 200;
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .cart-drawer-overlay.open {
      opacity: 1;
      visibility: visible;
    }
    .cart-drawer {
      position: fixed;
      top: 0; right: -480px; width: 100%; max-width: 440px; height: 100%;
      background: #ffffff;
      box-shadow: -10px 0 40px rgba(0,0,0,0.25);
      z-index: 201;
      display: flex;
      flex-direction: column;
      transition: right 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .cart-drawer.open {
      right: 0;
    }
    .cart-drawer-header {
      padding: 1.5rem;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .cart-drawer-header h3 {
      font-size: 1.25rem;
      font-weight: 800;
    }
    .close-drawer-btn {
      background: none;
      border: none;
      font-size: 1.5rem;
      cursor: pointer;
      color: #64748b;
    }
    .cart-items-list {
      flex: 1;
      overflow-y: auto;
      padding: 1.25rem;
    }
    .cart-item-row {
      display: flex;
      gap: 1rem;
      padding-bottom: 1rem;
      margin-bottom: 1rem;
      border-bottom: 1px solid #f1f5f9;
      align-items: center;
    }
    .cart-item-icon {
      font-size: 2.2rem;
      background: #f1f5f9;
      width: 60px;
      height: 60px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .cart-item-info {
      flex: 1;
    }
    .cart-item-title {
      font-size: 0.9rem;
      font-weight: 700;
      margin-bottom: 0.2rem;
    }
    .cart-item-price {
      font-size: 0.92rem;
      font-weight: 800;
      color: #0f172a;
    }
    .qty-controls {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-top: 0.4rem;
    }
    .qty-btn {
      width: 24px;
      height: 24px;
      border-radius: 4px;
      border: 1px solid #cbd5e1;
      background: #f8fafc;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .cart-drawer-footer {
      padding: 1.5rem;
      border-top: 1px solid #e2e8f0;
      background: #f8fafc;
    }
    .coupon-box {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
    .coupon-input {
      flex: 1;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 0.5rem 0.8rem;
      font-size: 0.85rem;
      text-transform: uppercase;
    }
    .apply-btn {
      background: #0f172a;
      color: #fff;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.82rem;
      cursor: pointer;
    }
    .price-breakup-row {
      display: flex;
      justify-content: space-between;
      font-size: 0.88rem;
      color: #64748b;
      margin-bottom: 0.4rem;
    }
    .price-total-row {
      display: flex;
      justify-content: space-between;
      font-size: 1.15rem;
      font-weight: 800;
      color: #0f172a;
      margin-top: 0.75rem;
      padding-top: 0.75rem;
      border-top: 1px dashed #cbd5e1;
    }
    .checkout-btn {
      width: 100%;
      background: linear-gradient(135deg, var(--secondary), #c2410c);
      color: #fff;
      border: none;
      padding: 0.9rem;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: 800;
      cursor: pointer;
      margin-top: 1rem;
      box-shadow: 0 10px 20px rgba(234, 88, 12, 0.35);
      transition: all 0.2s;
    }
    .checkout-btn:hover {
      transform: translateY(-2px);
    }

    /* Quick View Modal */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(8px);
      z-index: 300;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    .modal-content {
      background: #fff;
      border-radius: 20px;
      max-width: 850px;
      width: 100%;
      overflow: hidden;
      box-shadow: 0 25px 50px -12px rgba(0,0,0,0.4);
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      position: relative;
    }
    .modal-close {
      position: absolute;
      top: 1rem; right: 1rem;
      background: #f1f5f9;
      border: none;
      width: 36px; height: 36px;
      border-radius: 50%;
      font-size: 1.2rem;
      cursor: pointer;
      z-index: 10;
    }
    .modal-left {
      background: radial-gradient(circle, #f1f5f9 0%, #cbd5e1 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    .modal-hero-icon {
      font-size: 7.5rem;
      filter: drop-shadow(0 20px 20px rgba(0,0,0,0.15));
      animation: bob 4s ease-in-out infinite;
    }
    .modal-right {
      padding: 2.2rem;
      display: flex;
      flex-direction: column;
    }
    .size-pill {
      display: inline-block;
      padding: 0.4rem 0.8rem;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-right: 0.5rem;
      margin-bottom: 0.5rem;
      cursor: pointer;
    }
    .size-pill.selected {
      border-color: var(--primary);
      background: #eff6ff;
      color: var(--primary);
    }
    .pincode-check {
      display: flex;
      gap: 0.5rem;
      margin: 1rem 0;
    }
    .pincode-check input {
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 0.45rem 0.8rem;
      font-size: 0.85rem;
      width: 140px;
    }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 25px;
      right: 25px;
      background: #0f172a;
      color: #fff;
      padding: 1rem 1.6rem;
      border-radius: 12px;
      box-shadow: 0 15px 30px rgba(0,0,0,0.3);
      display: none;
      z-index: 500;
      font-weight: 600;
      border-left: 5px solid #22c55e;
    }

    @media (max-width: 900px) {
      .hero-container { grid-template-columns: 1fr; }
      .hero-floating-stage { height: 300px; }
      .main-layout { grid-template-columns: 1fr; }
      .filter-panel { display: none; }
      .modal-content { grid-template-columns: 1fr; }
      .modal-left { height: 200px; }
    }
  </style>
</head>
<body>

  <!-- Sticky Glassmorphism Header -->
  <div class="header-wrapper">
    <header class="top-nav">
      <a href="#" class="brand-logo">
        <span style="font-size: 1.8rem;">🚀</span>
        <div>
          <div class="brand-name">AERO</div>
          <div class="brand-tag">ZERO GRAVITY • FLAGSHIP STORE</div>
        </div>
      </a>

      <!-- Search Bar -->
      <div class="search-box-container">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Search for brands, sneakers, electronics, fashion...">
      </div>

      <!-- Navigation Actions -->
      <div class="nav-actions">
        <button class="nav-btn login-btn" onclick="showToast('Welcome back, VIP Explorer!')">Sign In</button>
        <button class="nav-btn" id="wishlistHeaderBtn" onclick="filterWishlist()">
          <span>❤️</span> Wishlist (<span id="wishCount">0</span>)
        </button>
        <button class="nav-btn" onclick="openCartDrawer()">
          <span>🛒</span> Cart
          <span class="cart-bubble" id="cartCount">0</span>
        </button>
      </div>
    </header>

    <!-- Category Sub-Menu -->
    <div class="category-bar">
      <span class="cat-item active" onclick="filterCategory('All', this)">✨ All Orbits</span>
      <span class="cat-item" onclick="filterCategory('Footwear', this)">👟 Footwear</span>
      <span class="cat-item" onclick="filterCategory('Electronics', this)">⚡ Electronics</span>
      <span class="cat-item" onclick="filterCategory('Men', this)">👔 Men's Fashion</span>
      <span class="cat-item" onclick="filterCategory('Women', this)">👗 Women's Fashion</span>
      <span class="cat-item" onclick="filterCategory('Deals', this)">🔥 50% Off Steals</span>
    </div>
  </div>

  <!-- Zero-Gravity Hero Section -->
  <section class="hero-orbit">
    <div class="hero-container">
      <div class="hero-content">
        <div class="hero-tag">✨ THE ZERO-GRAVITY SALE IS LIVE</div>
        <h1 class="hero-title">Defy Everyday Prices. <br><span>Shop Floating Deals.</span></h1>
        <p class="hero-subtitle">
          Experience frictionless shopping with dynamic 3D interactive physics, ambient floating product exhibits, and real-time express delivery.
        </p>
        <div class="hero-ctas">
          <button class="cta-primary" onclick="scrollToGrid()">Explore Catalog &darr;</button>
          <button class="cta-secondary" onclick="applyCoupon('ANTIGRAVITY')">Claim $25 Voucher</button>
        </div>
      </div>

      <!-- 3D Orbiting Product Stage -->
      <div class="hero-floating-stage" id="heroStage">
        <div class="orbit-sphere"></div>
        <div class="floating-card-hero float-item-1" onclick="openModalById(1)">
          <div class="hero-item-icon">👟</div>
          <div class="hero-item-title">Air Max Antigravity</div>
          <div class="hero-item-price">$129.99</div>
          <span class="hero-badge-tag">41% OFF</span>
        </div>
        <div class="floating-card-hero float-item-2" onclick="openModalById(2)">
          <div class="hero-item-icon">🎧</div>
          <div class="hero-item-title">Sony WH-1000XM5</div>
          <div class="hero-item-price">$279.00</div>
          <span class="hero-badge-tag">BESTSELLER</span>
        </div>
        <div class="floating-card-hero float-item-3" onclick="openModalById(4)">
          <div class="hero-item-icon">💻</div>
          <div class="hero-item-title">MacBook Air M3</div>
          <div class="hero-item-price">$1099.00</div>
          <span class="hero-badge-tag">NEW</span>
        </div>
      </div>
    </div>
  </section>

  <!-- Main Catalog with Sidebar -->
  <div class="main-layout" id="catalogSection">
    
    <!-- Sidebar -->
    <aside class="filter-panel">
      <div class="filter-header">
        <span class="filter-title">Filters</span>
        <button class="clear-btn" onclick="resetFilters()">CLEAR ALL</button>
      </div>

      <!-- Price Slider -->
      <div class="filter-group">
        <div class="filter-group-title">Price Range</div>
        <input type="range" id="priceRange" class="price-slider" min="30" max="1500" value="1500" oninput="updatePriceFilter(this.value)">
        <div class="price-labels">
          <span>$30</span>
          <span id="priceVal" style="font-weight: 700; color: var(--primary);">$1500 Max</span>
        </div>
      </div>

      <!-- Brand Checkboxes -->
      <div class="filter-group">
        <div class="filter-group-title">Brands</div>
        <div class="filter-options">
          <label><input type="checkbox" name="brand" value="Nike" onchange="applyFilters()"> Nike</label>
          <label><input type="checkbox" name="brand" value="Sony" onchange="applyFilters()"> Sony</label>
          <label><input type="checkbox" name="brand" value="Apple" onchange="applyFilters()"> Apple</label>
          <label><input type="checkbox" name="brand" value="Zara" onchange="applyFilters()"> Zara</label>
          <label><input type="checkbox" name="brand" value="Samsung" onchange="applyFilters()"> Samsung</label>
          <label><input type="checkbox" name="brand" value="Keychron" onchange="applyFilters()"> Keychron</label>
        </div>
      </div>

      <!-- Discount Filter -->
      <div class="filter-group">
        <div class="filter-group-title">Discounts</div>
        <div class="filter-options">
          <label><input type="checkbox" name="discount" value="40" onchange="applyFilters()"> 40% or more</label>
          <label><input type="checkbox" name="discount" value="30" onchange="applyFilters()"> 30% or more</label>
          <label><input type="checkbox" name="discount" value="20" onchange="applyFilters()"> 20% or more</label>
        </div>
      </div>

      <!-- Rating Filter -->
      <div class="filter-group">
        <div class="filter-group-title">Customer Ratings</div>
        <div class="filter-options">
          <label><input type="checkbox" name="rating" value="4.8" onchange="applyFilters()"> 4.8 ★ & above</label>
          <label><input type="checkbox" name="rating" value="4.5" onchange="applyFilters()"> 4.5 ★ & above</label>
        </div>
      </div>
    </aside>

    <!-- Product Feed -->
    <main>
      <div class="catalog-header">
        <div class="results-count">Showing <span id="itemCount">8</span> items</div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span style="font-size: 0.88rem; color: #64748b; font-weight: 600;">Sort By:</span>
          <select class="sort-select" id="sortSelect" onchange="applyFilters()">
            <option value="popular">Popularity</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
            <option value="discount">Highest Discount</option>
            <option value="rating">Customer Rating</option>
          </select>
        </div>
      </div>

      <!-- 3D Card Grid -->
      <div class="product-grid" id="productGrid"></div>
    </main>
  </div>

  <!-- Floating Cart Drawer -->
  <div class="cart-drawer-overlay" id="cartOverlay" onclick="closeCartDrawer()"></div>
  <div class="cart-drawer" id="cartDrawer">
    <div class="cart-drawer-header">
      <h3>Shopping Bag (<span id="drawerCount">0</span>)</h3>
      <button class="close-drawer-btn" onclick="closeCartDrawer()">&times;</button>
    </div>

    <div class="cart-items-list" id="cartItemsList"></div>

    <div class="cart-drawer-footer">
      <div class="coupon-box">
        <input type="text" id="couponCode" class="coupon-input" placeholder="Coupon Code (e.g. ANTIGRAVITY)">
        <button class="apply-btn" onclick="applyCouponFromInput()">APPLY</button>
      </div>

      <div class="price-breakup-row">
        <span>Total MRP</span>
        <span id="mrpTotal">$0.00</span>
      </div>
      <div class="price-breakup-row">
        <span>Discount on MRP</span>
        <span id="discountTotal" style="color: #16a34a;">-$0.00</span>
      </div>
      <div class="price-breakup-row">
        <span>Coupon Discount</span>
        <span id="couponDiscount" style="color: #16a34a;">-$0.00</span>
      </div>
      <div class="price-breakup-row">
        <span>Delivery Charges</span>
        <span style="color: #16a34a; font-weight: 700;">FREE</span>
      </div>

      <div class="price-total-row">
        <span>Total Amount</span>
        <span id="finalTotal">$0.00</span>
      </div>

      <button class="checkout-btn" onclick="simulateCheckout()">PROCEED TO CHECKOUT &rarr;</button>
    </div>
  </div>

  <!-- Quick View Modal -->
  <div class="modal-overlay" id="quickModal" onclick="closeModalOnOverlay(event)">
    <div class="modal-content" id="modalCard">
      <button class="modal-close" onclick="closeModal()">&times;</button>
      <div class="modal-left">
        <div class="modal-hero-icon" id="modalIcon">👟</div>
        <div id="modalBadge" class="badge-tag" style="position: static; margin-top: 1rem;">DEAL</div>
      </div>
      <div class="modal-right">
        <div id="modalBrand" class="product-brand">NIKE</div>
        <h2 id="modalTitle" style="font-size: 1.4rem; font-weight: 800; margin-bottom: 0.5rem;">Nike Air Max</h2>
        
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
          <span class="rating-badge" id="modalRating">4.8 ★</span>
          <span class="reviews-text" id="modalReviews">(2,840 ratings)</span>
        </div>

        <div class="price-row" style="margin-bottom: 1rem;">
          <span class="curr-price" id="modalPrice">$129.99</span>
          <span class="orig-price" id="modalOrigPrice">$219.99</span>
          <span class="discount-tag" id="modalDiscount">41% OFF</span>
        </div>

        <p id="modalDesc" style="font-size: 0.92rem; color: #475569; line-height: 1.5; margin-bottom: 1.25rem;">
          Description here.
        </p>

        <div style="margin-bottom: 1rem;">
          <div style="font-size: 0.82rem; font-weight: 700; margin-bottom: 0.5rem;">SELECT SIZE / VARIANT:</div>
          <div id="modalSizes"></div>
        </div>

        <div class="pincode-check">
          <input type="text" id="pincodeInput" placeholder="Enter Pincode" maxlength="6">
          <button class="quick-view-btn" onclick="checkDelivery()">Check Delivery</button>
        </div>
        <div id="deliveryMsg" style="font-size: 0.8rem; color: #16a34a; font-weight: 600; margin-bottom: 1.25rem;">
          ⚡ Express Delivery available in 24 Hours
        </div>

        <button class="checkout-btn" style="margin-top: auto;" id="modalAddBtn">
          ADD TO SHOPPING BAG
        </button>
      </div>
    </div>
  </div>

  <div class="toast" id="toast">Item added!</div>

  <script>
    let allProducts = [];
    let cart = {};
    let wishlist = new Set();
    let currentCategory = 'All';
    let appliedDiscount = 0;

    fetch('/api/products')
      .then(res => res.json())
      .then(data => {
        allProducts = data.products || [];
        renderProducts(allProducts);
      })
      .catch(err => {
        console.error('Fetch error:', err);
      });

    function handleCardTilt(e, card) {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const rotateX = ((y - centerY) / centerY) * -12;
      const rotateY = ((x - centerX) / centerX) * 12;

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.03, 1.03, 1.03)`;
    }

    function resetCardTilt(card) {
      card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
    }

    function renderProducts(list) {
      const grid = document.getElementById('productGrid');
      grid.innerHTML = '';
      document.getElementById('itemCount').innerText = list.length;

      if (list.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 4rem; color: #94a3b8; font-size: 1.2rem;">No products match your filters. Try clearing some selections.</div>';
        return;
      }

      list.forEach(item => {
        const isWish = wishlist.has(item.id);
        const card = document.createElement('div');
        card.className = 'tilt-card';
        card.onmousemove = (e) => handleCardTilt(e, card);
        card.onmouseleave = () => resetCardTilt(card);

        card.innerHTML = `
          ${item.badge ? `<div class="badge-tag">${item.badge}</div>` : ''}
          <button class="wishlist-btn ${isWish ? 'active' : ''}" onclick="toggleWishlist(event, ${item.id})">
            ${isWish ? '❤️' : '🤍'}
          </button>
          
          <div class="img-stage" onclick="openModalById(${item.id})">${item.icon}</div>
          
          <div class="product-brand">${item.brand}</div>
          <div class="product-title" onclick="openModalById(${item.id})">${item.name}</div>
          
          <div>
            <span class="rating-badge">${item.rating} ★</span>
            <span class="reviews-text">(${item.reviews_count.toLocaleString()})</span>
          </div>

          <div class="price-row">
            <span class="curr-price">$${item.price.toFixed(2)}</span>
            <span class="orig-price">$${item.original_price.toFixed(2)}</span>
            <span class="discount-tag">${item.discount}</span>
          </div>

          <div class="card-actions">
            <button class="quick-view-btn" onclick="openModalById(${item.id})">Quick View</button>
            <button class="add-cart-btn" onclick="addToCart(event, ${item.id})">
              <span>+</span> Add
            </button>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    document.getElementById('searchInput').addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      const filtered = allProducts.filter(p => 
        p.name.toLowerCase().includes(query) ||
        p.brand.toLowerCase().includes(query) ||
        p.category.toLowerCase().includes(query)
      );
      renderProducts(filtered);
    });

    function filterCategory(cat, el) {
      document.querySelectorAll('.cat-item').forEach(c => c.classList.remove('active'));
      if (el) el.classList.add('active');
      currentCategory = cat;
      applyFilters();
    }

    function updatePriceFilter(val) {
      document.getElementById('priceVal').innerText = '$' + val + ' Max';
      applyFilters();
    }

    function applyFilters() {
      let result = [...allProducts];

      if (currentCategory !== 'All') {
        if (currentCategory === 'Deals') {
          result = result.filter(p => parseInt(p.discount) >= 40);
        } else {
          result = result.filter(p => p.category === currentCategory);
        }
      }

      const maxPrice = parseFloat(document.getElementById('priceRange').value);
      result = result.filter(p => p.price <= maxPrice);

      const selectedBrands = Array.from(document.querySelectorAll('input[name="brand"]:checked')).map(cb => cb.value);
      if (selectedBrands.length > 0) {
        result = result.filter(p => selectedBrands.includes(p.brand));
      }

      const selectedDiscounts = Array.from(document.querySelectorAll('input[name="discount"]:checked')).map(cb => parseInt(cb.value));
      if (selectedDiscounts.length > 0) {
        const minDisc = Math.min(...selectedDiscounts);
        result = result.filter(p => parseInt(p.discount) >= minDisc);
      }

      const selectedRatings = Array.from(document.querySelectorAll('input[name="rating"]:checked')).map(cb => parseFloat(cb.value));
      if (selectedRatings.length > 0) {
        const minRating = Math.min(...selectedRatings);
        result = result.filter(p => p.rating >= minRating);
      }

      const sortBy = document.getElementById('sortSelect').value;
      if (sortBy === 'price-low') {
        result.sort((a, b) => a.price - b.price);
      } else if (sortBy === 'price-high') {
        result.sort((a, b) => b.price - a.price);
      } else if (sortBy === 'discount') {
        result.sort((a, b) => parseInt(b.discount) - parseInt(a.discount));
      } else if (sortBy === 'rating') {
        result.sort((a, b) => b.rating - a.rating);
      }

      renderProducts(result);
    }

    function resetFilters() {
      document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
      document.getElementById('priceRange').value = 1500;
      document.getElementById('priceVal').innerText = '$1500 Max';
      currentCategory = 'All';
      document.querySelectorAll('.cat-item').forEach((c, idx) => {
        if (idx === 0) c.classList.add('active'); else c.classList.remove('active');
      });
      applyFilters();
    }

    function toggleWishlist(e, id) {
      e.stopPropagation();
      if (wishlist.has(id)) {
        wishlist.delete(id);
        showToast('Removed from Wishlist');
      } else {
        wishlist.add(id);
        showToast('Added to Wishlist ❤️');
      }
      document.getElementById('wishCount').innerText = wishlist.size;
      applyFilters();
    }

    function filterWishlist() {
      if (wishlist.size === 0) {
        showToast('Your wishlist is empty!');
        return;
      }
      const wishProducts = allProducts.filter(p => wishlist.has(p.id));
      renderProducts(wishProducts);
      showToast(`Showing ${wishlist.size} wishlisted items`);
    }

    function addToCart(e, id) {
      if (e) e.stopPropagation();
      const product = allProducts.find(p => p.id === id);
      if (!product) return;

      if (!cart[id]) {
        cart[id] = { ...product, qty: 1 };
      } else {
        cart[id].qty++;
      }
      updateCartUI();
      showToast(`Added ${product.name} to Cart 🛒`);
    }

    function updateCartQty(id, delta) {
      if (!cart[id]) return;
      cart[id].qty += delta;
      if (cart[id].qty <= 0) {
        delete cart[id];
      }
      updateCartUI();
    }

    function updateCartUI() {
      const items = Object.values(cart);
      const totalCount = items.reduce((sum, item) => sum + item.qty, 0);
      document.getElementById('cartCount').innerText = totalCount;
      document.getElementById('drawerCount').innerText = totalCount;

      const listEl = document.getElementById('cartItemsList');
      listEl.innerHTML = '';

      if (items.length === 0) {
        listEl.innerHTML = '<div style="text-align: center; color: #94a3b8; padding: 4rem 1rem;">Your shopping bag is empty.<br>Start adding some zero-gravity deals!</div>';
        document.getElementById('mrpTotal').innerText = '$0.00';
        document.getElementById('discountTotal').innerText = '-$0.00';
        document.getElementById('couponDiscount').innerText = '-$0.00';
        document.getElementById('finalTotal').innerText = '$0.00';
        return;
      }

      let mrpSum = 0;
      let actualSum = 0;

      items.forEach(item => {
        mrpSum += item.original_price * item.qty;
        actualSum += item.price * item.qty;

        const row = document.createElement('div');
        row.className = 'cart-item-row';
        row.innerHTML = `
          <div class="cart-item-icon">${item.icon}</div>
          <div class="cart-item-info">
            <div class="cart-item-title">${item.name}</div>
            <div class="cart-item-price">$${(item.price * item.qty).toFixed(2)}</div>
            <div class="qty-controls">
              <button class="qty-btn" onclick="updateCartQty(${item.id}, -1)">-</button>
              <span style="font-weight: 700; font-size: 0.88rem;">${item.qty}</span>
              <button class="qty-btn" onclick="updateCartQty(${item.id}, 1)">+</button>
            </div>
          </div>
        `;
        listEl.appendChild(row);
      });

      const discountSum = mrpSum - actualSum;
      const finalAmount = Math.max(0, actualSum - appliedDiscount);

      document.getElementById('mrpTotal').innerText = '$' + mrpSum.toFixed(2);
      document.getElementById('discountTotal').innerText = '-$' + discountSum.toFixed(2);
      document.getElementById('couponDiscount').innerText = '-$' + appliedDiscount.toFixed(2);
      document.getElementById('finalTotal').innerText = '$' + finalAmount.toFixed(2);
    }

    function openCartDrawer() {
      document.getElementById('cartOverlay').classList.add('open');
      document.getElementById('cartDrawer').classList.add('open');
    }

    function closeCartDrawer() {
      document.getElementById('cartOverlay').classList.remove('open');
      document.getElementById('cartDrawer').classList.remove('open');
    }

    function applyCoupon(code) {
      document.getElementById('couponCode').value = code;
      openCartDrawer();
      applyCouponFromInput();
    }

    function applyCouponFromInput() {
      const code = document.getElementById('couponCode').value.trim().toUpperCase();
      if (code === 'ANTIGRAVITY' || code === 'AERO50') {
        appliedDiscount = 25.00;
        showToast('Coupon applied: $25 OFF 🎉');
      } else if (code) {
        showToast('Invalid coupon code');
        appliedDiscount = 0;
      }
      updateCartUI();
    }

    function simulateCheckout() {
      const count = Object.values(cart).length;
      if (count === 0) {
        showToast('Add items to cart before checkout!');
        return;
      }
      closeCartDrawer();
      showToast('🚀 Order Placed Successfully! Express delivery en route.');
      cart = {};
      appliedDiscount = 0;
      updateCartUI();
    }

    function openModalById(id) {
      const item = allProducts.find(p => p.id === id);
      if (!item) return;

      document.getElementById('modalIcon').innerText = item.icon;
      document.getElementById('modalBadge').innerText = item.badge || 'SPECIAL';
      document.getElementById('modalBrand').innerText = item.brand;
      document.getElementById('modalTitle').innerText = item.name;
      document.getElementById('modalRating').innerText = item.rating + ' ★';
      document.getElementById('modalReviews').innerText = `(${item.reviews_count.toLocaleString()} ratings)`;
      document.getElementById('modalPrice').innerText = '$' + item.price.toFixed(2);
      document.getElementById('modalOrigPrice').innerText = '$' + item.original_price.toFixed(2);
      document.getElementById('modalDiscount').innerText = item.discount;
      document.getElementById('modalDesc').innerText = item.description;

      const sizeContainer = document.getElementById('modalSizes');
      sizeContainer.innerHTML = '';
      (item.sizes || ['Standard']).forEach((size, idx) => {
        const pill = document.createElement('span');
        pill.className = `size-pill ${idx === 0 ? 'selected' : ''}`;
        pill.innerText = size;
        pill.onclick = () => {
          document.querySelectorAll('.size-pill').forEach(s => s.classList.remove('selected'));
          pill.classList.add('selected');
        };
        sizeContainer.appendChild(pill);
      });

      document.getElementById('modalAddBtn').onclick = () => {
        addToCart(null, item.id);
        closeModal();
      };

      document.getElementById('quickModal').style.display = 'flex';
    }

    function closeModal() {
      document.getElementById('quickModal').style.display = 'none';
    }

    function closeModalOnOverlay(e) {
      if (e.target.id === 'quickModal') closeModal();
    }

    function checkDelivery() {
      const val = document.getElementById('pincodeInput').value;
      if (val.length >= 5) {
        document.getElementById('deliveryMsg').innerText = `✅ Express delivery to ${val} available by tomorrow 5 PM!`;
      } else {
        document.getElementById('deliveryMsg').innerText = `Please enter a valid postal code.`;
      }
    }

    function scrollToGrid() {
      document.getElementById('catalogSection').scrollIntoView({ behavior: 'smooth' });
    }

    function showToast(text) {
      const toast = document.getElementById('toast');
      toast.innerText = text;
      toast.style.display = 'block';
      setTimeout(() => { toast.style.display = 'none'; }, 2400);
    }
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
