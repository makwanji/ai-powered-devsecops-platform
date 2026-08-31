FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    KUBECONFIG=/app/.kube/config

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

RUN useradd --create-home --uid 10001 mcpuser \
    && mkdir -p /app/.kube \
    && chown -R mcpuser:mcpuser /app

USER mcpuser

EXPOSE 8001

CMD ["python", "server.py"]
