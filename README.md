![alt text](http://greengrowthindex.gggi.org/wp-content/uploads/2019/09/LOGO_GGGI_GREEN_350x131px_002trans_Prancheta-1.png)

# Green Growth Downloader
------------------------------------
**This module downloads and standardize data from various public APIs**

# Supported APIs

| API           | URL                                                               | Downloading | Preprocessing |
|---------------|-------------------------------------------------------------------|-------------|---------------|
| World bank    | https://api.worldbank.org/v2/country/all/indicator/               | OK          | OK            |
| UNSTAT SDG    | https://unstats.un.org/SDGAPI/v1/sdg/Series/Data                  | OK          | OK            |
| Climate Watch | https://www.climatewatchdata.org/api/v1/data/historical_emissions | BUG         | BUG           |
| OECD          | http://stats.oecd.org/SDMX-JSON/data/                             | TO DO       | TO DO         |

# Installation
-------------------

```
$pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple  ggdata==0.1.32
```

Later to be added on proper pip.

# How to
-------------

See **Tutorial.ipynb** for details.

## Get data for a given indicator at a given API

```python
from ggdata.scripts import download

API_name = 'WB'

config = {
    'GGI_code': 'EE2',
    'params': {'indicator': 'EG.FEC.RNEW.ZS'}
}

data = download(API_name, config, raw=False)
```

# Quick Start for Green Growth Index
**(Not up to date, to be removed)**

A small command line tool is available to bulk download data. The tool lets you define an API name and a path.
For example:

```
$ggdownload WB --path data/ --raw true --restart false
```

- To download from WB data set WB
- To save in data/ folder set --path data/
- To download raw data set --raw true
- To download only missing data set --restart false

The information used to make the downloads are located in the ggdata/params folder.

Here is an example ggdata/params/SDG.json:
```
[
   {
      "GGI_code":"SE3",
      "params":{
         "seriesCode":"SL_TLF_NEET",
         "dimensions":"[{name:'Sex',values:['BOTHSEX']},{name:'Age',values:['15-24']}]"
      }
   },
   {
      "GGI_code":"EE1",
      "params":{
         "seriesCode":"EG_EGY_PRIM"
      }
   },

   ... AND SO ON ...

]
```



# Future improvements
-------------
Standardize parameters across APIs to be able to simplify getting data. (eg, the indicator name is seriesCode in SDG but indicator in WB and so on...)

Add functions to search indicators across APIs


# Author
---------------

S. Zabrocki for GGGI
