# Use uma imagem base do Python
FROM python:3.10-slim

RUN apt-get update && apt-get install -y cron

# Define o diretório de trabalho dentro do container
WORKDIR /src

# Copie o arquivo de dependências
COPY ../requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto
COPY . .

# Comando padrão para rodar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]