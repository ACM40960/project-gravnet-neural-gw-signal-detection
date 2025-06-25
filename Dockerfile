#Using python 3.9 as base image
FROM python:3.9-slim

#Setting up working directory
WORKDIR /app

#Install system dependencies
RUN apt-get update && apt-get install -y\
    gcc \
    g++ \
    gfortran \
    libfftw3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

#Copying requirements file
COPY requirements.txt .

#Install pytthon packages
RUN pip install --no-cache-dir -r requirements.txt

#Copy project files
COPY . .

#Exposing port for Jupyter 
EXPOSE 8888

#Default command
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]