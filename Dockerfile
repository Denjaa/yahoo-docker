FROM ubuntu
COPY requirements.txt scrape_and_save_stocks.py  .
RUN apt-get update && apt-get upgrade
RUN apt-get install -y python3
RUN apt-get install -y python3-pip && apt-get install -y python3-setuptools
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["scrape_and_save_stocks.py"]