# PowerShell Setup Script for NEXA Backend

Write-Host "`n🚀 NEXA Backend Setup" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host ""

# Check if .env already exists
if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/n)"
    if ($overwrite -ne "y") {
        Write-Host "❌ Setup cancelled." -ForegroundColor Red
        exit
    }
}

# Prompt for Gemini API key
Write-Host "🔑 Please enter your Gemini API key:" -ForegroundColor Cyan
Write-Host "(Get it from: https://aistudio.google.com/app/apikey)" -ForegroundColor Gray
$GEMINI_KEY = Read-Host "API Key"

if ([string]::IsNullOrWhiteSpace($GEMINI_KEY)) {
    Write-Host "❌ No API key provided. Setup cancelled." -ForegroundColor Red
    exit
}

# Create .env file
$envContent = @"
# Backend Environment Variables
GEMINI_API_KEY=$GEMINI_KEY
MODEL_DIR=Models
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8

Write-Host ""
Write-Host "✅ .env file created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Contents:" -ForegroundColor Yellow
Get-Content ".env"
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Cyan
Write-Host "1. Install dependencies: pip install google-generativeai python-dotenv" -ForegroundColor White
Write-Host "2. Start backend: uvicorn app:app --reload --port 8000" -ForegroundColor White
Write-Host "3. Test at: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "✨ Setup complete!" -ForegroundColor Green

