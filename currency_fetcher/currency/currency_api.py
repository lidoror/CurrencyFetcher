import json
from typing import Final
import requests
from currency_fetcher.log_factory import logger


class CurrencyFetcher:

    def __init__(self, url):
        self.url: str = url

    def get_url_data(self) -> dict:
        response = {}

        try:
            logger.info(f'request sent to {self.url.split("apikey")[0]}')
            response = requests.get(self.url)

        except requests.exceptions.RequestException as err:
            logger.error(f'An Error Occurred while sending the request:\nstatus code: [{err.response.status_code}] '
                         f'\nerror message: [{err.response}]')

        return json.loads(response.text)

    def get_account_status(self) -> str:
        logger.info('parsing the data to get account status')

        if 'status' not in self.url:
            logger.error('user tried to check status with wrong url endpoint')
            raise ValueError(f'cant fetch account status with this endpoint: [{self.url.split("apikey")[0]}]')

        json_response: dict = self.get_url_data()
        used_requests: str = json_response.get('quotas').get('month').get('used')
        remaining_requests: str = json_response.get('quotas').get('month').get('remaining')

        if used_requests is None or remaining_requests is None:
            logger.error('a problem occurred in get account status one or more of the value is None')
            return 'unable to fetch status data'

        status_message = f'this month you used_requests: [{used_requests}] requests and you have: ' \
                         f'[{remaining_requests}]requests remaining_requests'

        return status_message

    def get_currency_exchange_rate(self) -> str:
        logger.info('trying to fetch latest currency')
        ILS_VALUE_TO_EXCHANGE: Final = 1.0

        if 'latest' not in self.url:
            logger.error('user tried to check status with wrong url endpoint')
            raise ValueError('cant check the status of account with this usl endpoint')

        json_response: dict = self.get_url_data().get('data')
        currency_info: str = ''

        for currency_value in json_response.values():
            code: str = currency_value.get('code')
            exchange_rate: float = float(currency_value.get('value'))

            currency_info += f'Currency Name: {code}\nValue To ILS: {ILS_VALUE_TO_EXCHANGE / exchange_rate}\n'

        return currency_info
