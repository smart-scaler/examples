
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y         python3         python3-pip         python3-dev         git &&         apt-get clean && rm -rf /var/lib/apt/lists/*

# Install NVIDIA PyTorch dependencies
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Set the working directory
WORKDIR /app

# Copy the PyTorch script into the container
COPY fine_tune.py /app/fine_tune.py

# Install Python dependencies (if a requirements.txt exists)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements.txt found"

# Set the default command to run the script
CMD ["python3", "fine_tune.py"]
