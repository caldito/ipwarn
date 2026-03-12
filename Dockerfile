FROM python:3.12-slim

LABEL maintainer="pablo@caldito.me"

# Install uv for dependency management
RUN pip install --no-cache-dir uv

# Create application directory
WORKDIR /app

# Copy application files
COPY pyproject.toml /app/
COPY ipwarn/ /app/ipwarn/

# Install dependencies and package using uv
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install /app

# Add venv to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Create config directory
RUN mkdir -p /etc/ipwarn

# Copy default config
COPY config/ipwarn.conf.example /etc/ipwarn/ipwarn.conf

# Set entrypoint
CMD ["ipwarn", "--config", "/etc/ipwarn/ipwarn.conf"]
