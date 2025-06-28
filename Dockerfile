# Use TensorFlow GPU image with Python 3.9 and CUDA
FROM tensorflow/tensorflow:2.13.0-gpu

# Set UTF-8 encoding for compatibility
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Set working directory inside container
WORKDIR /app

# Install system dependencies for PyCBC
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    libfftw3-dev \
    libgsl-dev \
    libhdf5-dev \
    libopenblas-dev \
    liblapack-dev \
    pkg-config \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (e.g., notebooks, data, code)
COPY . .

# Expose port for Jupyter Notebook
EXPOSE 8888

# Launch Jupyter Notebook server
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
