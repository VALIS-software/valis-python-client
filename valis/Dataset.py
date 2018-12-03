from enum import EnumMeta

class Dataset(EnumMeta):
  GWAS_CATALOG = 'GWAS Catalog';
  CLINVAR = 'ClinVar';
  DBSNP = 'dbSNP';
  ENCODE = 'ENCODE';
  ROADMAP = 'Roadmap Epigenomics';
  FASTA = 'RefSeq';
  EFO = 'EFO';
  ENCODE_BIGWIG = 'ENCODEbigwig';
  EXAC = 'ExAC';
  TCGA = 'TCGA';
  ENSEMBL = 'ENSEMBL';
  GTEX = 'GTEx';
  KEGG = 'KEGG';
  IMMUNEATLAS = 'ImmuneAtlas';


