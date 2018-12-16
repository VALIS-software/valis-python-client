from valis import valis, Dataset

valis.login()

print(valis.variants.datasets())
print(valis.variants.eqtlDatasets())
print(valis.variants.gwasDatasets())
print(valis.pathways.datasets())
print(valis.genes.datasets())
print(valis.traits.datasets())
print(valis.patients.datasets())
print(valis.annotations.datasets())


# show immune atlas cell types
biosamples = valis.biosamples.names(datasets=[Dataset.IMMUNEATLAS])
print(biosamples)

# show encode cell types
encodeBiosamples = valis.biosamples.names(datasets=[Dataset.ENCODE])
print(encodeBiosamples)

# show encode annotation types for first  biosample
annTypes = valis.biosamples.annotationTypes(datasets=[Dataset.ENCODE], biosamples=encodeBiosamples[0])
print(annTypes)

# show targets
targetTypes = valis.biosamples.targets(datasets=[Dataset.ENCODE], biosamples=encodeBiosamples[0])
print(targetTypes)

# fetch the encode annotations
encQuery = valis.annotations.query(datasets=[Dataset.ENCODE], annotationTypes=annTypes[0], biosamples=encodeBiosamples[0])
encQuery = encQuery.filterRegion('chrX', 0, 10000000)
annotations=encQuery.fetch()
print('fetched %d annotations' % len(annotations))

### NOTE!!! fetch() imposes a 1 million result limit on the query by default.
### If you wish to fetch > 1 mil results use the getQueryResults to iterate directly as follows
### TODO: some issues here, let's investigate.
idx = 0
fetchSize = 1000000
bigQuery = valis.annotations.query(datasets=Dataset.ENCODE, biosamples=encodeBiosamples[0])
results, finished = valis.getQueryResults(bigQuery, startIdx=idx, endIdx=idx+fetchSize)

while not finished:
	more_results, finished = valis.getQueryResults(bigQuery, full=False, startIdx=idx, endIdx=idx+fetchSize)
	print ('got %d more results' % len(more_results))
	results += more_results
	idx += len(more_results)

print(len(results))