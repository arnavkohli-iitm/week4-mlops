# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY main.py .
COPY predict.py .

# 6. Expose the port the app will run on
EXPOSE 8000

# 7. Define the command to run your app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]