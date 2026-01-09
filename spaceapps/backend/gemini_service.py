"""
Gemini AI Service for Exoplanet Analysis
Handles AI-powered explanations and chat functionality
"""

from google import genai
from google.genai import types
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class GeminiAIService:
    def __init__(self, api_key: str):
        """Initialize Gemini AI service with API key"""
        self.api_key = api_key

        if not self.api_key:
            logger.warning("⚠️ Gemini API key not provided")
            self.client = None
            return

        try:
            self.client = genai.Client(api_key=self.api_key)
            self.model_id = 'gemini-2.5-flash'
            logger.info("✅ Gemini AI initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
            self.client = None

    def _format_tabnet_importance(self, tabnet_importance: Dict[str, float]) -> str:
        """Format TabNet importance for prompt"""
        if not tabnet_importance:
            return "Not available"

        sorted_features = sorted(tabnet_importance.items(), key=lambda x: x[1], reverse=True)[:5]
        return "\n".join([f"  - {feature}: {importance*100:.2f}%" for feature, importance in sorted_features])

    def _format_shap_values(self, shap_values: Dict[str, float]) -> str:
        """Format SHAP values for prompt"""
        if not shap_values:
            return "Not available"

        formatted = []
        for feature, value in shap_values.items():
            direction = "increases" if value > 0 else "decreases"
            formatted.append(f"  - {feature}: {direction} prediction confidence by {abs(value):.4f}")
        return "\n".join(formatted)

    def generate_prediction_explanation(
        self,
        prediction: Dict[str, Any],
        model_inputs: Dict[str, Any]
    ) -> str:
        """Generate detailed explanation for exoplanet classification prediction"""
        if not self.client:
            return self._generate_fallback_explanation(prediction, model_inputs)

        # Format TabNet importance
        tabnet_importance_str = self._format_tabnet_importance(
            prediction.get('tabnet_importance', {})
        )

        # Format SHAP values
        shap_values_str = self._format_shap_values(
            prediction.get('catboost_shap', {})
        )

        # Get probabilities
        probabilities = prediction.get('probabilities', {})
        planet_prob = float(probabilities.get('planet', 0)) * 100
        candidate_prob = float(probabilities.get('candidate', 0)) * 100
        false_positive_prob = float(probabilities.get('false_positive', 0)) * 100

        # Create comprehensive prompt
        prompt = f"""You are Nexus2, an expert AI astronomer and exoplanet scientist working with the NEXA exoplanet detection system. Your role is to provide clear, engaging, and scientifically accurate explanations of exoplanet classification results.

CLASSIFICATION RESULTS:
====================
Prediction: {prediction.get('prediction', 'Unknown')}
Confidence: {float(prediction.get('confidence', 0)):.1f}%

Probability Distribution:
- Planet: {planet_prob:.1f}%
- Candidate: {candidate_prob:.1f}%
- False Positive: {false_positive_prob:.1f}%

TOP INFLUENTIAL FEATURES (TabNet Importance):
============================================
{tabnet_importance_str}

FEATURE CONTRIBUTIONS (SHAP Values - CatBoost):
============================================
{shap_values_str}

INPUT PARAMETERS:
===============
Source: {model_inputs.get('source_id', 'Unknown')} (Mission: {model_inputs.get('mission_code', 'Unknown')})

Orbital Properties:
- Period: {model_inputs.get('period', 'N/A')} days
- Transit Duration: {model_inputs.get('duration', 'N/A')} hours
- Transit Depth: {model_inputs.get('depth', 'N/A')} ppm

Planetary Properties:
- Radius: {model_inputs.get('radius', 'N/A')} Earth radii
- Equilibrium Temperature: {model_inputs.get('eqt', 'N/A')} K
- Insolation Flux: {model_inputs.get('insol', 'N/A')} (Earth = 1.0)

Stellar Properties:
- Effective Temperature: {model_inputs.get('st_teff', 'N/A')} K
- Surface Gravity: {model_inputs.get('st_logg', 'N/A')} (log g)
- Radius: {model_inputs.get('st_rad', 'N/A')} (Solar radii)

YOUR TASK:
=========
Provide a comprehensive, engaging analysis that includes:

1. **Classification Summary** (2-3 sentences)
   - Clearly state what the AI classified this as and why
   - Mention the confidence level and what it means

2. **Scientific Interpretation** (3-4 sentences)
   - What do these parameters tell us about this object?
   - Is this consistent with known exoplanets or candidates?
   - What physical processes are at play here?

3. **Feature Importance Analysis** (2-3 sentences)
   - Explain why the top TabNet features were most influential
   - How did these features contribute to the decision?

4. **SHAP Value Insights** (2-3 sentences)
   - Interpret the SHAP values - which features pushed toward or away from this classification?
   - What does this tell us about the model's reasoning?

5. **Recommendations** (2-3 sentences)
   - If Planet/Candidate: What follow-up observations would be valuable?
   - If False Positive: What likely caused this signal?

STYLE GUIDELINES:
================
- Use clear, accessible language
- Be enthusiastic yet scientifically rigorous
- Use markdown formatting for better readability
- Explain technical terms when first used

Begin your response with a compelling opening!"""

        try:
            logger.info("📨 Sending prediction explanation request to Gemini...")
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )

            logger.info("✅ Received explanation from Gemini")
            return response.text

        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}")
            return self._generate_fallback_explanation(prediction, model_inputs)

    def generate_chat_response(
        self,
        question: str,
        prediction: Dict[str, Any],
        model_inputs: Dict[str, Any]
    ) -> str:
        """Generate contextual chat response about the prediction"""
        if not self.client:
            return self._generate_fallback_chat(question, prediction)

        # Get probabilities and confidence
        probabilities = prediction.get('probabilities', {})
        planet_prob = float(probabilities.get('planet', 0)) * 100
        candidate_prob = float(probabilities.get('candidate', 0)) * 100
        false_positive_prob = float(probabilities.get('false_positive', 0)) * 100
        confidence = float(prediction.get('confidence', 0))

        prompt = f"""You are Nexus2, an expert AI astronomer providing follow-up insights on an exoplanet detection analysis.

PREVIOUS CLASSIFICATION:
======================
Classification: {prediction.get('prediction', 'Unknown')}
Confidence: {confidence:.1f}%

Probabilities:
- Planet: {planet_prob:.1f}%
- Candidate: {candidate_prob:.1f}%
- False Positive: {false_positive_prob:.1f}%

KEY PARAMETERS:
=============
Source: {model_inputs.get('source_id', 'Unknown')} ({model_inputs.get('mission_code', 'Unknown')} mission)
Period: {model_inputs.get('period', 'N/A')} days
Depth: {model_inputs.get('depth', 'N/A')} ppm
Radius: {model_inputs.get('radius', 'N/A')} Earth radii
Temperature: {model_inputs.get('eqt', 'N/A')} K

USER QUESTION:
============
{question}

YOUR TASK:
=========
Provide a helpful, educational response that:
- Directly answers the user's question
- References the specific classification and data
- Uses clear, accessible language
- Is scientifically accurate
- Is concise (3-5 sentences maximum)"""

        try:
            logger.info("💬 Sending chat request to Gemini...")
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=512,
                )
            )

            logger.info("✅ Received chat response from Gemini")
            return response.text

        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}")
            return self._generate_fallback_chat(question, prediction)

    def _generate_fallback_explanation(self, prediction: Dict[str, Any], model_inputs: Dict[str, Any]) -> str:
        """Fallback explanation when Gemini is unavailable"""
        classification = prediction.get('prediction', 'unknown')
        confidence = float(prediction.get('confidence', 0))

        probabilities = prediction.get('probabilities', {})
        planet_prob = float(probabilities.get('planet', 0)) * 100
        candidate_prob = float(probabilities.get('candidate', 0)) * 100
        false_positive_prob = float(probabilities.get('false_positive', 0)) * 100

        return f"""## 🔬 Classification Analysis

The NEXA AI model has classified this detection as a **{classification}** with {confidence:.1f}% confidence.

### 📊 Probability Distribution
- **Planet:** {planet_prob:.1f}%
- **Candidate:** {candidate_prob:.1f}%
- **False Positive:** {false_positive_prob:.1f}%

### 🌟 Key Parameters
- **Source:** {model_inputs.get('source_id', 'Unknown')} ({model_inputs.get('mission_code', 'Unknown')} mission)
- **Orbital Period:** {model_inputs.get('period', 'N/A')} days
- **Transit Depth:** {model_inputs.get('depth', 'N/A')} ppm
- **Planet Radius:** {model_inputs.get('radius', 'N/A')} Earth radii
- **Equilibrium Temperature:** {model_inputs.get('eqt', 'N/A')} K

*Note: AI explanation service is temporarily unavailable. This is a basic analysis based on the model output.*"""

    def _generate_fallback_chat(self, question: str, prediction: Dict[str, Any]) -> str:
        """Fallback chat response when Gemini is unavailable"""
        classification = prediction.get('prediction', 'unknown')
        confidence = float(prediction.get('confidence', 0))

        return f"""Based on the classification of **{classification}** ({confidence:.1f}% confidence), I can provide some insights. However, the AI chat service is temporarily unavailable. 

For detailed analysis, please refer to the main explanation above.

*Note: Full AI chat functionality requires the Gemini API service to be available.*"""


# Global service instance
gemini_service = None


def get_gemini_service() -> GeminiAIService:
    """Get or create Gemini AI service instance"""
    global gemini_service

    if gemini_service is None:
        api_key = os.getenv('GEMINI_API_KEY')
        gemini_service = GeminiAIService(api_key)

    return gemini_service

