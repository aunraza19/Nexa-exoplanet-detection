# 🚀 NEXA Setup Guide - Gemini AI Integration

## Overview
Your NEXA project now uses **Google Gemini 2.0 Flash** for AI-powered exoplanet explanations instead of Azure OpenAI.

---

## ✨ What Changed

### ✅ Added
- **frontend/src/services/geminiAIAgent.js** - New Gemini AI service
- Gemini API integration for natural language explanations
- Contextual chat with AI astronomer "Nexus2"

### 🔄 Modified
- **LightCurveExplorer.js** - Now uses Gemini instead of Azure
- **.env.example** - Added Gemini API key configuration
- **README.md** - Updated documentation

---

## 🔑 Getting Your Gemini API Key

### Step 1: Visit Google AI Studio
Go to: https://aistudio.google.com/app/apikey

### Step 2: Sign In
Sign in with your Google account

### Step 3: Create API Key
1. Click "Create API Key"
2. Select a Google Cloud project (or create a new one)
3. Copy the generated API key

### Step 4: Keep it Secure
⚠️ **Never commit your API key to Git!**
- Add it to `.env` file (already in .gitignore)
- Don't share it publicly

---

## 📦 Setup Instructions

### 1. Configure Frontend

Create `frontend/.env` file:
```bash
cd frontend
cp .env.example .env
```

Edit `frontend/.env`:
```env
# Backend API URL (default for local development)
REACT_APP_API_URL=http://localhost:8000

# Gemini AI API Key (get from https://aistudio.google.com/app/apikey)
REACT_APP_GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 2. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
./run-local.sh
# Or: uvicorn app:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

---

## 🎯 Testing the AI Integration

### Test 1: Prediction with AI Explanation
1. Go to http://localhost:3000/explorer
2. Click "Load Dummy Data"
3. Click "Run Prediction"
4. Wait for AI explanation (uses Gemini)

### Test 2: Chat with AI
1. After getting a prediction
2. Type a question like:
   - "Why is this classified as a planet?"
   - "What does the equilibrium temperature tell us?"
   - "How confident is the model?"
3. Get AI-powered contextual response

---

## 🔧 Gemini Configuration

### Model Details
- **Model:** `gemini-2.0-flash-exp`
- **Temperature:** 0.7 (balanced creativity/accuracy)
- **Max Tokens:** 2048
- **Features:** 
  - Contextual conversations
  - SHAP interpretation
  - Scientific explanations
  - Follow-up Q&A

### API Limits (Free Tier)
- **Rate Limit:** 15 requests per minute
- **Daily Quota:** 1,500 requests per day
- **Token Limit:** 1M tokens per minute

### Error Handling
If Gemini API fails:
- ✅ Automatic fallback to local generation
- ✅ User sees fallback explanation
- ✅ No app crash

---

## 🐛 Troubleshooting

### Issue: "Gemini API Key is missing"
**Solution:** Make sure you:
1. Created `.env` file in `frontend/` directory
2. Added `REACT_APP_GEMINI_API_KEY=your_key`
3. Restarted the frontend server

### Issue: "API request failed: 400"
**Possible Causes:**
- Invalid API key
- API key not activated
- Rate limit exceeded

**Solution:**
1. Verify API key at https://aistudio.google.com/app/apikey
2. Wait a minute if rate limited
3. Check browser console for detailed error

### Issue: "No valid response from Gemini"
**Solution:**
- Check internet connection
- Verify API key is active
- Check Gemini API status
- App will use fallback explanation

### Issue: Backend API connection failed
**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify .env has correct URL
# REACT_APP_API_URL=http://localhost:8000
```

---

## 📊 Comparison: Azure vs Gemini

| Feature | Azure OpenAI | Gemini 2.0 Flash |
|---------|--------------|------------------|
| **Cost** | Paid ($$$) | Free tier available |
| **Speed** | ~2-3 seconds | ~1-2 seconds |
| **Context** | 128K tokens | 1M tokens |
| **Setup** | Complex (Azure account, subscription) | Simple (Google account) |
| **Rate Limits** | Based on subscription | 15 req/min (free) |
| **Quality** | GPT-4.1 | Gemini 2.0 Flash |

---

## 🔐 Security Best Practices

### ✅ DO:
- Store API keys in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables
- Regenerate keys if exposed

### ❌ DON'T:
- Commit `.env` to Git
- Share API keys publicly
- Hardcode keys in code
- Use same key for dev/prod

---

## 🚀 Deployment Notes

### For Production Deployment:

1. **Environment Variables:**
   - Set `REACT_APP_GEMINI_API_KEY` in your hosting platform
   - Set `REACT_APP_API_URL` to your backend URL

2. **Vercel/Netlify:**
   ```bash
   # Add in dashboard:
   REACT_APP_API_URL=https://your-backend-url.com
   REACT_APP_GEMINI_API_KEY=your_production_key
   ```

3. **Docker:**
   ```bash
   docker run -e REACT_APP_GEMINI_API_KEY=your_key ...
   ```

---

## 📚 Additional Resources

- **Gemini API Docs:** https://ai.google.dev/docs
- **Get API Key:** https://aistudio.google.com/app/apikey
- **Pricing:** https://ai.google.dev/pricing
- **Rate Limits:** https://ai.google.dev/gemini-api/docs/rate-limits

---

## ✨ Features Working with Gemini

### ✅ Fully Functional:
- Initial prediction explanation
- SHAP value interpretation
- TabNet importance analysis
- Contextual follow-up questions
- Scientific accuracy
- Markdown formatting
- Error handling with fallback

### 🎯 Example Questions You Can Ask:
- "Explain the SHAP values"
- "What makes this a good planet candidate?"
- "How does the transit depth affect classification?"
- "What follow-up observations would you recommend?"
- "Compare this to other known exoplanets"

---

## 🎉 Success!

Your NEXA project now has AI-powered explanations using Google Gemini! The system:
- ✅ No longer depends on Azure
- ✅ Uses free Gemini API
- ✅ Provides smart contextual responses
- ✅ Has automatic fallback
- ✅ Works entirely locally

**Next Steps:**
1. Get your Gemini API key
2. Add it to `.env`
3. Start exploring exoplanets with AI assistance! 🚀

