
# valis-python-client

### Dependencies
* Python 3
* Requests library

### Install

```
git clone git@github.com:VALIS-software/valis-python-client.git
cd valis-python-client
sudo python3 setup.py install
```

### Example Usage
NOTE: for more examples please see the /examples folder. Very basic docs are included in /docs/valis.html
```
from valis import valis, Dataset

# list gwas DB's
gwasDbs = valis.variants.gwasDatasets()

# fetch trait DB's
traitDbs = valis.traits.datasets()

# fetch traits in GWAS Catalog matching query 'carcinoma'
carcinomaTraits = valis.traits.search('carcinoma', datasets=[Dataset.GWAS_CATALOG])

# get list of variant tags in ExAC:
variantTags = valis.variants.tags(datasets=[Dataset.EXAC])

# generate variant query for missense or loss of function variants
missenseVariants = valis.variants.query(datasets=[Dataset.EXAC], variantTags=['missense_variant', 'loss_of_function'])

# search gwas data for missense variants mapping to carcinomas
gwasVariants = valis.variants.gwas(maxPValue=0.01, variantQuery=missenseVariants, traitQuery=carcinomaTraits, gwasDatasets=[Dataset.GWAS_CATALOG])

print('query %s' % gwasVariants.json())
print(gwasVariants.fetch())

```
