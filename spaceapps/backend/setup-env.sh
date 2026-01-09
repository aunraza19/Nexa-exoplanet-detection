#!/bin/bash
echo "✨ Setup complete!"
echo ""
echo "3. Test at: http://localhost:8000/docs"
echo "2. Start backend: uvicorn app:app --reload --port 8000"
echo "1. Install dependencies: pip install google-generativeai python-dotenv"
echo "🚀 Next steps:"
echo ""
cat .env
echo "📝 Contents:"
echo ""
echo "✅ .env file created successfully!"
echo ""

EOF
MODEL_DIR=Models
GEMINI_API_KEY=$GEMINI_KEY
# Backend Environment Variables
cat > .env << EOF
# Create .env file

fi
    exit 1
    echo "❌ No API key provided. Setup cancelled."
if [ -z "$GEMINI_KEY" ]; then

read -p "API Key: " GEMINI_KEY
echo "(Get it from: https://aistudio.google.com/app/apikey)"
echo "🔑 Please enter your Gemini API key:"
# Prompt for Gemini API key

fi
    fi
        exit 1
        echo "❌ Setup cancelled."
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo
    read -p "Do you want to overwrite it? (y/n): " -n 1 -r
    echo "⚠️  .env file already exists!"
if [ -f ".env" ]; then
# Check if .env already exists

echo ""
echo "===================="
echo "🚀 NEXA Backend Setup"

# Setup script for NEXA backend environment

