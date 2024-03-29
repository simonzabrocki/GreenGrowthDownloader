import abc
import requests
import json
from datetime import date
import wbdata


class Downloader(metaclass=abc.ABCMeta):
    '''
    Abstract class used to download data coming from an API
    '''
    def __init__(self, API_URL):
        self.API_URL = API_URL
        return None

    @abc.abstractmethod
    def get_raw_data(self, params):
        '''
        Download the raw data

        Parameters
        ---------
        params: dictionnary
            dictionnary with the API parameters
        '''
        pass

    def get_data(self, params):
        '''
        Fetch the raw data and add timestamp and origin

        Parameters
        ---------
        params: dictionnary
            dictionnary with the API parameters
        '''
        data, url = self.get_raw_data(params)
        metadata = {'URL': url, 'DownloadDate': str(date.today())}
        result = {'data': data, 'metadata' : metadata}
        return result

    def download_data(self, path, params):
        '''
        Fetch the data and save it at path

        Parameters
        ---------
        path: str
            Path to save file
        params: dictionnary
            dictionnary with the API parameters
        '''

        data = self.get_data(params)

        with open(path, 'w') as file:
            json.dump(data, file)

        return data


class CW_Downloader(Downloader):
    '''
    Class to download data coming from CW API
    '''
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

        return data, first_request.url


class SDG_Downloader(Downloader):
    '''
    Class to download data coming from SDG API
    '''
    def get_raw_data(self, params):

        params['pageSize'] = int(1e9)  # Set large number to get all the data, avoid 2 calls
        request = requests.get(self.API_URL, params=params)
        data = request.json()['data']
        return data, request.url


class WB_Downloader(Downloader):
    '''
    Class to download data coming from WB API
    '''
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

        # add source
        data[0]['Source'] = wbdata.get_indicator(indicator)[0]['sourceOrganization']  # Well maybe we could just use wbdata alltogether :/

        return data, request.url
    
    
class OECD_Downloader(Downloader):
    '''
    Class to download data coming from OECD API
    '''
    def get_raw_data(self, params):
        mandatory = params['mandatory']
        optional = params['optional']
        url = f"{self.API_URL}/{mandatory['dataSet']}/{mandatory['filter']}/{mandatory['agency']}"

        response = requests.get(url, params=optional)

        return response.json(), response.url
