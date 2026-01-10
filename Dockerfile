# Use python 3.10
FROM python:3.10-slim

# Install system dependencies (ffmpeg for audio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user (required by HF Spaces for some security policies)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements first to leverage cache
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application
COPY --chown=user . /app

# Expose the Gradio port
EXPOSE 7860

# Command to run the app
CMD ["python", "gradio_app.py"]
