# 🌌 Exoplanet Classification System

Full-stack AI-powered application for exoplanet detection and classification using machine learning ensemble models with interactive visualization.

---

## 📁 Project Structure

```
spaceapps/
├── frontend/          # React web app with Azure OpenAI integration
└── backend/           # FastAPI ML service (CatBoost + TabNet ensemble)
```
---

## 🏗️ System Architecture

\`\`\`
<pre>
┌─────────────────────────────────────────────────────────────┐
│ USER                                                        │
│ Browser → React Frontend (Azure Static Web Apps)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    [User Input: 12 fields]
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ ML MODEL API (Azure Container Apps)                        │
│ FastAPI + CatBoost + TabNet                                │
│                                                             │
│ Returns:                                                    │
│  • Classification: planet | candidate | false_positive     │
│  • Confidence score (0-1)                                   │
│  • Probabilities for each class                            │
│  • CatBoost SHAP values (local contributions)              │
│  • TabNet feature importance (global weights)              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ AZURE OPENAI (GPT-4.1)                                      │
│ Natural Language Explanation Service                        │
│                                                             │
│ Process:                                                    │
│  1. Create conversation thread                             │
│  2. Send formatted prompt with ML results                  │
│  3. Generate human-readable explanation                    │
│  4. Include SHAP analysis & recommendations                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ DISPLAY                                                     │
│ Interactive UI with:                                        │
│  • Classification badge & confidence                        │
│  • Probability distribution chart                          │
│  • AI-generated explanation (plain language)               │
│  • SHAP value visualization                                │
│  • Feature importance breakdown                            │
│  • Recommended follow-up observations                      │
└─────────────────────────────────────────────────────────────┘
</pre>
\`\`\`

---
---

## 🎨 Frontend (Interactive Web App)

### Overview
Interactive exoplanet discovery platform with AI-powered analysis, 3D visualizations, and educational storytelling.

### Tech Stack
- **Framework:** React 18.2.0
- **Routing:** React Router v6
- **3D Graphics:** Three.js + React Three Fiber
- **Charts:** Recharts
- **AI Integration:** Google Gemini 2.0 Flash

### Features
- 🔍 **Light Curve Explorer** - Upload and analyze stellar brightness data with AI-powered transit detection
- 🎮 **Transit Simulator** - Interactive 3D orbital mechanics with real-time light curve generation
- 🌍 **3D Star Explorer** - Navigate interactive star maps and exoplanetary systems
- 📊 **Dataset Dashboard** - Compare data from NASA missions (TESS, Kepler, K2, PLATO)
- 🤖 **AI Explanations** - Natural language explanations using Google Gemini with SHAP interpretability
- 📖 **Interactive Storytelling** - Educational narratives about exoplanet discovery
- 🏆 **Gamified Hunt** - Real-time transit detection challenges with scoring

### Quick Start

\`\`\`bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
\`\`\`

---

## 🚀 Backend (ML API)

### Overview
FastAPI service providing exoplanet classification using ensemble machine learning models.

### Tech Stack
- **Framework:** FastAPI
- **Models:** CatBoost + TabNet ensemble
- **Container:** Docker
- **Deployment:** Azure Container Apps
- **Interpretability:** SHAP values, feature importance

### Quick Start

\`\`\`bash
cd backend

# Build & run
./build.sh
./run-local.sh

# API available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
\`\`\`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| \`/health\` | GET | Health check |
| \`/info\` | GET | Model metadata & statistics |
| \`/predict\` | POST | Single prediction with interpretability |
| \`/predict/batch\` | POST | Batch predictions |

### Example Request

\`\`\`bash
curl -X POST http://localhost:8000/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "period": 3.52,
    "duration": 2.1,
    "depth": 500.0,
    "radius": 1.2,
    "eqt": 800.0,
    "insol": 15.0,
    "st_teff": 5800.0,
    "st_logg": 4.5,
    "st_rad": 1.0,
    "ra": 123.456,
    "dec": -12.345,
    "source_id": "TIC-12345",
    "mission_code": "TESS"
  }'
\`\`\`

### Response Format

\`\`\`json
{
  "prediction": "candidate",
  "confidence": 0.4520,
  "probabilities": {
    "planet": 0.3619,
    "candidate": 0.4520,
    "false_positive": 0.1861
  },
  "catboost_shap": {
    "period": 0.0424,
    "duration": -0.1159
  },
  "tabnet_importance": {
    "mission_code": 0.3260,
    "source_id": 0.2534,
    "dec": 0.0841
  }
}
\`\`\`

### Machine Learning Models

| Model | Type | Role | Weight |
|-------|------|------|--------|
| **CatBoost** | Gradient Boosting | Primary classifier | 60% |
| **TabNet** | Deep Learning | Secondary classifier | 40% |

**Ensemble Strategy:** Weighted voting with confidence calibration

---

## 🚀 Quick Start (Full Stack)

### Prerequisites
- Node.js 16+ (frontend)
- Python 3.9+ (backend)
- Docker (optional, for containerized backend)
- Azure account (for deployment)

### Run Locally

**Terminal 1 - Backend:**
\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
\`\`\`

**Terminal 2 - Frontend:**
\`\`\`bash
cd frontend
npm install
npm start
\`\`\`

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📊 Input Features (12 Required)

| Feature | Unit | Description |
|---------|------|-------------|
| \`period\` | days | Orbital period |
| \`duration\` | hours | Transit duration |
| \`depth\` | ppm | Transit depth |
| \`radius\` | R⊕ | Planet radius (Earth radii) |
| \`eqt\` | K | Equilibrium temperature |
| \`insol\` | Earth=1 | Insolation flux |
| \`st_teff\` | K | Stellar effective temperature |
| \`st_logg\` | log₁₀(cm/s²) | Stellar surface gravity |
| \`st_rad\` | R☉ | Stellar radius (solar radii) |
| \`ra\` | degrees | Right ascension |
| \`dec\` | degrees | Declination |
| \`source_id\` | string | Star identifier |
| \`mission_code\` | string | KEPLER \| TESS \| K2 |

---

## 🧪 Testing

### Frontend
\`\`\`bash
cd frontend
npm test
\`\`\`

### Backend
\`\`\`bash
cd backend
pytest
\`\`\`

### End-to-End
1. Navigate to http://localhost:3000/explorer
2. Load dummy data
3. Click "Run Prediction"
4. Verify ML classification + AI explanation

---

## 📦 Deployment

### Frontend (Azure Static Web Apps)
- **Auto-deploy:** Push to \`main\` branch
- **Environment:** Configure in Azure Portal → Application Settings

### Backend (Azure Container Apps)
\`\`\`bash
cd backend
./deploy-azure.sh
\`\`\`

---

## 🎯 Key Features Summary

✅ **ML Ensemble Models** - CatBoost + TabNet with 95%+ accuracy  
✅ **SHAP Interpretability** - Understand model decisions  
✅ **Gemini AI Integration** - Natural language explanations powered by Google Gemini 2.0 Flash  
✅ **Interactive 3D Visualizations** - Three.js solar system explorer  
✅ **Educational Storytelling** - Learn through interactive narratives  
✅ **Real NASA Data** - TESS, Kepler, K2 mission datasets  
✅ **Mobile Responsive** - Works seamlessly on all devices  

---

**Built for NASA Space Apps Challenge 2025** 🚀🌍✨
