FROM python:3.11-slim
WORKDIR /app
COPY starter2/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY starter2/pyproject.toml /tmp/build/
COPY starter2/logiai/ /tmp/build/logiai/
RUN pip install --no-cache-dir --no-deps /tmp/build && rm -rf /tmp/build
ENV LOGIAI_HOME=/app
RUN python -m logiai.dataset && python -m logiai.train
EXPOSE 8000
CMD ["uvicorn", "logiai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
