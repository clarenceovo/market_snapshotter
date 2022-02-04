FROM python:3.8

EXPOSE 8443
WORKDIR /code


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ .

CMD [ "python", "app.py" ]