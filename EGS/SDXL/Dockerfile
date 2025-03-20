FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Clone ComfyUI repository
RUN git clone https://github.com/comfyanonymous/ComfyUI .

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install PyTorch with CUDA support
RUN pip3 install --no-cache-dir torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

# Install ComfyUI requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Install additional common dependencies for stable diffusion
RUN pip3 install --no-cache-dir opencv-python-headless transformers accelerate scipy safetensors

# Create directories for models
RUN mkdir -p /app/models/checkpoints \
    /app/models/clip \
    /app/models/configs \
    /app/models/controlnet \
    /app/models/embeddings \
    /app/models/loras \
    /app/models/upscale_models \
    /app/models/vae \
    /app/models/unet \
    /app/input \
    /app/output

# Expose the default port
EXPOSE 8188

# Set the entrypoint
ENTRYPOINT ["python3", "main.py", "--listen", "0.0.0.0", "--port", "8188"]
