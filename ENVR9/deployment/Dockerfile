FROM python:3.13-slim

WORKDIR /app

COPY backend/requirements_envr9.txt .
RUN pip install --no-cache-dir -r requirements_envr9.txt

COPY . .

EXPOSE 8000

CMD ["python", "backend/fastapi_server.py"]
