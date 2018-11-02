import json
import requests

from enum import EnumMeta

class Genome(EnumMeta):
  VARIANT = 'variant'
  SNP = 'SNP'
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

class Pathway:
  def __init__(self, api):
    self.api = api      

  def names(self, datasets=[Dataset.KEGG]):
    """ Returns the list of all pathways available, optionally filtering by dataset"""
    return [p['name'] for name in self.api.infoQuery().filterType('pathway').filterSource(datasets).fetch()]

  def genes(self, pathway):
    """ Returns the list of genes in the specified pathway """
    return (self.api.genomeQuery()
      .filterType(Genome.GENE)
      .filterPathway(pathway))

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

    
  def gwas(self, maxPValue=0.01, traitQuery=None, variantTags=None, gwasDatasets=[Dataset.GWAS_CATALOG], variantDatasets=[Dataset.EXAC, Dataset.CLINVAR, Dataset.DBSNP]):
    variantQuery = self.query(variantTags, variantDatasets)
    # GWAS relations are an edge between a variant and a trait
    gwasQuery = self.api.edgeQuery().filterSource(gwasDatasets).filterMaxPValue(maxPValue)
    return variantQuery.addToEdge(gwasQuery.toNode(traitQuery))

  def query(self, variantTags=None, datasets=[Dataset.EXAC, Dataset.CLINVAR, Dataset.DBSNP]):
    return(self.api.genomeQuery()
      .filterSource(datasets)
      .filterVariantTag(variantTags))

class GenomicRegion:
  def __init__(self):
    pass

  def addInterval(self, contig, start, end):
    pass

  def removeInterval(self, contig, start, end):
    pass

  def getIntervals(self):
    pass

  def setIntervals(self, intervals):
    pass
  
  def createFromBED(self, path):
    pass
  
  def commit(self):
    pass
  
  def get(self):
    pass

class Gene:
  def __init__(self, api):
    self.api = api

  def datasets(self):
    """ Returns the list of annotation datasets available e.g ENCODE, ENSEMBL, ROADMAP """
    return [Dataset.ENSEMBL]
  
  def query(self, names=None):
    return (self.api.genomeQuery()
      .filterSource(Dataset.ENSEMBL)
      .filterType(Genome.GENE)
      .filterName(names))

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

class Biosample:
  def __init__(self, api):
    self.api = api
    self.annotations = Annotation(self.api)
  
  def names(self, datasets):
    """ returns the biosamples in the dataset """
    q = self.api.infoQuery().filterSource(datasets)
    return self.api.distinctValues('info.biosample', q)

  def types(self, datasets, biosamples=None):
    q = (self.api.infoQuery()
      .filterSource(datasets)
      .filterBiosample(biosamples))
    return self.api.distinctValues('info.types', q)
  
  def targets(self, datasets, biosamples=None, annotationType=None):
    q = (self.api.infoQuery()
      .filterSource(datasets)
      .filterAnnotationType(annotationType)
      .filterBiosample(biosamples))
    return self.api.distinctValues('info.targets', q)


class QueryBuilder:
  def __init__(self, api):
    self.query = None
    self.api = api
    self.isEdgeOnly = False

  def duplicate(self):
    copy = QueryBuilder(self.api)
    copy.query = json.loads(self.json())
    copy.isEdgeOnly = self.isEdgeOnly
    return copy

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

  def setFilterValue(self, filterKey, value):
    if value is None:
      return
    if (type(value) == list):
      self.query['filters'][filterKey] = { '$in' : value };
    else:
      self.query['filters'][filterKey] = value;

  def filterID(self, id):
    copy = self.duplicate()
    copy.query['filters']['_id'] = id;
    return copy

  def filterType(self, types):
    copy = self.duplicate()
    copy.setFilterValue('type', types)
    return copy
  
  def filterSource(self, source):
    copy = self.duplicate()
    copy.setFilterValue('source', source)
    return copy
  
  def filterContig(self, contig):
    if (self.query['type'] != QueryType.GENOME):
      raise 'filter contig only available for GenomeNodes';
    copy = self.duplicate()
    copy.query['filters']['contig'] = contig;
    return copy
  
  def filterLength(self, length):
    if (self.query.type != QueryType.GENOME):
      raise 'Length only available for GenomeNodes';
    
    copy = self.duplicate()
    copy.query['filters']['length'] = length;
    return copy
  
  def filterName(self, name):
    copy = self.duplicate()
    copy.setFilterValue('name', name);
    return copy
  
  def filterPathway(self, pathways):
    copy = self.duplicate()
    copy.setFilterValue('info.kegg_pathways', pathways);
    return copy
  
  def filterMaxPValue(self, pvalue):
    copy = self.duplicate()
    copy.setFilterValue('info.p-value', { '<': pvalue });
    return copy
  
  def filterBiosample(self, biosample):
    copy = self.duplicate()
    if biosample == None:
      return copy
    if (type(biosample) != list):
      biosample = [biosample]
    copy.setFilterValue('info.biosample', biosample)
    return copy
    
  def filterTargets(self, targets):
    copy = self.duplicate()
    if targets == None:
      return copy
    if len(targets):
      copy.query['filters']['info.targets'] = { '$all': targets };
    return copy
    
  def filterAnnotationType(self, annotationType):
    copy = self.duplicate()
    copy.setFilterValue('info.types', annotationType);
    return copy
  
  def filterAssay(self, assay):
    copy = self.duplicate()
    copy.query['filters']['info.assay'] = assay;
    return copy
  
  def filterOutType(self, outType):
    copy = self.duplicate()
    copy.query['filters']['info.outtype'] = outType;
    return copy
  
  def filterPatientBarCode(self, outType):
    copy = self.duplicate()
    copy.query['filters']['info.patient_barcodes'] = outType;
    return copy

  def filterPatientGender(self, gender):
    copy = self.duplicate()
    copy.query['filters']['info.gender'] = gender;
    return copy

  def filterPatientDisease(self, disease_code):
    copy = self.duplicate()
    copy.query['filters']['info.disease_code'] = disease_code;
    return copy
  
  def filterStartBp(self, start):
    if self.query['type'] != QueryType.GENOME:
      raise 'filterStartBp is only available for an Genome Query.';
    
    copy = self.duplicate()
    copy.query['filters']['start'] = start;
    return copy
  
  def filterEndBp(self, end):
    if self.query['type'] != QueryType.GENOME:
      raise 'filterEndBp is only available for an Genome Query.';
    copy = self.duplicate()
    copy.query['filters']['end'] = end;
    return copy
  
  def filterAffectedGene(self, gene):
    previous = self.query['filters']['variant_affected_genes'] or [];
    copy = self.duplicate()
    copy.query['filters']['info.variant_affected_genes'] = gene;
    return copy
  
  def filterVariantTag(self, tags):
    copy = self.duplicate()
    copy.setFilterValue('info.variant_tags',  tags)
    return copy

  def searchText(self, text):
    copy = self.duplicate()
    copy.query['filters']['$text'] = text;
    return copy

  def setLimit(self, limit):
    copy = self.duplicate()
    copy.query['limit'] = limit;
    return copy

  def get(self):
    return self.query

  def json(self):
    return json.dumps(self.query)
 
  def __str__(self):
    return json.dumps(self.query)

  def addToEdge(self, edgeQuery):
    if (self.query['type'] == QueryType.EDGE):
      raise 'Edge can not be connected to another edge.';
    copy = self.duplicate()
    copy.query['toEdges'].append(edgeQuery.get());
    if (not 'toNode' in edgeQuery.get()):
      copy.isEdgeOnly = True
    return copy

  def toNode(self, nodeQuery, reverse=False):
    if (self.query['type'] != QueryType.EDGE):
      raise 'toNode is only available for an Edge Query.';
    copy = self.duplicate()
    copy.query['toNode'] = nodeQuery.get();
    copy.query['reverse'] = reverse;
    return copy


  def intersect(self, genomeQuery, windowSize=None):
    if (self.query['type'] != QueryType.GENOME):
      raise 'Arithmetic is only available for an Genome Query.'
    ar = {
      'operator': 'intersect',
      'target_queries': [genomeQuery.get()],
    }
    if (windowSize != None):
      ar['windowSize'] = int(windowSize)
      ar['operator'] = 'window'
    copy = self.duplicate()
    copy.query['arithmetics'].append(ar);
    return copy

  def union(self, queries):
    if type(queries) != list:
      queries = [queries.get()]
    else:
      queries = [query.get() for query in queries]
    ar = {
      'operator': 'union',
      'target_queries': queries,
    }
    copy = self.duplicate()
    copy.query['arithmetics'].append(ar);
    return copy

  def diff(self, queries):
    if type(queries) != list:
      queries = [queries.get()]
    else:
      queries = [query.get() for query in queries]
    ar = {
      'operator': 'diff',
      'target_queries': queries,
    }
    copy = self.duplicate()
    copy.query['arithmetics'].append(ar);
    return copy

  def fetch(self, full=False, startIdx=None, endIdx=None):
    result, has_more = self.api.getQueryResults(self.setLimit(1000000), full, startIdx, endIdx)
    return result
  
  def distinctValues(self, key):
    return self.api.distinctValues(key, self)

  def saveAsBed(self, outputPath, sortResults=False):
    return self.api.downloadQuery(self.query, outputPath, sortResults)

class api:
    def __init__(self, ip='http://35.185.230.75', username=None, password=None):
        self.apiUrl = ip
        self.username = username
        self.password = password
        self.variants = Variant(self)
        self.traits = Trait(self)
        self.annotations = Annotation(self)
        self.pathways = Pathway(self)
        self.biosamples = Biosample(self)
        self.genes = Gene(self)

    def genomeQuery(self):
        return QueryBuilder(self).newGenomeQuery()

    def infoQuery(self):
        return QueryBuilder(self).newInfoQuery()

    def edgeQuery(self):
        return QueryBuilder(self).newEdgeQuery()

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
        return json.loads(requests.post(requestUrl, json=query.get()).content)

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

        if (query.isEdgeOnly):
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