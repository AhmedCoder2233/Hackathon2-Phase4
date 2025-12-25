# Stage 1: Builder
FROM python:3.13-slim-bookworm AS builder

# Install uv
RUN pip install uv

# Set up a work directory
WORKDIR /app

# Copy dependency definition files
COPY backend/pyproject.toml backend/uv.lock ./

# Install dependencies
RUN uv sync

# Stage 2: Final
FROM python:3.13-slim-bookworm AS final

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Copy application code
COPY backend/app /app/app

# Expose port
EXPOSE 8000

# Set the default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
