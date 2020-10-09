![alt text](http://greengrowthindex.gggi.org/wp-content/uploads/2019/09/LOGO_GGGI_GREEN_350x131px_002trans_Prancheta-1.png)

# Green Growth Downloader
------------------------------------
>Green Growth Index measures country performance in achieving sustainability targets including Sustainable Development Goals, Paris Climate Agreement, and Aichi Biodiversity Targets for four green growth dimensions – efficient and sustainable resource use, natural capital protection, green economic opportunities and social inclusion.


**This module downloads and format data used in the Green Growth Index**

# Supported APIs

| API           | URL                                                               | Downloading | Preprocessing | Processing |
|---------------|-------------------------------------------------------------------|-------------|---------------|------------|
| World bank    | https://api.worldbank.org/v2/country/all/indicator/               | OK          | OK            | TODO       |
| UNSTAT SDG    | https://unstats.un.org/SDGAPI/v1/sdg/Series/Data                  | OK          | OK            | TODO       |
| Climate Watch | https://www.climatewatchdata.org/api/v1/data/historical_emissions | OK          | OK            | TODO       |


# Installation
-------------------
TODO

# How to
-------------

See **tutorial notebooks** for more details.

## Get raw data for a given config

```python
from IndexComputation.GreenGrowthIndex import *

ST = pd.read_csv('sample_data/ST.csv',
                 sep=';',
                 header=0,
                 index_col=0)

indicators = pd.read_csv('sample_data/Indicators.csv', index_col=0)


GGI = GreenGrowthIndex()

Index = GGI.compute(indicators=indicators, sustainability_targets=ST)
```

# Authors
---------------

H. Peyrière, S. Zabrocki for the Global Green Growth Institute.
(To expand)
