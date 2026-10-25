FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpcap-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast, reliable dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency specifications
COPY requirements.txt ./

# Install Python dependencies
RUN uv pip install --system -r requirements.txt pytest

# Copy codebase
COPY . .

# Run test suite by default
CMD ["pytest", "-v"]
