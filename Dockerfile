FROM python:3.10-slim

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN apt-get update && \
    apt-get install imagemagick ffmpeg vim wget curl  -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && rm -rf /root/.cache/pip

# Copy the rest of the files
COPY . .

# Expose port 8080
EXPOSE 8080

# Run the app
CMD [ "python3", "main.py" ]
