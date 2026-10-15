FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Hash-pinned runtime dependencies only; test tooling stays out of the image.
COPY requirements.lock .
RUN pip install --no-cache-dir --require-hashes -r requirements.lock

RUN useradd --system --uid 10001 --no-create-home --home-dir /nonexistent \
	--shell /usr/sbin/nologin databix

# Application code stays root-owned and read-only to the runtime user.
COPY . .
RUN mkdir -p /app/data && chown databix /app/data

USER databix

VOLUME ["/app/data"]
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
