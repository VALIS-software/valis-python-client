from .Dataset import Dataset
from .GenomeType import GenomeType

class Pathway:
  def __init__(self, api):
    self.api = api      

  def datasets(self):
    return [Dataset.KEGG]

  def names(self, datasets=[Dataset.KEGG]):
    """ Returns the list of all pathways available, optionally filtering by dataset"""
    return [p['name'] for p in self.api.infoQuery().filterType('pathway').filterSource(datasets).fetch()]

  def genes(self, pathway):
    """ Returns the list of genes in the specified pathway """
    return (self.api.genomeQuery()
      .filterType(GenomeType.GENE)
      .filterPathway(pathway))
