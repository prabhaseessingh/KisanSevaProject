# 🌾 KisanSeva — Empowering Modern Agriculture with Innovation

> Bridging traditional farming wisdom with cutting-edge technology to help Indian farmers reduce pesticide use, increase yields, and embrace sustainable practices.

---

## 🚀 What is KisanSeva?

KisanSeva is a full-stack web platform built for Indian farmers that combines AI-powered pest diagnosis, smart crop planning, an agro marketplace, community knowledge exchange, and eco-friendly solar pest control hardware — all in one place.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔬 AI Pest Diagnosis | Upload a crop photo → instant pest/disease ID + treatment plan using TensorFlow.js MobileNet (client-side inference) |
| 📅 Smart Crop Calendar | Region & season-aware planting schedules with MSP-based financial projections for 20+ crops |
| 💰 ROI Calculator | Calculate 5-year savings from switching to solar-powered pest control vs. traditional pesticides |
| 🛒 Agro Marketplace | Buy/sell agri-products with cart, multi-step checkout, and Razorpay payment integration (UPI, Card, Net Banking, COD) |
| 💬 Knowledge Exchange | Community forum with Elder's Wisdom cards, Q&A, and farming video tutorials |
| 🌍 Multi-Language Support | English, Hindi (हिंदी), Punjabi (ਪੰਜਾਬੀ), Tamil (தமிழ்), Marathi (मराठी) + voice navigation |
| ☀️ Solar Insect Trap | Flagship hardware product — 100% chemical-free, solar-powered pest trap |
| 👤 Auth System | User registration/login with hashed passwords, session management, and personalized dashboard |

---

## 🧠 The Problem We're Solving

Indian farmers spend **₹8,000–₹15,000 per acre per year** on chemical pesticides that:
- Degrade soil health over time
- Create health risks for farmers and consumers
- Lead to pest resistance, requiring ever-stronger chemicals
- Contribute to environmental pollution

KisanSeva offers a smarter, greener path forward.

---

## 💡 Our Solution — Solar Insect Trap

A one-time investment solar-powered trap that:
- Attracts and eliminates harmful insects using UV light
- Requires **zero chemicals** and **zero electricity costs**
- Has a **5+ year lifespan**
- Pays back its cost in under **6 months** for an average 2-acre farm

---

## 📊 Projected Impact (at scale)

| Metric | Projection |
|---|---|
| Farmers Benefited | 10,000+ |
| Pesticide Cost Savings | ₹5 Crore+ |
| Crop Loss Reduction | Up to 85% |
| Generations Connected | 3+ |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, SQLAlchemy |
| Database | SQLite (local) / PostgreSQL (production via `DATABASE_URL`) |
| Frontend | HTML5, CSS3, Vanilla JS |
| AI/ML | TensorFlow.js + MobileNet (client-side, no server GPU needed) |
| Payments | Razorpay SDK (UPI, Card, Net Banking, COD) |
| Auth | Flask sessions, Werkzeug password hashing |
| File Uploads | Werkzeug `secure_filename`, local `static/uploads/` |

---

## 🗂️ Project Structure

```
kisanseva/
├── app.py                      # Flask app — routes, models, auth, API
├── instance/
│   └── kisanseva.db            # SQLite database
├── static/
│   ├── style.css
│   ├── uploads/                # User-uploaded crop images
│   └── *.jpg                   # Product & demo images
└── templates/
    ├── login_landing.html          # Landing page + hero
    ├── login_register.html         # Auth (login + register)
    ├── ai_pest_diagnosis.html      # AI pest diagnosis tool
    ├── crop_calendar.html          # Smart crop planner (20+ crops, MSP data)
    ├── roi_calculator.html         # Savings calculator with visual breakdown
    ├── marketplace.html            # Agro marketplace with cart & checkout
    ├── knowledge_exchange.html     # Forum, elder wisdom, video tutorials
    ├── language_support.html       # Multi-language + voice navigation
    └── product_details.html        # Solar trap product page
```

---

## ⚡ Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/your-username/kisanseva.git
cd kisanseva

# 2. Install dependencies
pip install flask flask-sqlalchemy werkzeug

# 3. Run the app
python app.py
```

Open `http://localhost:5000` in your browser.

For production, set environment variables:
```bash
export DATABASE_URL=postgresql://...   # PostgreSQL connection string
export SECRET_KEY=your-secret-key
```

---

## 🔑 Key Routes

| Route | Description |
|---|---|
| `GET /` | Landing page |
| `GET/POST /login_register` | Auth page |
| `GET/POST /ai-pest-diagnosis` | AI pest diagnosis (POST returns JSON) |
| `GET /crop-calendar` | Crop calendar (filter by `?season=Rabi`) |
| `GET/POST /roi-calculator` | ROI calculator |
| `GET /marketplace` | Agro marketplace (filter by `?category=...`) |
| `GET/POST /marketplace/add` | Add a new listing |
| `GET/POST /knowledge-exchange` | Community forum |
| `GET /language_support` | Multi-language page |
| `GET /product_details` | Solar trap product page |

---

## 🌱 Roadmap

- [ ] WhatsApp / SMS pest outbreak alerts
- [ ] Weather API integration for smarter crop recommendations
- [ ] Mobile app (React Native)
- [ ] IoT integration with solar trap for real-time pest count data
- [ ] Government scheme eligibility checker
- [ ] Telugu, Kannada, Gujarati, Bengali language support

---

## 👥 Team

Built with ❤️ for farmers across India.

---

## 📄 License

MIT License — free to use, modify, and distribute.
