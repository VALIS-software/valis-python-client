from valis import valis, Dataset

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
variants = valis.variants.query(userfile=cnrFiles[0]['fileID'])


pathwayGenes = valis.pathways.genes('GABAergic synapse')

variantsInIntersection = variants.intersect(pathwayGenes)

print(variantsInIntersection.fetch())



