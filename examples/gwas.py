from valis import valis, Dataset

# list gwas DB's
print(valis.variants.gwasDatasets())

# list trait DB's
print(traitDbs = valis.traits.datasets())

# list variant DB's
print(valis.traits.datasets())

# generate query for traits in GWAS Catalog containing text 'carcinoma'
carcinomaTraits = valis.traits.search('carcinoma', [Dataset.GWAS_CATALOG])

# print list of variant tags in ExAC:
print(valis.variants.tags(datasets=[Dataset.EXAC]))

# generate variant query for missense or loss of function variants
missenseVariants = valis.variants.query(datasets=[Dataset.EXAC], variantTags=['missense_variant', 'loss_of_function'])

# search gwas data for missense variants mapping to carcinomas
gwasVariants = valis.variants.gwas(maxPValue=0.01, variantQuery=missenseVariants, traitQuery=carcinomaTraits, datasets=[Dataset.GWAS_CATALOG])

print('query %s' % gwasVariants.json())
print(gwasVariants.fetch())