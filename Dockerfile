FROM python:3.11-slim
WORKDIR /app/
ADD src /app/
ADD Pipfile* /app/
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pipenv install --dev --system --ignore-pipfile
RUN cd /app/
CMD ["python3", "main.py"]