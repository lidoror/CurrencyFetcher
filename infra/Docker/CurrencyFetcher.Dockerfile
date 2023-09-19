FROM python:alpine3.18


WORKDIR /CurrencyFetcher

COPY currncy_fetcher/* /CurrencyFetcher

RUN pip install -r CurrencyFetcher/requirments.txt

CMD ["python3", "-m", "CurrencyFetcher.main"]