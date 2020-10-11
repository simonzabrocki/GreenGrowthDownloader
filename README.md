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

```
$git clone https://github.com/simonzabrocki/GreenGrowthDownloader.git
```

Later to be added on pip !

# Quick Start

A small command line tool has been made to make 'bulk downloads'. The tool lets you define and API name, a path.
For example:
- To download from WB data set WB
- To save in data/ folder set --path data/
- To download raw data set --raw true
- To download only missing data set --restart false
```
$python main.py WB --path data/ --raw true --restart false
```
The information used to make the download are located in the ggdata/params folder.

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

   ... TO CONTINUE ...

]
```
You can add information about new variable you need in the files.

To make specific downloads, refer to the following section

# How to
-------------

See **Tutorial.ipynb** for more details.

## Get data for a given indicator at a given API

```python
from ggdata.scripts import download

API_name = 'WB'

config = {
    'GGI_code': 'EE2',
    'params': {'indicator': 'EG.FEC.RNEW.ZS'}
}

data = download(API_name, config,raw=False)
```

# Authors
---------------

S. Zabrocki for GGGI
