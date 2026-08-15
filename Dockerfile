FROM public.ecr.aws/docker/library/python:3.12-slim

WORKDIR /app
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    build-essential \
    checkinstall \
    curl \
    make \
    git \
    libz-dev \
    zlib1g-dev \
    wget \
    openssl \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    fonts-dejavu \
    fonts-ipafont-gothic \
    fonts-ipafont-mincho \
    fonts-noto-cjk \
    fonts-noto-cjk-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:${PATH}"

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY . .
EXPOSE 80

ENV PYTHONUNBUFFERED=1
CMD [
  "uv", "run",
  "adk", "api_server",
  "--host", "0.0.0.0",
  "--port", "80",
  "agents"
]