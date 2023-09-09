FROM python:alpine3.18


WORKDIR /CurrencyFetcher

COPY currncy_fetcher /CurrencyFetcher

RUN pip install -r currncy_fetcher/requirments.txt

CMD ["python3", "-m", "currency_fetcher.main"]