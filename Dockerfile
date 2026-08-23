# Use the official Microsoft Playwright image which includes Python and all browser dependencies
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Playwright browsers are installed for the python package
RUN playwright install chromium

COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the API (which will also start the scheduler in the background)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
