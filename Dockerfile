FROM python:3.11-slim

WORKDIR /usr/local/app

RUN apt-get update -y;apt-get install openssh-client -y;apt-get install sshpass -y;

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    pkg-config \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --default-timeout=300 --retries=10 -r requirements.txt

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN pip install coqui-tts

RUN apt-get update && \
    apt-get install -y python3-dev python3-pip portaudio19-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyaudio

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsdl2-2.0-0 \
    libsdl2-mixer-2.0-0 \
    && rm -rf /var/lib/apt/lists/*


RUN ls 

COPY . .

RUN mkdir -p /root/.local/share/tts/tts_models--multilingual--multi-dataset--your_tts

RUN mv ./models/tts/tts_models--multilingual--multi-dataset--your_tts/* /root/.local/share/tts/tts_models--multilingual--multi-dataset--your_tts/

CMD ["python3","test_api_6.py"]