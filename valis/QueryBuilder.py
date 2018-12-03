import json
from .QueryType import *

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
      return self
    if len(value) == 1:
      value = value[0]
    if (type(value) == list):
      if value[0] == 'AND':
        self.query['filters'][filterKey] = { '$all' : value[1:] };
      elif value[0] == 'OR':
        self.query['filters'][filterKey] = { '$in' : value[1:] };
      else:
        self.query['filters'][filterKey] = { '$in' : value };
    else:
      self.query['filters'][filterKey] = value;
    return self

  def setUserFileID(self, userFileID):
    copy = self.duplicate()
    copy.query['userFileID'] = userFileID
    return copy

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
    copy.setFilterValue('contig', contig)
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
    copy.query['filters']['info.p-value'] = { '<': pvalue };
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
    copy.setFilterValue('info.assay',assay);
    return copy
  
  def filterOutType(self, outType):
    copy = self.duplicate()
    copy.setFilterValue('info.outtype', outType);
    return copy
  
  def filterVitalStatus(self, vitalStatus):
    copy = self.duplicate()
    copy.setFilterValue('info.vital_status', vitalStatus);
    return copy

  def filterPatientBarCode(self, outType):
    copy = self.duplicate()
    copy.setFilterValue('info.patient_barcodes', outType);
    return copy

  def filterPatientGender(self, gender):
    copy = self.duplicate()
    copy.setFilterValue('info.gender', gender);
    return copy

  def filterPatientDisease(self, disease_code):
    copy = self.duplicate()
    copy.setFilterValue('info.disease_code', disease_code);
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

  def filterRegion(self, contig, start, end):
    copy = self.duplicate()
    copy.filterContig(contig)
    copy.query['filters']['start'] = { '>' : start }
    copy.query['filters']['end'] = { '<' : end }
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

  def fetch(self, full=False, startIdx=None, endIdx=None, limit=None):
    if not limit:
      limit = 1000000
    result, has_more = self.api.getQueryResults(self.setLimit(limit), full, startIdx, endIdx)
    return result

  def release(self):
    if 'userFileID' in self.query:
      self.api.deleteFile(self.query['userFileID'])
    else:
      raise 'Cannot release query (not a user generated data file)'
  
  def distinctValues(self, key):
    return self.api.distinctValues(key, self)

  def saveAsBed(self, outputPath, sortResults=False):
    return self.api.downloadQuery(self.query, outputPath, sortResults)
