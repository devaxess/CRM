FROM python:3.9
MAINTAINER prasanth <mohanprasanth.ravi@axesstechnology.in>
ENV DJANGO_SETTINGS_MODULE=rest.settings
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN apt-get update
RUN apt-get install -y python3 python3-pip default-libmysqlclient-dev
RUN pip3 install -r requirements.txt
RUN pip3 install django
RUN pip3 install djangorestframework
RUN pip3 install django-cors-headers
WORKDIR /app
copy ./app . 
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
EXPOSE 8001

