# Launches Real NGINX and E-Commerce Microservice for live demo

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Starting Real NGINX & Microservice Pipeline    " -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Start Real Microservice on Port 5001
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", ".venv\Scripts\activate; python services/real_ecommerce_service.py"

# 2. Start Real NGINX Web Server on Port 8080
Start-Process -FilePath "c:\Acentra_Hackathon\nginx_dist\nginx-1.26.2\nginx.exe" -ArgumentList "-p c:\Acentra_Hackathon\nginx_dist\nginx-1.26.2"

Write-Host "Real Services are LIVE:" -ForegroundColor Yellow
Write-Host " -> NGINX Reverse Proxy:   http://127.0.0.1:8080" -ForegroundColor White
Write-Host " -> E-Commerce Service:    http://127.0.0.1:5001" -ForegroundColor White
Write-Host " -> Sentinel Backend:      http://127.0.0.1:8000" -ForegroundColor White
Write-Host " -> React Dashboard:       http://localhost:5173" -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Cyan
