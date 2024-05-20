FROM python:3.9

COPY . /src
WORKDIR /src


COPY ./requirements/requirements.txt /src/requirements.txt

RUN pip3 install  --no-cache-dir -r /src/requirements.txt


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]