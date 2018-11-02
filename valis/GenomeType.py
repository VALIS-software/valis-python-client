from enum import EnumMeta

class GenomeType(EnumMeta):
  """
  GenomeType encapsulates string values for the most common genomic annotation types
  (e.g transcript, gene, variant). GenomeType is an internal class and 
  valis.biosample.annotationTypes() is recommended over GenomeType.
  """
  VARIANT = 'variant'
  SNP = 'SNP'
  GENE = 'gene'