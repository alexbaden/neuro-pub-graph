# Create a graph from publication data by adding an edge between two co-authors on 
# a paper.
# Alex Baden - Copyright 2015
# 20150320 

import pickle
import igraph
import sys

def check_name(author_names, name, cur_author):
  
  name_formatted = name.split(' ')
  for author in author_names.keys():
    if author == cur_author:
      continue
    if author_names[author][0] == name_formatted[0].strip():
      if author_names[author][1] == name_formatted[1].strip()[0]:
        return author

  return None 

def check_paper(paper_id, authors, cur_author):
  for author in sorted(authors.keys()):
    if author == cur_author:
      continue 
    else:
      for paper in authors[author]:
        if int(paper) == int(paper_id):
          return author

  return None 

def process_author_list(authors):
  author_names = {}
  authors_processed = {}

  for author in authors.keys():
    author_formatted = author.split(' ')
    last = author_formatted[1].strip()
    first = author_formatted[0].strip()[0]
    author_names[author] = [last, first]
    authors_processed[author] = []

  for author in sorted(authors.keys()):
    for paper in authors[author]:
      result = check_paper(paper, authors, author)
      if result is not None:
        authors_processed[author].append(result)
  
  return authors_processed

def main():
  with open('pubmed.pickle', 'r') as f:
    data_raw = pickle.load(f)

  authors_raw = data_raw[0]
  departments_raw = data_raw[1]

  authors = process_author_list(authors_raw)
  g = igraph.Graph(directed=False)
  g["name"] = "JHU Neuroscience Graph"
  # add vertices
  for author in authors.keys():
    g.add_vertex(name=author, department=departments_raw[author])
 
  # add edges 
  for author in authors.keys():
    for coauthor in authors[author]:
      g.add_edge(author, coauthor, weight=1)
  """
  # collapse all edges, adding weights
  print "BEFORE:"
  print g.get_adjlist()
  g.simplify(combine_edges=dict(weight=sum))
  print "AFTER:"
  print g.get_adjlist()
  """
  g.write_graphml('graph_output.graphml')
  
if __name__ == '__main__':
  main()
