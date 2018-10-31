from valis import ValisAPI

client = ValisAPI('http://35.185.230.75', None, None)
q = client.genomeQuery().filterType('gene')
print(client.getQueryResults(q, True, 0, 10))

