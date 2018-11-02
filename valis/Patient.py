from .Dataset import Dataset

class Patient:
  def __init__(self, api):
    self.api = api

  def datasets(self):
    return [Dataset.TCGA]

  def genders(self, datasets=[Dataset.TCGA]):
    pass

  def indications(self, datasets=[Dataset.TCGA]):
    pass

  def vitalStatuses(self, datasets=[Dataset.TCGA]):
    pass

  def ages(self, datasets=[Dataset.TCGA]):
    pass

  def ageOfOnsets(self, datasets=[Dataset.TCGA]):
    pass

  def query(self, genders=None, vitalStatus=None, indications=None, patientBarcodes=None, datasets=[Dataset.TCGA]):
    return (self.api
      .infoQuery()
      .filterType('patient')
      .filterSource(datasets)
      .filterPatientGender(genders)
      .filterVitalStatus(vitalStatus)
      .filterPatientBarCode(patientBarcodes)
      .filterPatientDisease(indications))

  def variants(self, patientBarcodes=None, datasets=[Dataset.TCGA]):
    return (self.api.genomeQuery()
      .filterSource(datasets)
      .filterPatientBarCode(patientBarcodes)
    )

  def variantsForPatient(self, patient):
    return (self.variants(patientBarcodes=patient['info']['patient_barcode']))
