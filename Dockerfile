FROM python:3.8-slim

RUN mkdir -p /app/data
RUN apt-get update
RUN apt-get install -y git
RUN pip install --upgrade pip
RUN pip install discord.py mysql-connector-python

# get the word lists
# RUN git clone https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words.git
# RUN mv List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/en /app/data/en.txt
# RUN mv List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/es /app/data/es.txt

COPY nickel-jar.py /app/nickel-jar.py

WORKDIR /app

ENTRYPOINT [ "python", "/app/nickel-jar.py" ]
