FROM python:3.11.4

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN \
    --mount=type=cache,target=/var/cache/apt \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENV PYTHONPATH /code/app
COPY ./*.py /code/app/
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "81"]