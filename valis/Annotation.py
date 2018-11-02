from .Dataset import Dataset

class Annotation:
  def __init__(self, api):
    self.api = api

  def datasets(self):
    """ Returns the list of annotation datasets available e.g ENCODE, ENSEMBL, ROADMAP """
    return [Dataset.ENCODE, Dataset.ROADMAP]

  def query(self, datasets=[Dataset.ENCODE], biosamples=None, annotationTypes=None, targets=None):
    """ Returns a query for the  specified annotation types"""
    return (self.api.genomeQuery()
      .filterSource(datasets)
      .filterBiosample(biosamples)
      .filterTargets(targets)
      .filterAnnotationType(annotationTypes))
