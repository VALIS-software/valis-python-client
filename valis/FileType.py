from enum import EnumMeta

class FileType(EnumMeta):
  """
  FileType specifies the string values for the different userfile types that can
  be uploaded.
  """
  TXT_23ANDME = '23andme'
  VCF = 'vcf'
  BED = 'bed'
