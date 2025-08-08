# Usa imagem oficial Python slim
FROM python:3.11-slim

# Atualiza e instala dependências do sistema necessárias para pygame
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libsmpeg-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*


# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia arquivo de dependências
COPY requirements.txt .



# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para dentro do container
COPY . .

# Comando padrão para rodar o jogo (ajuste o nome do script se necessário)
CMD ["python", "game/game.py"]
