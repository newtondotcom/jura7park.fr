FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 80
COPY ./starte.sh /code/
RUN chmod +x /code/starte.sh
ENTRYPOINT ["/code/starte.sh"]
