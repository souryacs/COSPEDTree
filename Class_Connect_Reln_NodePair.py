#!/usr/bin/env python

import Header
from Header import *

##-----------------------------------------------------
''' this class defines the connectivity relationship between a pair of nodes
where each node is represented by one taxa 
initially the instances of the class are formed both from the input source trees
later the contents of these class instances are modified according to the generation of the consensus tree 
key of this class --- node1, node2 (pair of nodes) '''
class Connect_Reln_NodePair(object):
  # for a pair of nodes, input edge list is formed from input source trees, based on different edge connectivity 
  def __init__(self, fin_edge_tp):    
    # this is the final selected edge type that is established between two nodes 
    self.final_selected_edge_type = fin_edge_tp
    ''' this variable denotes the no of occurrences of a particular edge type 
    there are 4 types of edges (relationship) between a pair of taxa '''
    self.edge_weight = [0] * 4    
    ''' a connection priority value is defined as the 
    no of occurrences of this particular edge type between these pair of nodes 
    minus the sum of no of occurrences of other edge types between these pair of nodes '''
    self.conn_pr_val = [0] * 4    
    ''' this cost variable denotes the cost associated with different types of edge connection between 
    these pair of nodes considered 
    this value is updated during generation of the consensus tree '''
    self.Connect_Edge_Cost = [0] * 4
    ''' number of different edge types between these two nodes 
    according to different input source trees 
    if this value is 1 then corresponding taxa pair will be inserted in the single_edge_occurrence_list 
    this is used only when FRACTION_EDGE_WEIGHT option is enabled '''
    self.diff_inp_edge_type = 0
        
  def _GetEdgeWeight(self, edge_type):
    return self.edge_weight[edge_type]      
    
  def _GetEdgeCost_ConnReln(self, edge_type):
    return self.Connect_Edge_Cost[edge_type]
    
  def _IncrEdgeCost_ConnReln(self, edge_type, incr_cost):
    self.Connect_Edge_Cost[edge_type] = self.Connect_Edge_Cost[edge_type] + incr_cost

  # this function adds one edge count (with a given input edge type)
  def _AddEdgeCount(self, edge_type):
    self.edge_weight[edge_type] = self.edge_weight[edge_type] + 1
    
  # this function appends one final connected edge (for use in final supertree) 
  def _UpdateFinalEdgeInfo(self, edge_type):
    self.final_selected_edge_type = edge_type
    
  # this function prints the relationship information
  def _PrintRelnInfo(self):
    print 'edges [type/count/conn_pr_val]: '
    for i in range(4):
      print '[', i, '/', self.edge_weight[i], '/', self.conn_pr_val[i], ']'
    print 'final selected edge type : ', self.final_selected_edge_type
    
  ##-------------------------------------------------
  # this function computes the score metric value associated with individual pair of taxa 
  def _SetCostMetric(self, NewScheme, taxon1, taxon2):
    for edge_type in range(4):
      #---------------------------------
      if (NewScheme == 0):
	c = 1
      elif (NewScheme == 1):
	if (edge_type == DIRECTED_OUT_EDGE):
	  c = (len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedOutEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedEqEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedInEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedEqEdgeList())) / 2
	elif (edge_type == DIRECTED_IN_EDGE):
	  c = (len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedInEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedEqEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedOutEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedEqEdgeList())) / 2
	elif (edge_type == BI_DIRECTED_EDGE):
	  c = (len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedInEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedOutEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedEqEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedOutEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedEqEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedInEdgeList())) / 2
	else:	# NO_EDGE
	  c = (len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedInEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedOutEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedEqEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon1]._GetNonProcessedNoEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedOutEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedEqEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedInEdgeList())\
	      + len(PairLeaf_Node_Dict[taxon2]._GetNonProcessedNoEdgeList())) / 2
      else:
	#----------------------------
	# earlier code - sourya
	c = self.edge_weight[edge_type]
	#----------------------------
	# modified - sourya
	#if (self.edge_weight[edge_type] > 0):
	  ## this edge weight
	  #c = self.edge_weight[edge_type]
	#else:
	  ## average of other non zero weights
	  #cc = 0
	  #avg_wt = 0
	  #for et in range(4):
	    #if (self.edge_weight[et] > 0):
	      #cc = cc + 1
	      #avg_wt = avg_wt + self.edge_weight[et]
	  #c = avg_wt / cc
	#----------------------------
      #---------------------------------
      # assign the score metric for this edge type
      self.Connect_Edge_Cost[edge_type] = c * self.conn_pr_val[edge_type]
  
  ##-------------------------------------------------
  ''' this function calculates connection priority value for each of the edge types, 
  for this particular connection between a pair of nodes in the final tree '''
  def _SetConnPrVal(self, single_edge_prior, FRACTION_EDGE_WEIGHT):
    # determine the number of different edge types having non zero count (according to input source trees) 
    if FRACTION_EDGE_WEIGHT:
      for edge_type in range(4):
	if (self.edge_weight[edge_type] > 0):
	  self.diff_inp_edge_type = self.diff_inp_edge_type + 1
    # this is the sum of all the edge type instances (no of occurrences)
    listsum = sum(self.edge_weight)
    # now determine the connection priority of a particular edge type with respect to other edges     
    for edge_type in range(4):
      if (not FRACTION_EDGE_WEIGHT):
	# here we use the difference of current edge type frequency with the frequencies of all other edge types 
	self.conn_pr_val[edge_type] = 2 * self.edge_weight[edge_type] - listsum
      else:
	# here we normalize the difference with respect to the different input edge types having non zero occurrences in the source trees
	self.conn_pr_val[edge_type] = (2 * self.edge_weight[edge_type] - listsum) * (1.0) / self.diff_inp_edge_type
    
    ''' this code section is used when there exists NO EDGE relationship between a pair of taxa
    and we want to detect it '''
    if (not single_edge_prior):
      ''' if there is no vote for any particular edge type other than NO_EDGE,
      (that is, corresponding settings did not occur in any of the source tree)
      then we make only the NO_EDGE settings as valid - 
      they will only be considered for joining this pair in the final tree '''
      if (self.edge_weight[NO_EDGE] != 0)\
	and (self.edge_weight[DIRECTED_IN_EDGE] == 0)\
	and (self.edge_weight[DIRECTED_OUT_EDGE] == 0)\
	and (self.edge_weight[BI_DIRECTED_EDGE] == 0):
	return 1
      else:
	return 0
    else:
      outlist = [0, NO_EDGE]
      for edge_type in range(4):
	if (self.edge_weight[edge_type] == listsum) and (listsum > 0):
	  outlist = [1, edge_type]
	  break
	elif (self.edge_weight[edge_type] > 0) and (self.edge_weight[edge_type] < listsum):
	  break
      return outlist
  
  ##-------------------------------------------------
  # this function returns the connection priority value for input edge type
  def _GetConnPrVal(self, edge_type):
    return self.conn_pr_val[edge_type]
