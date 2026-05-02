FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and other necessary modules
# Note: Since the app structure imports from agents/ and memory/ at the same level as backend,
# we need to copy them to /app as well.
COPY backend/ ./backend/
COPY agents/ ./agents/
COPY memory/ ./memory/

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
