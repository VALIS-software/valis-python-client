from valis import valis, Dataset
from auth import VALIS_AUTH_USER, VALIS_AUTH_KEY

valis.login(VALIS_AUTH_USER, VALIS_AUTH_KEY)


# the available pathway datasets
availablePathwayDatasets = valis.pathways.datasets()

# the pathway names in kegg
pathwayNames = valis.pathways.names(availablePathwayDatasets[0])

# query representing genes in a pathway
genesInPathway = valis.pathways.genes(pathwayNames[0])

# fetch the list of genes in the pathway
genesInPathway.fetch()

# fetch biosamples in GTEx
biosamples = valis.biosamples.names(datasets=[Dataset.GTEX])

# fetch exac variants that regulate genes in this pathway
eqtlsForGenesInPathway = valis.variants.eqtl(genes=genesInPathway, biosamples=biosamples[0], variantDatasets=[Dataset.EXAC])


# define some intervals
customInterval = valis.region.createFromIntervals([('chr12', 111291402, 121291402), ('chr6', 30814428, 31814428)])
bedInterval = valis.region.createFromBed(open('examples/example.bed', 'rb'))
wholeInterval = customInterval.union(bedInterval)

# intersect these against the eQTLs
result = eqtlsForGenesInPathway.intersect(wholeInterval, windowSize=10000)
print(result.fetch())
