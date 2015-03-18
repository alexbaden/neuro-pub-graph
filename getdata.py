from urllib2 import Request, urlopen, quote, URLError
from urllib import urlencode
import httplib 
import json
import pickle 
import time
import sys

def get_author_pubs(author):
  author_text = author.split(' ')
  author_string = "{}, {}[Full Author Name]".format(author_text[1].strip(), author_text[0].strip())
  author_term = quote(author_string)
  url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=1000&term={}".format(author_term)

  request = Request(url)
      
  try:
    response = urlopen(request)
    papers = response.read()
  except URLError, e:
    print "Received error code", e

  return papers

def get_paper_authors(author_raw):
  # papers[id] = authors 
  papers = {}
  
  author_json = json.loads(author_raw)
  author_ids = author_json['esearchresult']['idlist']
  idlist = ','.join(author_ids) 
  
  url = 'eutils.ncbi.nlm.nih.gov'
  params = urlencode({'db':'pubmed','retmode':'json','rettype':'abstract','id':idlist})
  headers = {"Content-type": "application/x-www-form-urlencoded",
      "Accept": "text/plain"}
  try:
    conn = httplib.HTTPConnection(url)
    conn.request("POST", "/entrez/eutils/esummary.fcgi", params, headers)
    response = conn.getresponse()
    abstracts_raw = response.read()
  except httplib.HTTPException, e:
    print "Received error code", e

  print abstracts_raw
  abstracts = json.loads(abstracts_raw)
  #print abstracts 
  if 'result' in abstracts:
    for abstract in abstracts['result']:
      if abstract != 'uids':
        papers[abstract] = abstracts['result'][abstract]['authors']
  
    return papers
  else:
    return None 

def main():
  # authors[name] = papers (papers is a dict of id => authors on paper)
  authors = {}

  with open('faculty') as f:
    for line in f:
      authors[line.strip()] = None

  for author in sorted(authors.keys()):
    paperstmp = get_author_pubs(author) 
    print paperstmp 
    authors[author] = get_paper_authors(paperstmp)
    time.sleep(5)

  with open('pubmed.pickle') as f:
    pickle.dump(authors, f)

if __name__ == '__main__':
  main()

