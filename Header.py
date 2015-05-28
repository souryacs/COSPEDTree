#!/usr/bin/env python

import dendropy
from dendropy import treesim 
from dendropy import Tree, Taxon, TaxonSet
from dendropy import treecalc
import itertools
import numpy as np
from numpy import newaxis
import time
from cStringIO import StringIO
from operator import itemgetter
from optparse import OptionParser
from collections import deque

# we define custom edge types
BI_DIRECTED_EDGE = 0	# equality relationship
DIRECTED_OUT_EDGE = 1
DIRECTED_IN_EDGE = 2
NO_EDGE = 3	# no relationship
UNDEFINED_EDGE = 4

''' this variable is for establish a new connection which is not there in the source trees
that is, two nodes are not in the same source tree, 
thus there is no relationship (even the relationship "NO_EDGE" is not there)
and during tree construction, the connection is coming between them '''
ORIG_DIFF_SRC_TREE_CONNECT_SCORE = 0	#-1

''' this variable signifies that original 'NO_EDGE' connection is not preserved in the derived tree '''
ORIG_NO_EDGE_BECOME_CONNECTED = -3 	

''' this is for the case where original 'NO_EDGE' connection is remained in the derived tree '''
ORIG_NO_EDGE_REMAIN_NO_EDGE = 2		

''' this is for the case where originally the nodes are connected (max consensus), 
but 'NO_EDGE' connection is in the derived tree '''
#ORIG_CONNECTED_FINAL_NO_EDGE = -2	#-2

''' declaration of global variables needed to store the structures '''
''' we also note down the species list from the input multiple source tree data '''
Complete_Input_Species_List = []

''' the dictionary defines content of PairLeaf_Node structure '''
PairLeaf_Node_Dict = dict()

''' this dictionary defines the pair wise leaf node connection structure 
each entry is indexed by two nodes '''
Pair_Reln_Dict = dict()

''' this is a dictionary storing cluster of nodes 
each cluster is basically a collection of nodes having equality relationship between the nodes '''
Cluster_Node_Dict = dict()

''' this is the list containing the node pair and the corresponding scores of different edge types
the list is used to extract the maximum edge score to make the connection of next valid node pairs '''
Cost_List_Node_Pair = []

''' if SINGLE_EDGE_TYPE_CONN_PRIORITY option is set, then this list stores the cases 
  where a pair of taxa is connected only by a single edge type 
  (with respect to all the candidate source trees)
  it uses that edge type in the final connection 
  example: suppose two TAXA A and B are related by sibling relationship 
  with respect to all the candidate source trees
  there is no other relation between them 
  in this case, relation between A and B will be inserted in this list '''
single_edge_occurrence_list = [] 

''' this list contains the edges which are established either by original edge connection
or by derived edge connection due to the earlier edge connections
all such edges are maintained in this list
finally, this list is used to update the cost of the remaining non processed edges '''
EDGE_PROCESSED_LIST = []

# counter of node connection
nodes_connected = 0
