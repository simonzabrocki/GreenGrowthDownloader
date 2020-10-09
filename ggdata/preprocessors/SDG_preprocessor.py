from ggdata.preprocessors.preprocessor import Preprocessor
import pandas as pd
from ggdata.utils.ISOs import add_ISO


class SDG_Preprocessor(Preprocessor):

    def json_to_pandas(self, json):
        df = pd.json_normalize(json)
        columns = df.columns
        dimensions = [dim for dim in columns if 'dimensions' in dim]
        to_select = ['seriesDescription', 'geoAreaName',
                     'source', 'timePeriodStart', 'value'] + dimensions
        df = df[to_select]
        return df

    def format_pandas(self, df):
        df = df.copy()
        df = df.rename(columns={'geoAreaName': 'Country',
                                'timePeriodStart': 'Year',
                                'value': 'Value',
                                'seriesDescription': 'Description',
                                'source': 'Source'
                                }
                       )
        columns = df.columns
        dimensions = [dim for dim in columns if 'dimensions' in dim]

        for dim in dimensions:
            df['Description'] += ' ' + dim.split('.')[1] + ' ' + df[dim]

        df = add_ISO(df)
        return df.drop(columns=dimensions)

    def convert_dtypes(self, df):
        df = df.copy()

        df['Year'] = df['Year'].astype(int)
        df['Value'] = df['Value'].astype(float)

        return df

    def handle_exceptions(self, df):

        if self.variable == 'AB2.1.json':
            df = df.copy()
            df.loc[df['value'] == '>95', 'value'] = 95
            df.loc[df['value'] == '<5', 'value'] = 5
            return df
        else:
            return df
