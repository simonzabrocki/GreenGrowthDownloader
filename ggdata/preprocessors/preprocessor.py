import abc


class Preprocessor(metaclass=abc.ABCMeta):
    '''
    Abstract processor class used to preprocess data coming from API

    Attributes
    ----------
    variable: str
        Name of the variable to be preprocessed (Used to handle special cases)
    '''

    def __init__(self, variable):
        self.variable = variable
        return None

    def parse_json(self, json):
        '''
        Parse the json file

        Parameters
        ---------
        json: list of dictionnary
            The loaded json file
        '''
        metadata_json = json['metadata']
        data_json = json['data']

        return metadata_json, data_json

    @abc.abstractmethod
    def json_to_pandas(self, data_json):
        '''
        Convert the json to pandas

        Parameters
        ---------
        data_json: list of dictionnary
            The data from the json file
        '''
        pass

    @abc.abstractmethod
    def format_pandas(self, df):
        '''
        Format the raw pandas

        Parameters
        ---------
        df: pd.DataFrame
            Raw DataFrame
        '''
        pass

    @abc.abstractmethod
    def convert_dtypes(self, df):
        pass

    @abc.abstractmethod
    def handle_exceptions(self, df):
        pass

    def add_information_pandas(self, df, information, metadata_json):
        '''
        Add information to the pandas

        Parameters
        ---------
        df: pd.DataFrame
            Formated DataFrame
        information: dict
            A dictionnary with the information to add (eg. download data, variable name etc ...)

        Returns
        -------
        df: pd.DataFrame
        '''
        df = df.copy()
        for key in information:
            df[key] = information[key]
        for key in metadata_json:
            df[key] = metadata_json[key]
        return df

    def preprocess(self, data_json, information):
        '''
        Preprocess a given json file and complete with the relevant information

        Parameters
        ---------
        ddata_json: json
            Raw loaded json file
        information: dict
            A dictionnary with the information to add (eg. download data, variable name etc ...)

        Returns
        -------
        df: pd.DataFrame
        '''
        metadata_json, df = self.parse_json(data_json)
        for step in [self.json_to_pandas, self.handle_exceptions, self.format_pandas, self.convert_dtypes]:
            df = step(df)

        final_df = self.add_information_pandas(df, information, metadata_json)

        return final_df.dropna()
