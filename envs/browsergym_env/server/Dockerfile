
# Use the official Playwright Python image for browser support
FROM mcr.microsoft.com/playwright/python:v1.58.0-noble


# Set working directory to match package structure
WORKDIR /app/env


# Install only extra system packages needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-unifont \
    fonts-noto-color-emoji \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Copy environment files (Docker context: envs/browsergym_env/)
COPY . .


# Make start script executable
RUN chmod +x /app/env/server/start.sh


# Install Python dependencies using pip with hash-checking for reproducibility if requirements.txt is present
COPY server/requirements.txt ./server/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r ./server/requirements.txt \
    && pip install --no-cache-dir -e .


# Install MiniWoB++ from a pinned snapshot for reproducibility
ARG MINIWOB_COMMIT=7fd85d71a4b60325c6585396ec4f48377d049838
RUN mkdir -p /app/miniwob-plusplus && \
    curl -L "https://github.com/Farama-Foundation/miniwob-plusplus/archive/${MINIWOB_COMMIT}.tar.gz" \
    | tar -xz --strip-components=1 -C /app/miniwob-plusplus


# Set environment variables for reproducibility and clarity
ENV PYTHONUNBUFFERED=1 \
    BROWSERGYM_BENCHMARK=miniwob \
    BROWSERGYM_TASK_NAME="click-test" \
    BROWSERGYM_HEADLESS=true \
    BROWSERGYM_VIEWPORT_WIDTH=1280 \
    BROWSERGYM_VIEWPORT_HEIGHT=720 \
    BROWSERGYM_TIMEOUT=10000 \
    BROWSERGYM_PORT=8000 \
    MINIWOB_HTML_DIR=/app/miniwob-plusplus/miniwob/html \
    MINIWOB_HTTP_PORT=8888 \
    MINIWOB_URL=http://127.0.0.1:8888/miniwob/ \
    ENABLE_WEB_INTERFACE=true

# For WebArena tasks, these should be set by the user when running the container:
# ENV SHOPPING=
# ENV SHOPPING_ADMIN=
# ENV REDDIT=
# ENV GITLAB=
# ENV MAP=
# ENV WIKIPEDIA=
# ENV HOMEPAGE=


# Expose required ports
EXPOSE 8000 8888


# Health check for container
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1


# Run the server using the start script
CMD ["/app/env/server/start.sh"]
