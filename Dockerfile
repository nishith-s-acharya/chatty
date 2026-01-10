# Use standard Python 3.10 image (not slim) to ensure all build tools are present
FROM python:3.10

# Install system dependencies (ffmpeg for audio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set entrypoint to bash to ensure environment is loaded
SHELL ["/bin/bash", "-c"]

# Create a non-root user
RUN useradd -m -u 1000 user

# Switch to user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy requirements
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application
COPY --chown=user . $HOME/app

EXPOSE 7860

CMD ["python", "gradio_app.py"]
