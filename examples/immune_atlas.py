from valis import valis, Dataset

# write a query for traits
raTraits = valis.traits.search('rheumatoid arthritis', [Dataset.GWAS_CATALOG])
ucTraits = valis.traits.search('ulcerative colitis', [Dataset.GWAS_CATALOG])

# write a query for variants data
dbsnp = valis.variants.query(datasets=[Dataset.DBSNP])

# gwas takes in a variantQuery and a traitQuery
raSNPs = valis.variants.gwas(maxPValue=0.01, variantQuery=dbsnp, traitQuery=raTraits, gwasDatasets=[Dataset.GWAS_CATALOG])
ucSNPs = valis.variants.gwas(maxPValue=0.01, variantQuery=dbsnp, traitQuery=ucTraits, gwasDatasets=[Dataset.GWAS_CATALOG])

# intersect the two SNPs
both = raSNPs.intersect(ucSNPs)

# fetch the immune atlas annotations
immune = valis.annotations.query(datasets=Dataset.IMMUNEATLAS, biosamples='1002-Th1_precursors-U')

# to fetch all metadata set full=True

# fetch all the immune cell annotations that intersect a GWAS SNP:
print(immune.intersect(both).fetch(full=True))

# fetch all the GWAS SNP that intersect an immune cell annotation
print(both.intersect(immune).fetch(full=True))