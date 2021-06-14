from ggdata.preprocessors.preprocessor import Preprocessor
import pandas as pd


def parse_key(key):
    split = key.split(':')
    return {f'key_{i}': int(k) for i,k in enumerate(split)}


def parse_series(series):
    
    dfs = []
    
    for serie_key, serie in series.items():
        key_idx = parse_key(serie_key)
        
        df = pd.DataFrame.from_dict(serie['observations'], orient='index').rename(columns = {0: 'Value'})
        df.index = df.index.astype(int)
        
        for key, idx in key_idx.items():
            df[key] = idx
        
        dfs.append(df)  
    
    return pd.concat(dfs)


def merge_dims_series(series_df, structure_dims):
    '''To improve, special case for TIME_PERIOD seems risky'''
    df = series_df.merge(structure_dims['TIME_PERIOD'], left_index=True, right_index=True)
    
    for dim, dim_df in structure_dims.items():
        if dim != 'TIME_PERIOD':
            df = df.merge(dim_df, on=dim)
    return df  



def parse_structure_dims(structure_dims):
    '''To improve, check what exactly observation look like across datasets'''
    dfs = {}
    
    for dim in structure_dims['series']:
        
        key = f"key_{dim['keyPosition']}"
        df = pd.DataFrame(dim['values']).rename(columns={'id': dim['id'], 'name': dim['name']}).reset_index().rename(columns={'index':key})
        
        dfs[key] = df
    
    for obs in structure_dims['observation']:
        
        dfs[obs['role']] = pd.DataFrame(obs['values']).rename(columns={'id': obs['id'], 'name': obs['name']})

    return dfs


class OECD_Preprocessor(Preprocessor):
    '''
    Processor class used to preprocess data coming from OECD API
    '''
    def json_to_pandas(self, json):
    
        structure_dims = json['structure']['dimensions']
        series = json['dataSets'][0]['series']

        dims = parse_structure_dims(structure_dims)
        series = parse_series(series)

        df = merge_dims_series(series, dims)

        return df

    def format_pandas(self, df):
        return df

    def convert_dtypes(self, df):
        return df

    def handle_exceptions(self, df):
        return df
