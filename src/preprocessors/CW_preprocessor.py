from src.preprocessors.preprocessor import Preprocessor
import pandas as pd


class CW_Preprocessor(Preprocessor):

    def dict_to_df(self, dictionnary):
        df = pd.DataFrame(dictionnary['emissions'])

        for key in dictionnary.keys():
            if key != 'emissions':
                df[key] = dictionnary[key]

        return df

    def json_to_pandas(self, data_json):
        return pd.concat([self.dict_to_df(d) for d in data_json], axis=0)

    def handle_exceptions(self, df):
        return df

    def format_pandas(self, df):
        df = df.rename(columns={'year': 'Year', 'value': 'Value', 'iso_code3': 'ISO', 'data_source': 'Source', 'country': 'Country'})
        return df.drop(columns=['id'], errors='ignore')

    def convert_dtypes(self, df):
        return df


def process_GE1_0(df):
    df = df.copy()
    df['Description'] = df['gas'] + ' ' + df['sector'] + ' ' + df['unit']
    return df


def process_GE2_0(df):
    res = pd.DataFrame()
    res = df.groupby(['iso_code3', 'year', 'sector', 'country', 'data_source'])['value'].sum().reset_index()
    Agri = res[res.sector == 'Agriculture'].set_index(['iso_code3', 'year', 'country', 'data_source']).drop(columns='sector')
    LUCF = res[res.sector == 'Total excluding LUCF'].set_index(['iso_code3', 'year', 'country', 'data_source']).drop(columns='sector')
    res = (LUCF - Agri).reset_index()
    description = ' '.join(df.gas.unique()) + ' ' + ' and excluding'.join(df.sector.unique()) + ' ' + ' '.join(df.unit.unique())
    res['Description'] = description
    return res


def process_GE3_0(df):
    res = pd.DataFrame()
    res = df.groupby(['iso_code3', 'year', 'sector', 'country', 'data_source'])['value'].sum().reset_index()
    Agri = res[res.sector == 'Agriculture'].set_index(['iso_code3', 'year', 'country', 'data_source']).drop(columns='sector')
    LUCF = res[res.sector == 'Land-Use Change and Forestry'].set_index(['iso_code3', 'year', 'country', 'data_source']).drop(columns='sector')
    res = (LUCF + Agri).reset_index()
    description = ' '.join(df.gas.unique()) + ' ' + ' and '.join(df.sector.unique()) + ' ' + ' '.join(df.unit.unique())
    res['Description'] = description
    return res
