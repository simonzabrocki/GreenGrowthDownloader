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
