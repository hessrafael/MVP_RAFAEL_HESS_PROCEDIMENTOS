# Define a imagem base
FROM python:3.10.6

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos para o diretorio de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte para o diretório de trabalho
COPY . .

# Cria variável de ambiente para dizer que está utilizando Docker
ENV DOCKER_ENV 'true'

# Define o comando de execução da API
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5002"]