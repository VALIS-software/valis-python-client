from valis import ValisAPI, Dataset, Genome

client = ValisAPI()

# all TCGA patients
patientQuery = (client
	.infoQuery()
	.filterType('patient')
	.filterSource(Dataset.TCGA)
	.filterPatientGender('MALE')
	.filterPatientDisease('LUSC'))

print(client.getQueryResults(patientQuery, full=True))