FROM python:latest

WORKDIR /code

COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python app.py"]
