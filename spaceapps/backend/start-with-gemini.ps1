# NEXA Backend Startup Script with Gemini API Key
# Run this script to start the backend with Gemini AI enabled

# Set Gemini API Key
$env:GEMINI_API_KEY = "AIzaSyDuHVeWI8XWcwn87R1UJ4bQy_UUKmlHEac"

Write-Host "`n🚀 Starting NEXA Backend with Gemini AI..." -ForegroundColor Cyan
Write-Host "API Key: $($env:GEMINI_API_KEY.Substring(0,10))...`n" -ForegroundColor Green

# Start uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

