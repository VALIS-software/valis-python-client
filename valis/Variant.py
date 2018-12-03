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

  def eqtl(self, maxPValue=0.01, biosamples=None, genes=None, eqtlDatasets=[Dataset.GTEX], variantTags=None, variantDatasets=[Dataset.DBSNP, Dataset.EXAC, Dataset.CLINVAR]):
    """ Returns the eQTLs contained within datasets, filtered by optional biosamples and optionally affecting genes within geneQuery"""

    # fetch all eQTL's that are known to modulate genes in this set
    eQTLs = (self.api.edgeQuery()
      .filterSource(eqtlDatasets)
      .filterBiosample(biosamples)
      .filterMaxPValue(maxPValue))

    variants = self.query(datasets=variantDatasets, variantTags=variantTags)
    return variants.addToEdge(eQTLs)

    
  def gwas(self, maxPValue=0.01, traitQuery=None, variantQuery=None, gwasDatasets=[Dataset.GWAS_CATALOG]):
    # GWAS relations are an edge between a variant and a trait
    if not variantQuery:
      variantQuery = self.query(datasets=[Dataset.DBSNP])
    gwasQuery = self.api.edgeQuery().filterSource(gwasDatasets).filterMaxPValue(maxPValue)
    return variantQuery.addToEdge(gwasQuery.toNode(traitQuery))

  def query(self, variantTags=None, datasets=[Dataset.EXAC, Dataset.CLINVAR, Dataset.DBSNP]):
    return(self.api.genomeQuery()
      .filterSource(datasets)
      .filterVariantTag(variantTags))
