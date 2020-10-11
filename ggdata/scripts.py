from ggdata.downloaders.downloader import WB_Downloader, SDG_Downloader, CW_Downloader
from ggdata.preprocessors.WB import WB_Preprocessor
from ggdata.preprocessors.SDG import SDG_Preprocessor
from ggdata.preprocessors.CW import CW_Preprocessor
from ggdata.ressources import load_API_parameters
from colorama import Fore, init
import json

init(autoreset=True)


API_CONFIGS = {
    'WB': {
        'API': 'WB API',
        'configs': load_API_parameters('WB'),
        'downloader': WB_Downloader('https://api.worldbank.org/v2/country/all/indicator/'),
        'preprocessor': WB_Preprocessor,
    },
    'SDG': {
        'API': 'SDG API',
        'downloader': SDG_Downloader('https://unstats.un.org/SDGAPI/v1/sdg/Series/Data'),
        'configs': load_API_parameters('SDG'),
        'preprocessor': SDG_Preprocessor,
    },
    'CW': {
        'API': 'CW API',
        'downloader': CW_Downloader('https://www.climatewatchdata.org/api/v1/data/historical_emissions'),
        'configs': load_API_parameters('CW'),
        'preprocessor': CW_Preprocessor,
    }
}


def download(API_name, config, path=None, raw=True, API_CONFIGS=API_CONFIGS):
    '''
    Wrapper function for downloading and preprocessing data from API.
    This is used in the command line tool. For specific uses, use the individual downloaders and preprocessors.

    Parameters
    ----------
    API_name: str
        The name of the API
    config: dict
        A dictionnary with keys 'GGI_code' and 'params'.
    path: str
        Path for saving
    raw: Bool
        whether to download the raw data or the preprocessed one.
    API_CONFIGS:
        The configs of the APIs
    '''
    assert API_name in ['CW', 'SDG', 'WB'], f"{API_name} is not in {['CW', 'SDG', 'WB']}"

    # SET UP PARAMATERS
    params = config['params']
    GGI_code = config['GGI_code']
    information = {'Variable': GGI_code, 'From': API_CONFIGS[API_name]['API']}

    Downloader = API_CONFIGS[API_name]['downloader']
    Preprocessor = API_CONFIGS[API_name]['preprocessor'](GGI_code)

    # DOWNLOADING
    print(f'Downloading {config} from {API_name}', end=': ')
    try:
        data = Downloader.get_data(params)
        print(Fore.GREEN + 'DONE')
    except Exception as e:
        print(Fore.RED + 'Error occured ', e)

    # Saving Raw
    if raw:
        if path:
            file_path = f"{path}/{GGI_code}_{API_name}.json"
            print(f'Saving at {file_path}', end=': ')
            try:
                with open(file_path, 'w') as file:
                    json.dump(data, file)
                print(Fore.GREEN + 'DONE')
            except Exception as e:
                print(Fore.RED + 'Error occured ', e)
        return data

    # PREPROCESSING
    else:
        print('PreProcessing', end=': ')
        try:
            df = Preprocessor.preprocess(data, information)
            print(Fore.GREEN + 'DONE')
        except Exception as e:
            print(Fore.RED + 'Error occured ', e)

        if path:
            file_path = f'{path}/{GGI_code}_{API_name}.csv'
            print(f'Saving at {file_path}', end=': ')
            try:
                df.to_csv(file_path, index=False)
                print(Fore.GREEN + f'DONE')
            except Exception as e:
                print(Fore.RED + 'Error occured ', e)

    return data


def download_all(API_name, path=None, raw=True, API_CONFIGS=API_CONFIGS):
    '''
    Wrapping for loop for downloading the full specified data on an API
    '''
    for config in API_CONFIGS[API_name]['configs']:
        download(API_name=API_name, config=config, path=path, raw=raw)
