# Dockerfile

# Use official slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only requirements first → better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir fastapi uvicorn   # for dummy server

# Copy the rest of the code
COPY . .


# Run bot.py 
CMD ["python", "bot.py"]