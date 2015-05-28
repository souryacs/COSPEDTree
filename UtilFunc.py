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
''' this function generates leaf node list '''
def Generate_Node_List(Leaf_node_list):  
  Node_list = [''.join(Leaf_node_list[i].taxon.label) for i, lf in enumerate(Leaf_node_list)]
  return Node_list  
    
##-----------------------------------------------------
''' this function reads the input tree collection file
the file contains a collection of input candidate source trees
each such tree is composed of a large no of taxa (placed at the leaves of the tree) '''
def Read_Species_Data(ROOTED_TREE, PRESERVE_UNDERSCORE, INPUT_FILE_FORMAT, INPUT_FILENAME):
  ''' depending on the value of INPUT_FILE_FORMAT
  the data is read from the file according to NEWICK or NEXUS format '''
  if (INPUT_FILE_FORMAT == 1):
    Species_TreeList = dendropy.TreeList.get_from_path(INPUT_FILENAME, \
						      schema="newick", \
						      preserve_underscores=PRESERVE_UNDERSCORE, \
						      default_as_rooted=ROOTED_TREE)
  else:
    Species_TreeList = dendropy.TreeList.get_from_path(INPUT_FILENAME, \
						      schema="nexus", \
						      preserve_underscores=PRESERVE_UNDERSCORE, \
						      default_as_rooted=ROOTED_TREE)
  
  return Species_TreeList
    
