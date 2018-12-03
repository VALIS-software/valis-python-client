from .QueryBuilder import *
from .GenomeType import *
from .FileType import *
from .QueryType import *
from .Dataset import *
from .Patient import *
from .Trait import *
from .GenomicRegion import * 
from .Gene import *
from .Annotation import *
from .Biosample import *
from .Api import api

def ALL(d):
  return ['AND'] + d

def ANY(d):
  return ['OR'] + d

valis = api()