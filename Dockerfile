FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirement.sh .
RUN chmod +x requirement.sh
RUN ./requirement.sh

COPY . .

# Download Vosk model (English small model)
RUN curl -L -o vosk.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
RUN apt-get update && apt-get install -y unzip
RUN unzip vosk.zip
RUN rm vosk.zip

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
