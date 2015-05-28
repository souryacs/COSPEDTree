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
''' this function check whether node1 is an ancestor of node2 '''
def Check_Ancestor(node1, node2):
  flag = 0
  while (1):
    if (node1 == node2):
      flag = 1
      break
    else:        
      if (node2.parent_node is not None):
	node2 = node2.parent_node
      else:
	break
  return flag    
    
##-----------------------------------------------------
''' this function defines relationship between a pair of taxa, with respect to a particular tree
a taxa is represented by a leaf node in a tree 
the relationship is either ancestor / descendant, or siblings, or no relationship '''
def DefineLeafPairReln(species1, species2, Curr_tree):
  # find the nodes in the tree corresponding to the input taxa
  node1 = Curr_tree.find_node_with_taxon_label(species1)
  node2 = Curr_tree.find_node_with_taxon_label(species2)
  # key helps to find out the content in the structure "Pair_Reln_Dict"
  key = (species1, species2)

  ''' at first check whether the parent of these two nodes are same
  in that case, the pair of tuples are in equality relationship '''
  if (node1.parent_node == node2.parent_node):
    Pair_Reln_Dict[key]._AddEdgeCount(BI_DIRECTED_EDGE)
    PairLeaf_Node_Dict[species1]._AddOrigEdge(species2, BI_DIRECTED_EDGE)
    PairLeaf_Node_Dict[species2]._AddOrigEdge(species1, BI_DIRECTED_EDGE)
    #print species1, ' and ', species2, 'are connected via BI_DIRECTED_EDGE '
  elif (Check_Ancestor(node1.parent_node, node2.parent_node) == 1):	
    # checking whether node1 is ancestor of node2
    Pair_Reln_Dict[key]._AddEdgeCount(DIRECTED_OUT_EDGE)
    PairLeaf_Node_Dict[species1]._AddOrigEdge(species2, DIRECTED_OUT_EDGE)
    PairLeaf_Node_Dict[species2]._AddOrigEdge(species1, DIRECTED_IN_EDGE)
    #print species1, ' to ', species2, ' --- DIRECTED_OUT_EDGE '
  elif (Check_Ancestor(node2.parent_node, node1.parent_node) == 1):
    # checking whether node2 is ancestor of node1
    Pair_Reln_Dict[key]._AddEdgeCount(DIRECTED_IN_EDGE)
    PairLeaf_Node_Dict[species1]._AddOrigEdge(species2, DIRECTED_IN_EDGE)
    PairLeaf_Node_Dict[species2]._AddOrigEdge(species1, DIRECTED_OUT_EDGE)
    #print species1, ' to ', species2, ' --- DIRECTED_IN_EDGE '
  else:
    #otherwise the nodes do not have any kind of relationship
    Pair_Reln_Dict[key]._AddEdgeCount(NO_EDGE)
    PairLeaf_Node_Dict[species1]._AddOrigEdge(species2, NO_EDGE)
    PairLeaf_Node_Dict[species2]._AddOrigEdge(species1, NO_EDGE)    
    #print species1, ' to ', species2, ' --- NO_EDGE '    
