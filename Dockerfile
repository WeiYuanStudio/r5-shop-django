FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /r5-shop-django
COPY requirements.txt /r5-shop-django/
RUN pip install -r requirements.txt
COPY . /r5-shop-django/

EXPOSE 8080
CMD python3 manage.py runserver 0.0.0.0:8080
