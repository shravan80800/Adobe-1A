# Use Python 3.10 base
FROM python:3.10-slim

# Create working directory
WORKDIR /app

# Copy all files
COPY . .

# Create input/output folders
RUN mkdir -p /app/input /app/output

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Preload model (so it works offline)
#RUN python downloadmodel.py

# Set default command
CMD ["python", "main.py"]
