
import argparse
import json
import pandas as pd
from colorama import Fore, init
from src.downloaders.downloader import CW_Downloader, SDG_Downloader, WB_Downloader


def download(API_params, folder_path, downloader):
    init(autoreset=True)

    for d in API_params:
        params = d['params']
        path = f"{folder_path}/{d['GGI_code']}.json"

        print(f'Fetching from {downloader.API_URL} with parameters: ')
        [print(f'{key}: {params[key]}') for key in params.keys()]

        try:
            downloader.download_data(path, params)
            print(Fore.GREEN + 'Done')
        except Exception as e:
            print(Fore.RED + 'Something went wrong: ', e)


def download_script():

    with open('params/APIs/CW.json', 'r') as file:
        CW_params = json.load(file)
    with open('params/APIs/SDG.json', 'r') as file:
        SDG_params = json.load(file)
    with open('params/APIs/WB.json', 'r') as file:
        WB_params = json.load(file)

    download(CW_params, 'data/CW_API',
             CW_Downloader(API_URL='https://www.climatewatchdata.org/api/v1/data/historical_emissions'))
    download(SDG_params, 'data/SDG_API',
             SDG_Downloader(API_URL='https://unstats.un.org/SDGAPI/v1/sdg/Series/Data'))
    download(WB_params, 'data/WB_API',
             WB_Downloader(API_URL='https://api.worldbank.org/v2/country/all/indicator/'))


if __name__ == '__main__':

    download_script()
