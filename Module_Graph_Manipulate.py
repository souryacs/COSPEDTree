#!/usr/bin/env python

import Header
from Header import *

import Class_Cluster_node
from Class_Cluster_node import *
import Class_Connect_Reln_NodePair
from Class_Connect_Reln_NodePair import *
import Class_PairLeaf_Node
from Class_PairLeaf_Node import *

##-----------------------------------------------------        
''' this function returns the root node for the final supertree 
for a depth first forest, multiple root nodes can be possible - so it returns the node with 0 indegree '''
def Extract_Node_Min_Indeg(no_of_clusters):
  min_indeg_node_idx = -1
  valid_node_found = 0
  for i in Cluster_Node_Dict:
    if (Cluster_Node_Dict[i]._GetExploredStatus() == 0):
      if (valid_node_found == 0):
	min_indeg = Cluster_Node_Dict[i]._Get_Indegree()
	min_indeg_node_idx = i
	valid_node_found = 1
      elif (valid_node_found == 1) and (Cluster_Node_Dict[i]._Get_Indegree() < min_indeg):
	min_indeg = Cluster_Node_Dict[i]._Get_Indegree()
	min_indeg_node_idx = i
      elif (valid_node_found == 1) and (Cluster_Node_Dict[i]._Get_Indegree() == min_indeg)\
	    and (Cluster_Node_Dict[i]._Get_Outdegree() > Cluster_Node_Dict[min_indeg_node_idx]._Get_Outdegree()):    
	min_indeg = Cluster_Node_Dict[i]._Get_Indegree()
	min_indeg_node_idx = i
    
  return min_indeg_node_idx
  
##-----------------------------------------------------
# this function prints the tree in Newick format
def PrintNewick(root_species_idx, EQUIV_PART):
  Tree_Str_List = ''
  # process the node provided it has not been explored yet
  if (Cluster_Node_Dict[root_species_idx]._GetExploredStatus() == 0):  
    # set the explored status of the current node to true
    Cluster_Node_Dict[root_species_idx]._SetExploredStatus()
    
    # get the out edge list of the current node which are not explored yet 
    outnodes = []
    for l in Cluster_Node_Dict[root_species_idx]._GetOutEdgeList():
      if (Cluster_Node_Dict[l]._GetExploredStatus() == 0):
	outnodes.append(l)
      
    if (len(outnodes) == 0):
      if (EQUIV_PART) and (len(Cluster_Node_Dict[root_species_idx]._GetSpeciesList()) > 1):
	Tree_Str_List = Tree_Str_List + '('
      # modify - sourya
      if 0:
	Tree_Str_List = Tree_Str_List + ','.join(Cluster_Node_Dict[root_species_idx]._GetSpeciesList())
      else:
	Tree_Str_List = Tree_Str_List + ','.join("'" + item + "'" for item in Cluster_Node_Dict[root_species_idx]._GetSpeciesList())
      # end modify - sourya
      if (EQUIV_PART) and (len(Cluster_Node_Dict[root_species_idx]._GetSpeciesList()) > 1):
	Tree_Str_List = Tree_Str_List + ')'
    else:
      Tree_Str_List = Tree_Str_List + '('
      # modify - sourya
      if 0:
	Tree_Str_List = Tree_Str_List + ','.join(Cluster_Node_Dict[root_species_idx]._GetSpeciesList())
      else:
	Tree_Str_List = Tree_Str_List + ','.join("'" + item + "'" for item in Cluster_Node_Dict[root_species_idx]._GetSpeciesList())
      # end modify - sourya
      Tree_Str_List = Tree_Str_List + ','    
      Tree_Str_List = Tree_Str_List + '('
      for i in range(len(outnodes)):
	Tree_Str_List = Tree_Str_List + PrintNewick(outnodes[i], EQUIV_PART)
	if (i < (len(outnodes) - 1)):
	  Tree_Str_List = Tree_Str_List + ','
      Tree_Str_List = Tree_Str_List + ')'
      Tree_Str_List = Tree_Str_List + ')'
    
  return Tree_Str_List
  
##-----------------------------------------------------  
''' this function performs transitive reduction of a graph (transitive closure) and subsequently modifies the cluster of nodes
in terms of the edge connectivity, to make it free of redunant edges '''
def CompressDirectedGraph(Cluster_Graph_Trans_Closure_Adj_Mat, no_of_clusters):  
  # reflexive reduction
  for i in range(no_of_clusters):
    Cluster_Graph_Trans_Closure_Adj_Mat[i][i] = 0
    
  # transitive reduction
  for j in range(no_of_clusters):
    for i in range(no_of_clusters):
      if (Cluster_Graph_Trans_Closure_Adj_Mat[i][j] == 1):
	for k in range(no_of_clusters):
	  if (Cluster_Graph_Trans_Closure_Adj_Mat[j][k] == 1):
	    Cluster_Graph_Trans_Closure_Adj_Mat[i][k] = 0
	    # remove the edge from the cluster node directory
	    Cluster_Node_Dict[i+1]._RemoveOutEdge(k+1)
	    Cluster_Node_Dict[k+1]._RemoveInEdge(i+1)

##-----------------------------------------------------
# this function computes the transitive closure of the given matrix
def Form_Transitive_Closure(Cluster_Graph_Adj_Mat, Cluster_Graph_Trans_Closure_Adj_Mat, no_of_clusters):
  for i in range(no_of_clusters):
    oel = Cluster_Node_Dict[i+1]._GetOutEdgeList()
    for j in range(no_of_clusters):
      if (i == j) or ((j+1) in oel):
	Cluster_Graph_Adj_Mat[i][j][0] = 1
      else:
	Cluster_Graph_Adj_Mat[i][j][0] = 0
      
  for k in range(no_of_clusters):
    for i in range(no_of_clusters):
      for j in range(no_of_clusters):
	if (Cluster_Graph_Adj_Mat[i][j][k] == 1):
	  Cluster_Graph_Adj_Mat[i][j][k+1] = 1
	elif (Cluster_Graph_Adj_Mat[i][k][k] == 1) and (Cluster_Graph_Adj_Mat[k][j][k] == 1):
	  Cluster_Graph_Adj_Mat[i][j][k+1] = 1
	else:
	  Cluster_Graph_Adj_Mat[i][j][k+1] = 0

  # now copy the transitive closure output
  for i in range(no_of_clusters):
    for j in range(no_of_clusters):
      Cluster_Graph_Trans_Closure_Adj_Mat[i][j] = Cluster_Graph_Adj_Mat[i][j][no_of_clusters]
  
  return
  
