FROM python:3.12-slim

LABEL maintainer="pablo@caldito.me"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy application files
COPY ipwarn/ /app/ipwarn/
COPY pyproject.toml /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir .

# Create config directory
RUN mkdir -p /etc/ipwarn

# Copy default config
COPY config/ipwarn.conf.example /etc/ipwarn/ipwarn.conf

# Set entrypoint
CMD ["python", "-m", "ipwarn", "--config", "/etc/ipwarn/ipwarn.conf"]
