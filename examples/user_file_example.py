from valis import valis, Dataset

valis.login()


# list all of the user files
myFiles = valis.getUploadedFiles()


"""
TLE_A = father wild type

TLE_B= Proband of the trios. Age of onset at 32 years old

TLE_C= Sister of TLE_B. Affected by the disease. Age of onset 28 years old.
"""


# filter out the CNR files
cnrFiles = []
for file in myFiles:
	if ('TLE' in file['fileName']):
		print('file: %s, (%d variants)' % (file['fileName'], file['numDocs']))
		cnrFiles.append(file)
print(cnrFiles)

# fetch the variants for the first file
# NOTE: you can only query one userfile at a time.
# You can combine them by using the union operator, or manually
# this a restriction that we're trying to fix.
variants = valis.variants.query(userfile=cnrFiles[0]['fileID'])

result = variants.fetch(full=True)

print(result)


# pathwayGenes = valis.pathways.genes('GABAergic synapse')

# variantsInIntersection = variants.intersect(pathwayGenes)

# print(variantsInIntersection.fetch())



