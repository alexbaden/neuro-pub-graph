import pickle
import igraph
import sys

def check_name(author_names, name, cur_author):
  
  name_formatted = name.split(' ')
  for author in author_names.keys():
    if author == cur_author:
      continue
    if author_names[author] ==  name_formatted[0].strip():
      return author

  return None 

def process_author_list(authors):
  author_names = {}
  authors_processed = {}

  for author in authors.keys():
    author_formatted = author.split(' ')
    last = author_formatted[1].strip()
    author_names[author] = last
    authors_processed[author] = []

  for author in sorted(authors.keys()):
    for paper in authors[author]:
      for listedauth in authors[author][paper]:
        if listedauth['authtype'] == 'Author':
          result = check_name(author_names, listedauth['name'], author)
          if result is not None:
            authors_processed[author].append(result)
  
  return authors_processed

def main():
  with open('pubmed.pickle', 'r') as f:
    authors_raw = pickle.load(f)


  authors = process_author_list(authors_raw)
  print authors 
  sys.exit(0)
  g = igraph.Graph(directed=True)
  g["name"] = "JHU Neuroscience Graph"
  # add vertices
  for author in authors.keys():
    g.add_vertex(name=author)
 
  # add edges 
  #TODO

if __name__ == '__main__':
  main()
