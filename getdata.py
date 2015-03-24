# Download Publication Data from Pubmed
# Alex Baden - Copyright 2015
# 20150320

from urllib2 import Request, urlopen, quote, URLError
from urllib import urlencode
import httplib 
import json
import pickle 
import time
import sys

def get_author_pubs(author):
  #author_text = author.split(' ')
  #author_string = "{}, {}[Author]".format(author_text[1].strip(), author_text[0].strip())
  author_string = "{}[Author]".format(author) #.strip(), author_text[0].strip())
  author_term = quote(author_string)
  url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=1000&term={}".format(author_term)

  request = Request(url)
      
  try:
    response = urlopen(request)
    papers = response.read()
  except URLError, e:
    print "Received error code in get pubs", e

  return papers

def get_paper_authors(author_raw):
  # papers[id] = authors 
  papers = {}
  
  author_json = json.loads(author_raw)
  author_ids = author_json['esearchresult']['idlist']
  print "Getting " + str(len(author_ids)) + " papers"
  for i in xrange(0,len(author_ids),15):
    start = i
    end = (i + 14) 
    if end > len(author_ids): 
      end = len(author_ids)
    print "start: " + str(start) + ", end: " + str(end)
    idlist = ','.join(author_ids[start:end]) 
    print idlist  
    url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&rettype=abstract&id={}".format(idlist)
    print url
    request = Request(url)
      
    try:
      response = urlopen(request)
      abstracts_raw = response.read()
    except URLError, e:
      print "Received error code in get papers", e
    
    abstracts = json.loads(abstracts_raw)
    if 'result' in abstracts:
      for abstract in abstracts['result']:
        if abstract != 'uids':
          papers[abstract] = abstracts['result'][abstract]['authors']
  
  return papers

def main():
  # authors[name] = papers (papers is a dict of id => authors on paper)
  authors = {}
  # departments[name] = department (string) 
  departments = {}

  with open('faculty') as f:
    for line in f:
      tmp = line.split(';')
      authors[tmp[0].strip()] = tmp[1].strip()
      departments[tmp[0].strip()] = tmp[2].strip()

  for author in sorted(authors.keys()):
    print "Processing ", author
    paperstmp = get_author_pubs(authors[author]) 
    authors[author] = get_paper_authors(paperstmp)
    time.sleep(5)

  with open('pubmed.pickle', 'w') as f:
    pickle.dump([authors, departments], f)
    
if __name__ == '__main__':
  main()

