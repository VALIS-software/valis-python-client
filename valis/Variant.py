from .Dataset import Dataset

class Variant:
  def __init__(self, api):
    self.api = api

  def datasets(self):
    """ Returns the list of all variant datasets available"""
    return [Dataset.GWAS_CATALOG, Dataset.CLINVAR, Dataset.DBSNP, Dataset.TCGA, Dataset.GTEX]

  def tags(self, datasets=[Dataset.EXAC]):
    """ Returns the variant tags available, optionally filtered by datasets"""
    return self.api.infoQuery().filterSource(datasets).distinctValues('info.variant_tags')

  def gwasDatasets(self):
    """ Returns the GWAS datasets that are available"""
    return [Dataset.GWAS_CATALOG, Dataset.CLINVAR]

  def eqtlDatasets(self):
    """ Returns the eQTL datasets that are available"""
    return [Dataset.GTEX]

  def eqtl(self, maxPValue=0.01, biosamples=None, eqtlDatasets=[Dataset.GTEX], variantTags=None, variantDatasets=[Dataset.DBSNP, Dataset.EXAC, Dataset.CLINVAR]):
    """ Returns the eQTLs contained within datasets, filtered by optional biosamples """
    eQTLs = (self.api.edgeQuery()
      .filterSource(eqtlDatasets)
      .filterBiosample(biosamples)
      .filterMaxPValue(maxPValue))

    variants = self.query(datasets=variantDatasets, variantTags=variantTags)
    return variants.addToEdge(eQTLs)

    
  def gwas(self, maxPValue=0.01, traitQuery=None, variantQuery=None, datasets=[Dataset.GWAS_CATALOG]):
    # GWAS relations are an edge between a variant and a trait
    if not variantQuery:
      variantQuery = self.query(datasets=[Dataset.DBSNP])
    if not traitQuery:
      # search for any trait
      traitQuery = self.query(datasets=[Dataset.EFO])
    gwasQuery = self.api.edgeQuery().filterSource(datasets).filterMaxPValue(maxPValue)
    return variantQuery.addToEdge(gwasQuery.toNode(traitQuery))

  def query(self, variantTags=None, datasets=[Dataset.EXAC, Dataset.CLINVAR, Dataset.DBSNP], userfile=None):
    if userfile:
      if type(userfile) == list:
        print('cannot query multiple user files, use union')
      return(self.api.genomeQuery()
        .setUserFileID(userfile)
        .filterVariantTag(variantTags))
    else:
      return(self.api.genomeQuery()
        .filterSource(datasets)
        .filterVariantTag(variantTags))
