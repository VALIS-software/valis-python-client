from .Dataset import Dataset

class Gene:
  def __init__(self, api):
    self.api = api

  def datasets(self):
    """ Returns the list of annotation datasets available e.g ENCODE, ENSEMBL, ROADMAP """
    return [Dataset.ENSEMBL]
  
  def query(self, names=None):
    return (self.api.genomeQuery()
      .filterSource(Dataset.ENSEMBL)
      .filterType(GenomeType.GENE)
      .filterName(names))
