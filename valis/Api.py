import requests
from requests.auth import HTTPBasicAuth
import json
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
from .Variant import *
from .Pathway import *

class api:
    def __init__(self, ip='http://35.185.230.75', username=None, password=None):
        self.apiUrl = ip
        self.username = username
        self.password = password
        self.variants = Variant(self)
        self.traits = Trait(self)
        self.patients = Patient(self)
        self.annotations = Annotation(self)
        self.pathways = Pathway(self)
        self.biosamples = Biosample(self)
        self.genes = Gene(self)
        self.region = GenomicRegion(self)

    def check_auth(self):
        if not self.username or not self.password:
            print('You need to login!')
            self.username=input('Enter Username [dev]: ') or 'dev'
            self.password=input('Enter Password: ')
            if not self.username or not self.password:
                raise Exception('Not Logged In')

    def send_get(self, requestUrl):
        self.check_auth()
        return requests.get(requestUrl, auth=HTTPBasicAuth(self.username, self.password))

    def send_post(self, requestUrl, json):
        self.check_auth()
        return requests.post(requestUrl, json=json, auth=HTTPBasicAuth(self.username, self.password))

    def send_delete(self, requestUrl):
        self.check_auth()
        return requests.delete(requestUrl, auth=HTTPBasicAuth(self.username, self.password))

    def login(self, username, password):
        self.username = username
        self.password = password

    def newGenomicRegion(self):
        return GenomicRegion(self)

    def genomeQuery(self):
        return QueryBuilder(self).newGenomeQuery()

    def infoQuery(self):
        return QueryBuilder(self).newInfoQuery()

    def edgeQuery(self):
        return QueryBuilder(self).newEdgeQuery()

    def contigs(self):
        return json.loads(self.send_get('%s/contig_info' % self.apiUrl).content)

    def getUploadedFiles(self):
        files = json.loads(self.send_get('%s/user_files' % self.apiUrl).content)
        final_files = []
        for file in files:
            if not 'tmp-region' in file['fileName']:
                final_files.append(file)
        return final_files


    def getDetails(dataID, userFileID=None):
        requestUrl = '%s/details/%s' % (self.apiUrl, dataID);
        if (userFileID):
            requestUrl = requestUrl + "?userFileID=" + userFileID;
        return json.loads(self.send_get(requestUrl).content)

    def distinctValues(self, key, query):
        requestUrl = '%s/distinct_values/%s' % (self.apiUrl, key);
        result = self.send_post(requestUrl, json=query.get()).content
        try:
            return json.loads(result)
        except:
            print('Request Failed')
            print(result)

    def deleteFile(self, fileID):
      url = '%s/user_files?fileID=%s' % (self.apiUrl, fileID)
      return self.send_delete(url)

    def uploadFile(self, file, name=None):
        url = '%s/user_files' % self.apiUrl
        file_path = file.name
        if '.bed' in file_path:
          file_type = FileType.BED
        elif '.vcf' in file_path:
          file_type = FileType.VCF
        else:
          file_type = FileType.TXT_23ANDME

        if name:
          files = {'file': (name, file), 'fileType' : ('', file_type)}
        else:
          files = {'file': file, 'fileType' : ('', file_type)}
        return self.send_post(url, files=files).content

    def downloadQuery(self, query, output_path, sort=False):
        requestUrl = '%s/download_query' % self.apiUrl
        result = self.send_post(requestUrl, json={ 'query': query.get(), 'sort': sort}).content
        with open(output_path, "wb") as f:
            f.write(result)

    def fetchBAMData(self, fileQuery, intervalQuery):
        pass

    def fetchBigwigData(self, fileQuery, intervalQuery):
        pass

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

        result = json.loads(self.send_post(requestUrl, json=query.get()).content)

        return result['data'], result['reached_end']
