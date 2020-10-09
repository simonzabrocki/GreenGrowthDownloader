import json
import argparse

from ggdata.downloaders.downloader import SDG_Downloader
from ggdata.downloaders.downloader import WB_Downloader
from ggdata.downloaders.downloader import CW_Downloader

from ggdata.preprocessors.SDG_preprocessor import SDG_Preprocessor
from ggdata.preprocessors.WB_preprocessor import WB_Preprocessor
from ggdata.preprocessors.CW_preprocessor import CW_Preprocessor

from colorama import Fore, init

meta_configs = {

    'WB': {
        'API': 'WB API',
        'URL': 'https://api.worldbank.org/v2/country/all/indicator/',
        'config': 'ggdata/params/WB.json',
        'downloader': WB_Downloader,
        'preprocessor': WB_Preprocessor,
    },
    'SDG': {
        'API': 'SDG API',
        'URL': 'https://unstats.un.org/SDGAPI/v1/sdg/Series/Data',
        'downloader': SDG_Downloader,
        'config': 'ggdata/params/SDG.json',
        'preprocessor': SDG_Preprocessor,
    },
    'CW': {
        'API': 'CW API',
        'URL': 'https://www.climatewatchdata.org/api/v1/data/historical_emissions',
        'downloader': CW_Downloader,
        'config': 'ggdata/params/CW.json',
        'preprocessor': CW_Preprocessor,
    }
}


def download_from_metaconfig(meta_config, path="data/", SAVE_RAW=False):
    Downloader = meta_config['downloader'](API_URL=meta_config['URL'])
    API_name = meta_config['API']
    print(f"{API_name}", end=': ')

    with open(meta_config['config'], 'r') as file:
        API_params = json.load(file)
        n_requests = len(API_params)

    print(n_requests, 'requests specified')

    for k, dictionnary in enumerate(API_params):
        params = dictionnary['params']

        print(f"Request {k+1}/{n_requests}: {dictionnary}",)
        print('Downloading', end=': ')

        try:
            if SAVE_RAW:
                data = Downloader.download_data(path=f"{path}/{dictionnary['GGI_code']}.json", params=params)
            else:
                data = Downloader.get_data(params)
            print(Fore.GREEN + 'DONE')
        except Exception as e:
            print(Fore.RED + 'Error occured ', e)

        print('PreProcessing', end=': ')
        variable = dictionnary['GGI_code']
        Preprocessor = meta_config['preprocessor'](variable)
        information = {'Variable': variable, 'From': meta_config['API']}

        try:
            df = Preprocessor.preprocess(data, information)
            print(Fore.GREEN + 'DONE')
        except Exception as e:
            print(Fore.RED + 'Error occured ', e)

        print(f'Saving at {path}/{variable}_{API_name}.csv', end=': ')

        try:
            df.to_csv(f'{path}/{variable}_{API_name}.csv', index=False)
            print(Fore.GREEN + 'DONE')
        except Exception as e:
            print(Fore.RED + 'Error occured ', e)


if __name__ == '__main__':
    init(autoreset=True)

    parser = argparse.ArgumentParser(description='Download and preprocess data.')
    parser.add_argument('API', metavar='API', type=str, help='A supported API name.')
    parser.add_argument('--p', metavar='path', type=str, default="data/", help='Where the downloaded file goes.')
    parser.add_argument('--r', metavar='raw', type=bool, default=False, help='Save raw ouput')

    args = parser.parse_args()
    if args.API == 'ALL':
        print(f"Downloading and Processing APIs: {' '.join(meta_configs.keys())}")
        for meta_config_name in meta_configs:
            download_from_metaconfig(meta_configs[meta_config_name], args.p, args.r)
    else:
        download_from_metaconfig(meta_configs[args.API], args.p, args.r)
