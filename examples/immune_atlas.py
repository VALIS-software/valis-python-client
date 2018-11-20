from valis import valis, Dataset



# generate query for traits in GWAS Catalog containing text 
raTraits = valis.traits.search('rheumatoid arthritis', [Dataset.GWAS_CATALOG])
ucTraits = valis.traits.search('ulcerative colitis', [Dataset.GWAS_CATALOG])

# variants
dbsnp = valis.variants.query(datasets=[Dataset.DBSNP])

# gwas
raSNPs = valis.variants.gwas(maxPValue=0.01, variantQuery=dbsnp, traitQuery=raTraits, gwasDatasets=[Dataset.GWAS_CATALOG])
ucSNPs = valis.variants.gwas(maxPValue=0.01, variantQuery=dbsnp, traitQuery=ucTraits, gwasDatasets=[Dataset.GWAS_CATALOG])


both = raSNPs.intersect(ucSNPs)

immune = valis.annotations.query(datasets=Dataset.IMMUNEATLAS, biosamples='1002-Th1_precursors-U')

# to fetch all metadata set full=True

# fetch all the immune cell annotations that intersect a GWAS SNP:
print(immune.intersect(both).fetch(full=True))

# fetch all the GWAS SNP that intersect an immune cell annotation
print(both.intersect(immune).fetch(full=True))