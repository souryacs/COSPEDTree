#!/usr/bin/env python

import Header
from Header import *

##-----------------------------------------------------
''' this class defines a leaf node of input candidate source trees
that is, it corresponds to one taxa '''
class PairLeaf_Node(object):
  def __init__(self):
    # these lists store original edge lists (from the input data)
    # that is, from the data of input candidate source trees, these lists contain the nodes (taxa) 
    # which are related to current taxa 
    # lists are classified according to the relationship type
    # these lists are updated during the formation of consensus tree, for lowering computation 
    self.orig_out_edge_list = []
    self.orig_in_edge_list = []
    self.orig_eq_edge_list = []
    self.orig_no_edge_list = []
    # these lists store the final obtained lists (obtained using direct edges) corresponding to the final consensus tree
    # these lists are updated according to the consensus tree formation
    # lists are classified according to the relationship type
    self.Final_out_edge_list = []
    self.Final_in_edge_list = []    
    self.Final_eq_edge_list = []
    self.Final_no_edge_list = []
    
    ''' this variable signifies whether current taxa is a part of a proper cluster 
    a cluster contains set of taxa mutually related via sibling relationship
    if the value is 0 then it is still not inserted in a cluster 
    unless the number is 1 '''
    self.clust_elem_insert = 0

  def _GetClustInsertStatus(self):
    return self.clust_elem_insert
    
  def _SetClustInsertStatus(self):
    self.clust_elem_insert = 1
  
  # these functions remove taxa from the original edge list of the current taxa
  # according to the original candidate source trees, list of taxa related via certain relationship type were maintained
  # those information is deleted if not required further
  def _SelectivelyRemoveEdgeOrigConn(self, edge_type, other_node_idx):
    if (edge_type == BI_DIRECTED_EDGE) and (other_node_idx in self.orig_eq_edge_list):
      self.orig_eq_edge_list.remove(other_node_idx)
    elif (edge_type == DIRECTED_IN_EDGE) and (other_node_idx in self.orig_in_edge_list):
      self.orig_in_edge_list.remove(other_node_idx)
    elif (edge_type == DIRECTED_OUT_EDGE) and (other_node_idx in self.orig_out_edge_list):
      self.orig_out_edge_list.remove(other_node_idx)
    elif (edge_type == NO_EDGE) and (other_node_idx in self.orig_no_edge_list):
      self.orig_no_edge_list.remove(other_node_idx)
    
  def _RemoveEdgeFromOriginalConnectivity(self, other_node_idx):
    for edge_type in range(4):
      self._SelectivelyRemoveEdgeOrigConn(edge_type, other_node_idx)
        
  # these functions add taxa to the original edge list of the current taxa
  # according to the original candidate source trees, list of taxa related via certain relationship type are inserted
  def _AddOrigEdge(self, other_node_idx, edge_type):
    if (edge_type == BI_DIRECTED_EDGE) and (other_node_idx not in self.orig_eq_edge_list):
      self.orig_eq_edge_list.append(other_node_idx)
    if (edge_type == DIRECTED_IN_EDGE) and (other_node_idx not in self.orig_in_edge_list):
      self.orig_in_edge_list.append(other_node_idx)
    if (edge_type == DIRECTED_OUT_EDGE) and (other_node_idx not in self.orig_out_edge_list):
      self.orig_out_edge_list.append(other_node_idx)
    if (edge_type == NO_EDGE) and (other_node_idx not in self.orig_no_edge_list):
      self.orig_no_edge_list.append(other_node_idx)
      
  # this function inserts the final connected taxa with respect to current taxa
  # depending on the connection type, appropriate edge list is considered
  # after inserting the edge type (w.r.t target taxa, those information is removed from the original edge list)
  def _AddFinalEdge(self, edge_type, other_node_idx):
    if (edge_type == BI_DIRECTED_EDGE):
      if (other_node_idx not in self.Final_eq_edge_list):
	self.Final_eq_edge_list.append(other_node_idx)
    if (edge_type == DIRECTED_IN_EDGE):
      if (other_node_idx not in self.Final_in_edge_list):
	self.Final_in_edge_list.append(other_node_idx)
    if (edge_type == DIRECTED_OUT_EDGE):
      if (other_node_idx not in self.Final_out_edge_list):
	self.Final_out_edge_list.append(other_node_idx)	
    if (edge_type == NO_EDGE):
      if (other_node_idx not in self.Final_no_edge_list):
	self.Final_no_edge_list.append(other_node_idx)	    
    # now remove this edge information from the original connectivity edges, 
    # as only the remaining non-processed (non-finalized) nodes will be considered
    self._RemoveEdgeFromOriginalConnectivity(other_node_idx)
      
  # these functions return the final connectivity (w.r.t consensus tree) of the current taxa
  # depending on the edge type
  def _GetFinalEqEdgeList(self):
    return self.Final_eq_edge_list
    
  def _GetFinalOutEdgeList(self):
    return self.Final_out_edge_list

  def _GetFinalInEdgeList(self):
    return self.Final_in_edge_list
    
  def _GetFinalNoEdgeList(self):
    return self.Final_no_edge_list    
  
  # these functions return list of taxa w.r.t certain edge types those are yet not considered (or discarded)
  # for final supertree construction
  # depending on the edge type
  def _GetNonProcessedEqEdgeList(self):
    return self.orig_eq_edge_list
    
  def _GetNonProcessedOutEdgeList(self):
    return self.orig_out_edge_list

  def _GetNonProcessedInEdgeList(self):
    return self.orig_in_edge_list

  def _GetNonProcessedNoEdgeList(self):
    return self.orig_no_edge_list
    
  # this function prints the information of one taxa after processing input candidate source trees
  def _PrintOriginalNodeInfo(self):
    print 'original out edge list: ', self.orig_out_edge_list
    print 'original in edge list: ', self.orig_in_edge_list
    print 'original eq edge list: ', self.orig_eq_edge_list
    print 'original no edge list: ', self.orig_no_edge_list
    
  # this function is called after formation of consensus tree
  def _PrintFinalNodeInfo(self):
    print 'final out edge list: ', self.Final_out_edge_list
    print 'final in edge list: ', self.Final_in_edge_list
    print 'final eq edge list: ', self.Final_eq_edge_list
    print 'final no edge list: ', self.Final_no_edge_list
