FROM python:3.7-slim

RUN mkdir -p /app/data
RUN pip install discord.py

COPY nickel-jar.py /app/nickel-jar.py

WORKDIR /app

ENTRYPOINT [ "python", "/app/nickel-jar.py" ]
