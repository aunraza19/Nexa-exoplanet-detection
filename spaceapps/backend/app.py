from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import numpy as np
import joblib
import pandas as pd
from catboost import CatBoostClassifier, Pool
from pytorch_tabnet.tab_model import TabNetClassifier
import os
import logging
from pathlib import Path

# Load .env file FIRST before anything else
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ[k] = v

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"GEMINI_API_KEY loaded: {bool(os.getenv('GEMINI_API_KEY'))}")

from gemini_service import get_gemini_service

app = FastAPI(
    title="Exoplanet Classification API",
    description="Ensemble model for exoplanet classification",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = os.getenv("MODEL_DIR", "Models")

numeric_cols = [
    'period', 'duration', 'depth', 'radius', 'eqt', 'insol',
    'st_teff', 'st_logg', 'st_rad', 'ra', 'dec'
]
categorical_cols = ['source_id', 'mission_code']

class ExoplanetInput(BaseModel):
    period: float = Field(..., description="Orbital period (days)")
    duration: float = Field(..., description="Transit duration (hours)")
    depth: float = Field(..., description="Transit depth (ppm)")
    radius: float = Field(..., description="Planet radius (Earth radii)")
    eqt: float = Field(..., description="Equilibrium temperature (K)")
    insol: float = Field(..., description="Insolation flux (relative to Earth)")
    st_teff: float = Field(..., description="Stellar temperature (K)")
    st_logg: float = Field(..., description="Stellar surface gravity (log10 cm/s²)")
    st_rad: float = Field(..., description="Stellar radius (Solar radii)")
    ra: float = Field(..., description="Right Ascension (degrees)")
    dec: float = Field(..., description="Declination (degrees)")
    source_id: str
    mission_code: str

    class Config:
        schema_extra = {
            "example": {
                "period": 289.86,
                "duration": 4.5,
                "depth": 150.0,
                "radius": 2.38,
                "eqt": 279.0,
                "insol": 0.89,
                "st_teff": 5518.0,
                "st_logg": 4.45,
                "st_rad": 0.98,
                "ra": 290.567,
                "dec": 44.280,
                "source_id": "Kepler-22",
                "mission_code": "KEPLER"
            }
        }

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    catboost_shap: Optional[Dict[str, float]] = None
    tabnet_importance: Optional[Dict[str, float]] = None

class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    version: str

cat_model = None
tabnet_model = None
scaler = None
label_encoder = None
source_encoder = None
mission_encoder = None

@app.on_event("startup")
async def load_models():
    global cat_model, tabnet_model, scaler, label_encoder, source_encoder, mission_encoder
    
    try:
        logger.info("Loading models and encoders...")
        
        cat_model = CatBoostClassifier()
        cat_model.load_model(f"{OUTPUT_DIR}/catboost_model.cbm")
        logger.info("✓ CatBoost loaded")
        
        tabnet_model = joblib.load(f"{OUTPUT_DIR}/tabnet_model.pkl")
        logger.info("✓ TabNet loaded")
        
        scaler = joblib.load(f"{OUTPUT_DIR}/tabnet_scaler.pkl")
        logger.info("✓ Scaler loaded")
        
        label_encoder = joblib.load(f"{OUTPUT_DIR}/label_encoder.pkl")
        source_encoder = joblib.load(f"{OUTPUT_DIR}/source_id_encoder.pkl")
        mission_encoder = joblib.load(f"{OUTPUT_DIR}/mission_code_encoder.pkl")
        logger.info("✓ Encoders loaded")
        
        # Initialize Gemini AI service
        gemini = get_gemini_service()
        logger.info("✓ Gemini AI service initialized")

        logger.info("🚀 All models loaded successfully!")
        
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")
        raise


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy",
        models_loaded=all([cat_model, tabnet_model, scaler, label_encoder]),
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    models_ok = all([cat_model, tabnet_model, scaler, label_encoder, source_encoder, mission_encoder])
    return HealthResponse(
        status="healthy" if models_ok else "unhealthy",
        models_loaded=models_ok,
        version="1.0.0"
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(data: ExoplanetInput):
    try:
        input_dict = data.dict()
        df = pd.DataFrame([input_dict])
        
        try:
            df['source_id'] = source_encoder.transform(df['source_id'].astype(str))
        except ValueError:
            df['source_id'] = 0
            
        try:
            df['mission_code'] = mission_encoder.transform(df['mission_code'].astype(str))
        except ValueError:
            df['mission_code'] = 0
        
        X_input = df[numeric_cols + categorical_cols]
        X_input_scaled = X_input.copy()
        X_input_scaled[numeric_cols] = scaler.transform(X_input[numeric_cols])
        
        cat_features_idx = [X_input.columns.get_loc(c) for c in categorical_cols]
        cat_pred_proba = cat_model.predict_proba(
            Pool(X_input, cat_features=cat_features_idx)
        )
        
        tabnet_pred_proba = tabnet_model.predict_proba(X_input_scaled.values)
        
        ensemble_proba = (cat_pred_proba + tabnet_pred_proba) / 2
        ensemble_pred_idx = np.argmax(ensemble_proba, axis=1)[0]
        ensemble_conf = np.max(ensemble_proba, axis=1)[0]
        
        predicted_class = label_encoder.inverse_transform([ensemble_pred_idx])[0]
        class_labels = label_encoder.classes_
        
        proba_dict = {
            label: float(prob) 
            for label, prob in zip(class_labels, ensemble_proba[0])
        }
        
        try:
            cat_shap_values = cat_model.get_feature_importance(
                Pool(X_input, cat_features=cat_features_idx),
                type='ShapValues'
            )
            shap_row = cat_shap_values[0, :-1, ensemble_pred_idx]
            shap_dict = {
                col: float(val) 
                for col, val in zip(X_input.columns, shap_row)
            }
            
            tabnet_importance = tabnet_model.feature_importances_
            importance_dict = {
                col: float(val)
                for col, val in zip(X_input.columns, tabnet_importance)
            }
        except Exception as e:
            shap_dict = None
            importance_dict = None
        
        return PredictionResponse(
            prediction=predicted_class,
            confidence=float(ensemble_conf),
            probabilities=proba_dict,
            catboost_shap=shap_dict,
            tabnet_importance=importance_dict
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch")
async def predict_batch(data: List[ExoplanetInput]):
    try:
        results = []
        for item in data:
            result = await predict(item)
            results.append(result)
        return results
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@app.get("/info")
async def model_info():
    return {
        "model_type": "Ensemble (CatBoost + TabNet)",
        "features": {
            "numeric": numeric_cols,
            "categorical": categorical_cols
        },
        "classes": list(label_encoder.classes_) if label_encoder else [],
        "description": "Exoplanet classification model",
        "gemini_enabled": bool(os.getenv('GEMINI_API_KEY'))
    }


# Gemini AI endpoints
class ExplanationRequest(BaseModel):
    prediction: Dict
    model_inputs: Dict


class ChatRequest(BaseModel):
    question: str
    prediction: Dict
    model_inputs: Dict


@app.post("/ai/explain")
async def generate_explanation(request: ExplanationRequest):
    """Generate AI explanation for prediction results"""
    try:
        logger.info("=== AI Explanation Request Received ===")
        logger.info(f"Prediction: {request.prediction.get('prediction', 'N/A')}")

        gemini = get_gemini_service()
        logger.info(f"Gemini service obtained: {gemini}")
        logger.info(f"Gemini has client: {gemini.client is not None if gemini else False}")

        explanation = gemini.generate_prediction_explanation(
            prediction=request.prediction,
            model_inputs=request.model_inputs
        )
        logger.info(f"Explanation generated, length: {len(explanation)}")
        return {"explanation": explanation}
    except Exception as e:
        logger.error(f"Explanation generation error: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=f"Failed to generate explanation: {str(e)}")


@app.post("/ai/chat")
async def chat_with_ai(request: ChatRequest):
    """Chat with AI about prediction results"""
    try:
        gemini = get_gemini_service()
        response = gemini.generate_chat_response(
            question=request.question,
            prediction=request.prediction,
            model_inputs=request.model_inputs
        )
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
