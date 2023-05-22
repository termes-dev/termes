FROM python:3.10

WORKDIR /termes

COPY ./requirements.txt /termes/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /termes/requirements.txt

COPY ./src /termes/src

WORKDIR /termes/src

CMD ["uvicorn", "termes.application:app", "--host", "0.0.0.0", "--port", "8000"]