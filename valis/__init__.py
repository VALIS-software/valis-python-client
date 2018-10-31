import json
import requests

from enum import EnumMeta

class Genome(EnumMeta):
  VARIANT = 'variant'
  SNP = 'snp'
  GENE = 'gene'
  # TODO : Finish listing all types

class FileType(EnumMeta):
  TXT_23ANDME = '23andme'
  VCF = 'vcf'
  BED = 'bed'

class QueryType(EnumMeta):
  GENOME = 'GenomeNode'
  INFO = 'InfoNode'
  EDGE = 'EdgeNode'

class Dataset(EnumMeta):
  GENOME = 'GRCh38_gff';
  GWAS_CATALOG = 'GWAS Catalog';
  CLINVAR = 'ClinVar';
  DBSNP = 'dbSNP';
  ENCODE_ANNOTATIONS = 'ENCODE';
  ROADMAP = 'Roadmap Epigenomics';
  FASTA = 'RefSeq';
  EFO = 'EFO';
  ENCODE_bigwig = 'ENCODEbigwig';
  ExAC = 'ExAC';
  TCGA = 'TCGA';
  ENSEMBL = 'ENSEMBL';
  GTEX = 'GTEx';


class QueryBuilder:
  def __init__(self):
    self.query = None

  def newGenomeQuery(self):
    self.query = {
      'type': QueryType.GENOME,
      'filters': {},
      'toEdges': [],
      'arithmetics': [],
    }
    return self

  def newInfoQuery(self):
    self.query = {
      'type': QueryType.INFO,
      'filters': {},
      'toEdges': [],
      'arithmetics': [],
    }
    return self

  def newEdgeQuery(self):
    self.query = {
      'type': QueryType.EDGE,
      'filters': {},
      'toEdges': [],
      'arithmetics': [],
    }
    return self

  def filterID(self, id):
    self.query['filters']['_id'] = id;
    return self

  def filterType(self, type):
    self.query['filters']['type'] = type;
    return self
  
  def filterSource(self, source):
    self.query['filters']['source'] = source;
    return self
  
  def filterContig(self, contig):
    if (self.query['type'] != QueryType.GENOME):
      raise 'filter contig only available for GenomeNodes';
    self.query['filters']['contig'] = contig;
    return self
  
  def filterLength(self, length):
    if (self.query.type != QueryType.GENOME):
      raise 'Length only available for GenomeNodes';
    
    self.query['filters']['length'] = length;
    return self
  
  def filterName(self, name):
    self.query['filters']['name'] = name;
    return self
  
  def filterPathway(self, pathways):
    self.query.filters['info.kegg_pathways'] = pathways;
    return self
  
  def filterMaxPValue(self, pvalue):
    self.query.filters['info.p-value'] = { '<': pvalue };
    return self
  
  def filterBiosample(self, biosample):
    if type(biosample) == list :
      self.query.filters['info.biosample'] = { '$in' : biosample };
    else:
      self.query.filters['info.biosample'] = biosample;
    return self
    
  def filterTargets(self, targets):
    if len(targets):
      self.query.filters['info.targets'] = { '$all': targets };
    return self
    
  def filterInfotypes(self, type):
    self.query.filters['info.types'] = type;
    return self
  
  def filterAssay(self, assay):
    self.query.filters['info.assay'] = assay;
    return self
  
  def filterOutType(self, outType):
    self.query.filters['info.outtype'] = outType;
    return self
  
  def filterPatientBarCode(self, outType):
    self.query.filters['info.patient_barcodes'] = outType;
    return self
  
  def filterStartBp(self, start):
    if self.query['type'] != QueryType.GENOME:
      raise 'filterStartBp is only available for an Genome Query.';
    
    self.query['filters']['start'] = start;
    return self
  
  def filterEndBp(self, end):
    if self.query['type'] != QueryType.GENOME:
      raise 'filterEndBp is only available for an Genome Query.';
    self.query['filters']['end'] = end;
    return self
  
  def filterAffectedGene(self, gene):
    previous = self.query['filters']['variant_affected_genes'] or [];
    self.query['filters']['info.variant_affected_genes'] = gene;
    return self
  
  def filterVariantTag(self, tag):
    if type(tag) == list:
      self.query['filters']['info.variant_tags'] = { '$in' : tag };
    else:
      self.query['filters']['info.variant_tags'] = tag;
    return self

  def searchText(self, text):
    self.query['filters']['$text'] = text;
    return self

  def setLimit(self, limit):
    self.query['limit'] = limit;
    return self

  def get(self):
    return self.query

  def json(self):
    return json.dumps(self.query)
 
  def __str__(self):
    return json.dumps(self.query)

  def isGwas(self):
    return False



class ValisAPI:
    def __init__(self, ip='http://35.185.230.75', username=None, password=None):
        self.apiUrl = ip
        pass

    def genomeQuery(self):
        return QueryBuilder().newGenomeQuery()

    def infoQuery(self):
        return QueryBuilder().newInfoQuery()

    def edgeQuery(self):
        return QueryBuilder().newEdgeQuery()

    def contigs(self):
        return json.loads(requests.get('%s/contig_info' % self.apiUrl).content)

    def getUploadedFiles(self):
        return json.loads(requests.get('%s/user_files' % self.apiUrl).content)

    def getDetails(dataID, userFileID=None):
        requestUrl = '%s/details/%s' % (self.apiUrl, dataID);
        if (userFileID):
            requestUrl = requestUrl + "?userFileID=" + userFileID;
        return json.loads(requests.get(requestUrl).content)

    def distinctValues(self, key, query):
        requestUrl = '%s/distinct_values/%s' % (self.apiUrl, key);
        return requests.post(requestUrl, json=query.get()).content

    def uploadFile(self, file_path):
        url = '%s/user_files' % self.apiUrl
        files = {'file': open(file_path, 'rb'), 'fileType' : file_type}
        return requests.post(url, files=files)


    def downloadQuery(self, query, output_path, sort=False):
        requestUrl = '%s/download_query' % self.apiUrl
        result = requests.post(requestUrl, json={ 'query': query.get(), 'sort': sort}).content
        with open(output_path, "wb") as f:
            f.write(result)

    def getQueryResults(self, query, full=False, startIdx=None, endIdx=None):
        requestUrl = '%s/query/basic' % self.apiUrl
        if (full):
            requestUrl = '%s/query/full' % self.apiUrl;

        if (query.isGwas()):
            requestUrl = '%s/query/gwas' % self.apiUrl;

        options = [];
        if (startIdx != None):
            options.append('result_start=%d' % startIdx);

        if (endIdx != None):
            options.append('result_end=%d' % endIdx);

        if (len(options)):
            requestUrl = requestUrl + '?' + '&'.join(options)

        result = json.loads(requests.post(requestUrl, json=query.get()).content)
        return result['data'], result['reached_end']



