from uuid import uuid4
import os

class GenomicRegion:
  def __init__(self, api):
    self.api = api

  def createFromIntervals(self, intervals):
    fname = './tmp-region-' + str(uuid4()) + str('.bed')
    with open(fname, 'w') as f:
      for interval in intervals:
        f.write('\t'.join([interval[0], str(interval[1]-1), str(interval[2] - 1)]) + '\n')
    ret = self.createFromBed(open(fname, 'rb'))
    os.remove(fname)
    return ret

  def createFromBed(self, file):
    name = 'tmp-region-' + str(uuid4()) + str('.bed')
    self.api.uploadFile(file, name)
    files = self.api.getUploadedFiles()
    for file in files:
      if file['fileName'] == name:
        return self.api.genomeQuery().setUserFileID(file['fileID'])
    raise 'Failed to contact server'

  def get(self):
    # return query defining this genomic region
    pass