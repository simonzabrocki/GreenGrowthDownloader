from ggdata.preprocessors.preprocessor import Preprocessor
import pandas as pd


class WB_Preprocessor(Preprocessor):

    def json_to_pandas(self, data_json):
        df = pd.json_normalize(data_json[1])
        df['Source'] = data_json[0]['Source']

        return df

    def format_pandas(self, df):
        df = df.rename(columns={'countryiso3code': 'ISO',
                                'date': 'Year',
                                'value': 'Value',
                                'indicator.value': 'Description',
                                'country.value': 'Country'})

        df = df.drop(columns=['obs_status', 'unit', 'decimal', 'indicator.id', 'country.id'])
        return df

    def convert_dtypes(self, df):
        return df

    def handle_exceptions(self, df):
        return df
