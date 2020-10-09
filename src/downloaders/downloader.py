import abc
import requests
import json
from datetime import date
import wbdata


class Downloader(metaclass=abc.ABCMeta):
    def __init__(self, API_URL):
        self.API_URL = API_URL
        return None

    @abc.abstractmethod
    def get_raw_data(self, params):
        pass

    def get_data(self, params):
        data = self.get_raw_data(params)
        metadata = {'URL': self.API_URL, 'DownloadDate': str(date.today())}

        result = {}
        result['data'] = data
        result['metadata'] = metadata

        return result

    def download_data(self, path, params):

        data = self.get_data(params)

        with open(path, 'w') as file:
            json.dump(data, file)
        return None


class CW_Downloader(Downloader):

    def get_raw_data(self, params):
        first_request = requests.get(self.API_URL, params=params)
        data = first_request.json()['data']

        if 'next' in first_request.links.keys():
            has_next = True
            next_url = first_request.links['next']['url']
        else:
            has_next = False

        while has_next:
            next_request = requests.get(next_url)
            data += (next_request.json()['data'])

            if 'next' in next_request.links.keys():
                next_url = next_request.links['next']['url']
            else:
                has_next = False

        return data


class SDG_Downloader(Downloader):

    def get_raw_data(self, params):

        params['pageSize'] = int(1e9)
        request = requests.get(self.API_URL, params=params)
        data = request.json()['data']
        return data


class WB_Downloader(Downloader):

    def get_raw_data(self, params):
        indicator = params['indicator']
        url = f'{self.API_URL}/{indicator}'
        params = {'format': 'json', 'per_page': 1}
        # request to get the number of element and make a full request
        pre_request = requests.get(url, params=params)

        total = pre_request.json()[0]['total']
        params['per_page'] = total

        # actual request

        request = requests.get(url, params=params)

        data = request.json()

        data[0]['Source'] = wbdata.get_indicator(indicator)[0]['sourceOrganization']  # Well maybe we could just use wbdata alltogether :/

        return data
