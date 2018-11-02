
class Biosample:
  def __init__(self, api):
    self.api = api
  def names(self, datasets):
    """ returns the biosamples in the dataset """
    q = self.api.infoQuery().filterSource(datasets)
    return self.api.distinctValues('info.biosample', q)

  def annotationTypes(self, datasets, biosamples=None):
    q = (self.api.infoQuery()
      .filterSource(datasets)
      .filterBiosample(biosamples))
    return self.api.distinctValues('info.types', q)
  
  def targets(self, datasets, biosamples=None, annotationType=None):
    q = (self.api.infoQuery()
      .filterSource(datasets)
      .filterAnnotationType(annotationType)
      .filterBiosample(biosamples))
    return self.api.distinctValues('info.targets', q)

