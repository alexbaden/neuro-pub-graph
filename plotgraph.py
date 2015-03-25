#!/usr/bin/env python

# Copyright 2015 Open Connectome Project (http://openconnecto.me)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# plotgraphs.py
# Created by Greg Kiar on 2015-03-23.
# Email: gkiar@jhu.edu
# Copyright (c) 2015. All rights reserved.

# Load necessary packages
from os import system
from argparse import ArgumentParser
from igraph import Graph, Layout, plot
from scipy.sparse import csgraph
from scipy.linalg import eig
from numpy import ceil, zeros, asarray, eye, array, sqrt, transpose, log

def compute_clusters(graph):
  lap_data = csgraph.laplacian(asarray(graph.get_adjacency(attribute="weight").data), normed=False)
  lap_cov = covariate_laplacian(graph, 'department')
  lap_total = 1*lap_data + 10000000000*lap_cov + 1000*eye(len(graph.vs)) + 1000000

  [evals, evecs] = eig(lap_total)
  
  coords = array((log(evecs[2]/sqrt(evals[2])), log(evecs[1]/sqrt(evals[1]))))
  coords = transpose(abs(coords))
  return coords

def set_colors(graph):
  for i in range(0, len(graph.vs)):
  	graph.vs[i]['color'] = get_color(graph.vs[i]['department'])

def get_color(d):
	return {'Neuroscience': 'indianred', 'Neurology': 'lightslateblue',
	  'Psychological and Brain Sciences': 'royalblue', 'Biomedical Engineering': 'powderblue',
	  'Biology': 'orchid', 'Molecular Biology': 'seagreen', 'Computer Science': 'aquamarine',
	  'Electrical Engineering': 'pink', 'Pharmacology': 'lightsteelblue', 'Radiology': 'hotpink',
	  'Chemical and Biomolecular Engineering': 'khaki', 'Applied Mathematics and Statistics': 'lawngreen',
	  'Applied Physics Laboratory': 'magenta', 'Physics': 'lightseagreen', 'Biostatistics': 'orange',
	  'Materials Science an Engineering': 'linen', 'Mind and Brain Institute':'purple',
	  'Cellular and Molecular Medicine':'gray'}[d]

def covariate_laplacian(graph, attr):
  lap = zeros([len(graph.vs), len(graph.vs)])
  for i in range(0, len(graph.vs)):
  	for j in range(0, len(graph.vs)):
  		if graph.vs[i][attr] == graph.vs[j][attr]:
  		  lap[i][j] = 1.0
  return lap

def main():
  parser = ArgumentParser()
  parser.add_argument("graph", action="store", help="The graph which you want to plot in 2D")
  result = parser.parse_args()

  graph = Graph.Read_GraphML(result.graph)
  #for i in graph.vs:
  # if i.degree() is 0:
  #	print i.degree()
  #	i.delete()
  cluster_locs = compute_clusters(graph)
  set_colors(graph)

  #import pdb ; pdb.set_trace()
  graph.vs["label"] = graph.vs["name"]
  lays = Layout(tuple(map(tuple,cluster_locs)))
  plot(graph, target='/Users/gkiar/git/neuro-pub-graph/temp.png', layout=graph.layout("kamada_kawai"), edge_width=log(graph.es["weight"]))
  #import pdb ; pdb.set_trace() #graph.layout("kamada_kawai")

if __name__=='__main__':
  main()


