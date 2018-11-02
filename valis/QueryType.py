from enum import EnumMeta

class QueryType(EnumMeta):
  GENOME = 'GenomeNode'
  INFO = 'InfoNode'
  EDGE = 'EdgeNode'