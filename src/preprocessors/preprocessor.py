import abc
import os
import json
import pandas as pd


class Preprocessor(metaclass=abc.ABCMeta):

    def __init__(self, file):
        self.file = file
        return None

    def parse_json(self, json):
        metadata_json = json['metadata']
        data_json = json['data']

        return metadata_json, data_json

    @abc.abstractmethod
    def json_to_pandas(self, data_json):
        pass

    @abc.abstractmethod
    def format_pandas(self, df):
        pass

    @abc.abstractmethod
    def convert_dtypes(self, df):
        pass

    @abc.abstractmethod
    def handle_exceptions(self, df):
        pass

    def add_information_pandas(self, df, information, metadata_json):
        df = df.copy()
        for key in information:
            df[key] = information[key]
        for key in metadata_json:
            df[key] = metadata_json[key]
        return df

    def preprocess(self, json, information):
        metadata_json, df = self.parse_json(json)
        for step in [self.json_to_pandas, self.handle_exceptions, self.format_pandas, self.convert_dtypes]:
            df = step(df)

        final_df = self.add_information_pandas(df, information, metadata_json)

        return final_df.dropna()


def preprocess(folder, API_name, preprocessor):

    dfs = []
    for file in os.listdir(folder):
        path = f'{folder}/{file}'
        print(path, end=': ')

        variable = '.'.join(file.split('.')[:-1])
        information = {'Variable': variable, 'From': API_name}

        with open(path) as f:
            data = json.load(f)
            df = preprocessor(file).preprocess(data, information)
            dfs.append(df)
        f.close()
        print(df_preprocess_status(df))

    return pd.concat(dfs, axis=0)


def df_preprocess_status(df):
    shape = df.shape
    column_name = ' '.join(df.columns)
    duplicates_number = df.duplicated().sum()
    missingval_number = df.shape[0] - df.dropna().shape[0]

    return (('shape', shape), ('columns', column_name), ('duplicates', duplicates_number), ("missing values", missingval_number))
