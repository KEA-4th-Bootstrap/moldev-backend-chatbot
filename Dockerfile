FROM python:3.11.9

COPY . /src
WORKDIR /src


COPY ./requirements.txt /src/requirements.txt

RUN pip3 install -r requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]