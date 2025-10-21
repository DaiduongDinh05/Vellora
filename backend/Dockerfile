FROM python:3.13-slim

WORKDIR /backend

COPY requirements.txt /backend/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend/

EXPOSE 8000

#Similar to fastapi dev app/main.py, watches for reloads
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]