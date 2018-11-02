from .Dataset import *

class Trait:
  def __init__(self, api):
    self.api = api

  def datasets(self):
    """ Returns the list of all trait datasets available"""
    return [Dataset.GWAS_CATALOG, Dataset.CLINVAR, Dataset.EFO]

  def query(self, datasets=[Dataset.GWAS_CATALOG]):
    return self.api.infoQuery().filterType('trait').filterSource(datasets)

  def withName(self, names=[], datasets=[Dataset.GWAS_CATALOG]):
    return self.query(datasets).filterName(names)

  def search(self, searchText, datasets=[Dataset.GWAS_CATALOG]):
    return self.query(datasets).searchText(searchText)
