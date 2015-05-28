#!/usr/bin/env python

import Header
from Header import *

##-----------------------------------------------------
''' this class is representative of a cluster of nodes
each node represents one input taxa
a cluster of node is formed by collecting all the taxa that are related via equality relationship 
according to the rule of equivalence partition '''
class Cluster_node(object):
  def __init__(self, Tuple=None):
    # this list contains the species list of the current cluster
    self.Species_List = [] 
    # can be 0 or 1 - denote whether the cluster node has been explored during newick string construction
    self.explored = 0    
    # this variable stores the out edge list from this cluster
    # each list element is the other cluster index
    # this is formed during initial construction of the cluster
    self.out_edge_list = []
    # this variable stores the in edge list from this cluster
    # each list element is the other cluster index 
    # this is formed during initial construction of the cluster
    self.in_edge_list = []
    # during initialization, append one tuple to this cluster
    if Tuple is not None:
      self._Append_tuple(Tuple)    

  # these functions keep track whether the cluster node is used during newick string formation for supertree construction
  # each of the clusters (containing a set of taxa) should be visited exactly once for supertree generation
  def _SetExploredStatus(self):
    self.explored = 1

  def _ResetExploredStatus(self):
    self.explored = 0
    
  def _GetExploredStatus(self):
    return self.explored
          
  # returns the constituent species list of this cluster
  def _GetSpeciesList(self):
    return self.Species_List
        
  # append one species information in this cluster
  def _Append_tuple(self, Tuple):
    if Tuple not in self.Species_List:
      self.Species_List.append(Tuple)

  # it returns the original connectivity -- out edge -- of the cluster node to the other nodes (clique formation)
  def _GetOutEdgeList(self):
    return self.out_edge_list
    
  # it returns the original connectivity -- in edge -- of the cluster node to the other nodes (clique formation)
  def _GetInEdgeList(self):
    return self.in_edge_list    
    
  # it returns the final cluster node connectivity (tree shape) -- in edges
  def _Get_Indegree(self):
    return len(self.in_edge_list)

  # it returns the final cluster node connectivity (tree shape) -- out edges
  def _Get_Outdegree(self):
    return len(self.out_edge_list)
  
  # it adds one out edge information to both the original connectivity (clique) and the final connectivity (tree shape)
  def _AddOutEdge(self, dest_clust_idx):
    if dest_clust_idx not in self.out_edge_list:
      self.out_edge_list.append(dest_clust_idx)
    
  # it adds one in edge information to both the original connectivity (clique) and the final connectivity (tree shape)
  def _AddInEdge(self, src_clust_idx):
    if src_clust_idx not in self.in_edge_list:
      self.in_edge_list.append(src_clust_idx)
    
  # here the final connectivity is changed (not the original clique based connectivity) -- out edge remove
  def _RemoveOutEdge(self, dest_clust_idx):
    if dest_clust_idx in self.out_edge_list:
      self.out_edge_list.remove(dest_clust_idx)    
    
  # here the final connectivity is changed (not the original clique based connectivity) -- in edge remove
  def _RemoveInEdge(self, dest_clust_idx):
    if dest_clust_idx in self.in_edge_list:
      self.in_edge_list.remove(dest_clust_idx)    
    
  def _PrintClusterInfo(self, clust_index):
    print '====>>>>  Printing information for cluster index: ', clust_index
    print 'species list: ', self.Species_List
    print 'out edge list: ', self.out_edge_list
    print 'in edge list: ', self.in_edge_list
