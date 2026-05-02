# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; if (!(Test-Path '..\venv')) { python -m venv ..\venv }; ..\venv\Scripts\activate; pip install -r ..\requirements.txt; uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd ai-virtual-doctor-ui; npm install; npm run dev"

Write-Host "Services are starting in new windows!"
Write-Host "Backend API will be at: http://localhost:8000"
Write-Host "Frontend UI will be at: http://localhost:5173"
