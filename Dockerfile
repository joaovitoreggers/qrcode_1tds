# Usar uma imagem base do Python
FROM python:3.12-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Criar e definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependências
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar o código da aplicação
COPY . /app/

# Rodar o collectstatic para coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Comando para iniciar o servidor Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]

# Expor a porta que o Django irá usar
EXPOSE 8000
