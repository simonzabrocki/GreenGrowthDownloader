![alt text](http://greengrowthindex.gggi.org/wp-content/uploads/2019/09/LOGO_GGGI_GREEN_350x131px_002trans_Prancheta-1.png)

# Green Growth Downloader
------------------------------------
**This module downloads and format data used in the Green Growth Index**

# Supported APIs

| API           | URL                                                               | Downloading | Preprocessing |
|---------------|-------------------------------------------------------------------|-------------|---------------|
| World bank    | https://api.worldbank.org/v2/country/all/indicator/               | OK          | OK            |
| UNSTAT SDG    | https://unstats.un.org/SDGAPI/v1/sdg/Series/Data                  | OK          | OK            |
| Climate Watch | https://www.climatewatchdata.org/api/v1/data/historical_emissions | OK          | OK            |

# Installation
-------------------
TODO

# How to
-------------

See **tutorial notebooks** for more details.

## Get raw data for a given config

```python
from src.downloaders.downloader import SDG_Downloader

Downloader = SDG_Downloader('https://unstats.un.org/SDGAPI/v1/sdg/Series/Data')

parameters = {'seriesCode': 'SL_TLF_NEET',
              'dimensions': "[{name:'Sex',values:['BOTHSEX']},{name:'Age',values:['15-24']}]"}

data = Downloader.get_data(parameters)
```

## Preprocess raw data

```python
from src.preprocessors.SDG_preprocessor import SDG_Preprocessor

Preprocessor = SDG_Preprocessor(file='test') # file argument to change (Used to preprocess special cases)

information = {'Variable': 'Test', 'From': 'SDG API'} # Let's you add more information to the dataframe

df = Preprocessor.preprocess(data, information)
```

# Authors
---------------

S. Zabrocki for the Global Green Growth Institute.
