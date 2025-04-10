FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py"]
