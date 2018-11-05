from valis import valis, Dataset

# list gwas DB's
gwasDbs = valis.variants.gwasDatasets()

# fetch trait DB's
traitDbs = valis.traits.datasets()

# fetch traits in GWAS Catalog matching query 'carcinoma'
carcinomaTraits = valis.traits.search('carcinoma')

# get list of variant tags in ExAC:
variantTags = valis.variants.tags(datasets=[Dataset.EXAC])

# generate variant query for missense or loss of function variants
missenseVariants = valis.variants.query(datasets=[Dataset.EXAC], variantTags=['missense_variant', 'loss_of_function'])

# search gwas data for missense variants mapping to carcinomas
gwasVariants = valis.variants.gwas(maxPValue=0.01, variantQuery=missenseVariants, traitQuery=carcinomaTraits, gwasDatasets=[Dataset.GWAS_CATALOG])

print('query %s' % gwasVariants.json())
print(gwasVariants.fetch())