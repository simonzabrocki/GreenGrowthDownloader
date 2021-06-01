import pkg_resources
import json
import pandas as pd


def load_API_parameters(API_name):
    """
    A function to load existing configs used in the green growth data

    Parameters
    ----------
    API_name: str
        API name to choose from CW (climate watch), WB (World Bank), SDG (UNSTAT)
    """
    stream = pkg_resources.resource_stream(__name__, f'params/{API_name}.json')
    with open(stream.name, 'r') as f:  # to improve stream already have the info i think, no need to load again !
        data = json.load(f)
    return data
    

def load_country_info(path='params/countries_info.csv'):
    """
    A function to load country infos in dataframe
    Parameters
    ----------
    path: str
        Path to the country info file
    """
    stream = pkg_resources.resource_stream(__name__, path)
    
    df = pd.read_csv(stream.name, index_col=0)
    
    return df

