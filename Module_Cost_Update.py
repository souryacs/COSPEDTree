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
''' this function updates the list containing the score of node pairs, by an amount delta_score '''
def UpdateEdgeCostInMemList(nodeA, nodeB, delta_score, connect_edge_type, INIT_COST_PRIOR_PROCESS):
  if (delta_score != 0):
    # form the list key to search the content of the Cost_List_Node_Pair
    key = (nodeA, nodeB)
    nodeA_idx = Complete_Input_Species_List.index(nodeA)
    nodeB_idx = Complete_Input_Species_List.index(nodeB)
    edge_cost_orig = Pair_Reln_Dict[key]._GetEdgeCost_ConnReln(connect_edge_type)
    orig_list_key = [nodeA_idx, nodeB_idx, connect_edge_type, edge_cost_orig]
    
    # this condition is to prevent key error 
    # some keys may not be found due to late addition of unnecessary edges (connections)
    if orig_list_key in Cost_List_Node_Pair:
      # now find the index of this entry in the final list
      orig_search_idx_list = Cost_List_Node_Pair.index(orig_list_key)
      # at first update the score in the structure Pair_Reln_Dict
      Pair_Reln_Dict[key]._IncrEdgeCost_ConnReln(connect_edge_type, delta_score)
      # prepare the list key to have the target score
      target_score = edge_cost_orig + delta_score
      if (INIT_COST_PRIOR_PROCESS == 1):
	# just update the score metric with the new target score
	Cost_List_Node_Pair[orig_search_idx_list][3] = target_score
      else:
	# otherwise the function is used to update the list content and sort the positions
	new_list_key = [nodeA_idx, nodeB_idx, connect_edge_type, target_score]
	if (delta_score > 0):
	  search_idx_list = orig_search_idx_list - 1
	  # if the cost increment is positive, then we have to move towards the front of the list
	  while (search_idx_list >= 0):
	    if (Cost_List_Node_Pair[search_idx_list][3] < target_score):
	      search_idx_list = search_idx_list - 1
	    elif (Cost_List_Node_Pair[search_idx_list][3] == target_score):
	      if ((Cost_List_Node_Pair[search_idx_list][2] == NO_EDGE) and (connect_edge_type != NO_EDGE)):
		search_idx_list = search_idx_list - 1
	      elif (Pair_Reln_Dict[(Complete_Input_Species_List[Cost_List_Node_Pair[search_idx_list][0]], Complete_Input_Species_List[Cost_List_Node_Pair[search_idx_list][1]])]._GetConnPrVal(Cost_List_Node_Pair[search_idx_list][2])\
		    < Pair_Reln_Dict[(nodeA, nodeB)]._GetConnPrVal(connect_edge_type)):	
		search_idx_list = search_idx_list - 1
	      else:
		break
	    else:
	      break
	  # insert the new key in the list
	  Cost_List_Node_Pair.insert((search_idx_list+1), new_list_key)
	else:
	  search_idx_list = orig_search_idx_list + 1
	  # if the cost increment is negative, then we have to move towards the rear of the list
	  while (search_idx_list < len(Cost_List_Node_Pair)):
	    if (Cost_List_Node_Pair[search_idx_list][3] > target_score):
	      search_idx_list = search_idx_list + 1
	    elif (Cost_List_Node_Pair[search_idx_list][3] == target_score):
	      if ((Cost_List_Node_Pair[search_idx_list][2] != NO_EDGE) and (connect_edge_type == NO_EDGE)):
		search_idx_list = search_idx_list + 1
	      elif (Pair_Reln_Dict[(Complete_Input_Species_List[Cost_List_Node_Pair[search_idx_list][0]], Complete_Input_Species_List[Cost_List_Node_Pair[search_idx_list][1]])]._GetConnPrVal(Cost_List_Node_Pair[search_idx_list][2])\
		    > Pair_Reln_Dict[(nodeA, nodeB)]._GetConnPrVal(connect_edge_type)):
		search_idx_list = search_idx_list + 1
	      else:
		break
	    else:
	      break
	  # insert the new key in the list
	  Cost_List_Node_Pair.insert(search_idx_list, new_list_key)

	# now remove the element of the Cost_List_Node_Pair containing the old value
	Cost_List_Node_Pair.remove(orig_list_key)
	#print 'in function UpdateEdgeCostInMemList --- old cost: ', edge_cost_orig, ' shifted to : ', target_score, 'old idx: ', orig_search_idx_list, 'new idx: ', final_search_idx_list
    
##-----------------------------------------------------
''' this function modules the UpdateEdgeCost_Conn_Reln function
arguments: nodeA --- whose neighborhood (x) needs to be reviewed
	   nodeB --- relationship between this node and neighborhood (x) of nodeA needs to be examined
	   neighborhood_edge_type - type of neighborhood of nodeA that is to be examined
	   target_edge_type: species the cost of this type of edge between nodeB and x that needs to be updated
	   node_A_B_edge_type: edge type between nodeA and nodeB
'''
def ModuleUpdCost(nodeA, nodeB, neighborhood_edge_type, target_edge_type, \
		  INIT_COST_PRIOR_PROCESS, node_A_B_edge_type):    
  # here an edge type between nodeA and nodeB is to be evaluated
  # define the neighborhood of node A
  nodeA_neighb = []
  if (neighborhood_edge_type == DIRECTED_IN_EDGE):
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetNonProcessedInEdgeList())
  elif (neighborhood_edge_type == BI_DIRECTED_EDGE):
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetNonProcessedEqEdgeList())
  elif (neighborhood_edge_type == DIRECTED_OUT_EDGE):
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetNonProcessedOutEdgeList())
  else:
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetNonProcessedNoEdgeList())

  if nodeB in nodeA_neighb:
    nodeA_neighb.remove(nodeB)	# dont consider nodeB
    
  if (len(nodeA_neighb) > 0):
    for l in nodeA_neighb:
      # following process calculates the score of the original neighborhood connection
      if (INIT_COST_PRIOR_PROCESS == 1):
	# here we accumulate the cost of the edge from nodeA to l
	key1 = (nodeA, l)
	key2 = (l, nodeA)
	if (key1 in Pair_Reln_Dict):
	  original_neigb_score = Pair_Reln_Dict[key1]._GetConnPrVal(neighborhood_edge_type)
	else:
	  if (neighborhood_edge_type == NO_EDGE) or (neighborhood_edge_type == BI_DIRECTED_EDGE):
	    original_neigb_score = Pair_Reln_Dict[key2]._GetConnPrVal(neighborhood_edge_type)
	  elif (neighborhood_edge_type == DIRECTED_IN_EDGE):
	    original_neigb_score = Pair_Reln_Dict[key2]._GetConnPrVal(DIRECTED_OUT_EDGE)
	  elif (neighborhood_edge_type == DIRECTED_OUT_EDGE):
	    original_neigb_score = Pair_Reln_Dict[key2]._GetConnPrVal(DIRECTED_IN_EDGE)
	    
      # now we calculate the score of the derived edge connection
      # (in terms of deviation from the best possible edge between these 2 nodes) 
      key1 = (nodeB, l)
      key2 = (l, nodeB)
      if (key1 not in Pair_Reln_Dict) and (key2 not in Pair_Reln_Dict):
	if (target_edge_type == NO_EDGE):
	  delta_score = ORIG_NO_EDGE_REMAIN_NO_EDGE
	else:
	  delta_score = ORIG_DIFF_SRC_TREE_CONNECT_SCORE
      else:
	if key1 in Pair_Reln_Dict:
	  delta_score = Pair_Reln_Dict[key1]._GetConnPrVal(target_edge_type)
	  if (target_edge_type != NO_EDGE):
	    # check whether originally between these 2 nodes, NO_EDGE connection was predominant 
	    if (Pair_Reln_Dict[key1]._GetConnPrVal(NO_EDGE) > 0):
	      delta_score = delta_score + ORIG_NO_EDGE_BECOME_CONNECTED	    	    
	else:
	  # at first complement the target edge type
	  if (target_edge_type == DIRECTED_IN_EDGE):
	    delta_score = Pair_Reln_Dict[key2]._GetConnPrVal(DIRECTED_OUT_EDGE)
	  elif (target_edge_type == DIRECTED_OUT_EDGE):
	    delta_score = Pair_Reln_Dict[key2]._GetConnPrVal(DIRECTED_IN_EDGE)
	  else:
	    delta_score = Pair_Reln_Dict[key2]._GetConnPrVal(target_edge_type)
	  if (target_edge_type != NO_EDGE):
	    # check whether originally between these 2 nodes, NO_EDGE connection was predominant 
	    if (Pair_Reln_Dict[key2]._GetConnPrVal(NO_EDGE) > 0):
	      delta_score = delta_score + ORIG_NO_EDGE_BECOME_CONNECTED
	      
      # now we update the score of the edge
      if (INIT_COST_PRIOR_PROCESS == 1):
	# here we update the edge cost between nodeA and nodeB
	# node_A_B_edge_type is the defined edge type between these two nodes, cost of which needs to be updated
	kt1 = (nodeA, nodeB)
	kt2 = (nodeB, nodeA)
	if kt1 in Pair_Reln_Dict:
	  UpdateEdgeCostInMemList(nodeA, nodeB, (original_neigb_score + delta_score), \
				  node_A_B_edge_type, INIT_COST_PRIOR_PROCESS)
	else:
	  if (node_A_B_edge_type == BI_DIRECTED_EDGE) or (node_A_B_edge_type == NO_EDGE):
	    UpdateEdgeCostInMemList(nodeB, nodeA, (original_neigb_score + delta_score), \
				    node_A_B_edge_type, INIT_COST_PRIOR_PROCESS)
	  elif (node_A_B_edge_type == DIRECTED_IN_EDGE):
	    UpdateEdgeCostInMemList(nodeB, nodeA, (original_neigb_score + delta_score), \
				    DIRECTED_OUT_EDGE, INIT_COST_PRIOR_PROCESS)
	  elif (node_A_B_edge_type == DIRECTED_OUT_EDGE):
	    UpdateEdgeCostInMemList(nodeB, nodeA, (original_neigb_score + delta_score), \
				    DIRECTED_IN_EDGE, INIT_COST_PRIOR_PROCESS)	  
      else:
	# here we update the score of edge between nodeA and l 
	# (where l belongs to the neighborhood of nodeA)
	# now call the function to update the delta_score of list element
	kt1 = (nodeA, l)
	kt2 = (l, nodeA)
	if kt1 in Pair_Reln_Dict:
	  UpdateEdgeCostInMemList(nodeA, l, delta_score, neighborhood_edge_type, INIT_COST_PRIOR_PROCESS)
	elif kt2 in Pair_Reln_Dict:
	  # at first complement the neighborhood_edge_type
	  if (neighborhood_edge_type == DIRECTED_IN_EDGE):
	    UpdateEdgeCostInMemList(l, nodeA, delta_score, DIRECTED_OUT_EDGE, INIT_COST_PRIOR_PROCESS)  
	  elif (neighborhood_edge_type == DIRECTED_OUT_EDGE):
	    UpdateEdgeCostInMemList(l, nodeA, delta_score, DIRECTED_IN_EDGE, INIT_COST_PRIOR_PROCESS)	  
	  else:
	    UpdateEdgeCostInMemList(l, nodeA, delta_score, neighborhood_edge_type, INIT_COST_PRIOR_PROCESS)

##-----------------------------------------------------
''' this function is called to update the edge score between a set of taxa
nodeA and nodeB are two input nodes, which are already connected in the final tree
i.e. their final edge type is decided

here the NON-PROCESSED neighborhood of nodeA and nodeB are checked

1)(say x belongs to non processed neighborhood of nodeB, with ? as the edge type) --- 
  check the possible connection of x to nodeA
  the score of this connection from x to nodeA is the priority associated with corresponding edge type
  this score is added with the score of edge type ? between nodeB to x
2)(say y belongs to non processed neighborhood of nodeA, with ? as the edge type) --- 
  check the possible connection of y to nodeB
  the score of this connection from y to nodeB is the priority associated with corresponding edge type
  this score is added with the score of edge type ? between nodeA to y '''
  
def UpdateEdgeCost_Conn_Reln(nodeA, nodeB, edge_type, COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS):
  
  # case 1 - A->B connection 
  if (edge_type == DIRECTED_OUT_EDGE):        
    ##-----------------------------------------
    ## check non processed neighborhood of nodeA
    ##-----------------------------------------
    # check the non processed neighbors of nodeA that can be connected in future via edge C->A
    # check the possible connection C->B 
    ModuleUpdCost(nodeA, nodeB, DIRECTED_IN_EDGE, DIRECTED_IN_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)    
    # check the non processed neighbors of nodeA that can be connected in future via edge C=A
    # check the possible connection C->B
    ModuleUpdCost(nodeA, nodeB, BI_DIRECTED_EDGE, DIRECTED_IN_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # add - sourya
    # check the non processed neighbors of nodeA that can be connected in future via edge C><A
    # check the possible connection C><B
    ModuleUpdCost(nodeA, nodeB, NO_EDGE, NO_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # end add - sourya
    ##-----------------------------------------
    ## check non processed neighborhood of nodeB
    ##-----------------------------------------
    # check the non processed neighbors of node B that can be connected in future via edge B->C
    # check the possible connection A->C
    ModuleUpdCost(nodeB, nodeA, DIRECTED_OUT_EDGE, DIRECTED_OUT_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)    
    # check the non processed neighbors of node B that can be connected in future via edge B=C
    # check the possible connection A->C 
    ModuleUpdCost(nodeB, nodeA, BI_DIRECTED_EDGE, DIRECTED_OUT_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)    
      
  # case 2 - A<-B connection 
  if (edge_type == DIRECTED_IN_EDGE):    
    ##-----------------------------------------
    ## check non processed neighborhood of nodeA 
    ##-----------------------------------------
    # check the non processed neighbors of node A that can be connected in future via edge A->C
    # check the possible connection B->C
    ModuleUpdCost(nodeA, nodeB, DIRECTED_OUT_EDGE, DIRECTED_OUT_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)    
    # check the non processed neighbors of node A that can be connected in future via edge A=C
    # check the possible connection B->C 
    ModuleUpdCost(nodeA, nodeB, BI_DIRECTED_EDGE, DIRECTED_OUT_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    ##-----------------------------------------
    ## check non processed neighborhood of nodeB
    ##-----------------------------------------
    # check the non processed neighbors of node B that can be connected in future via edge C->B
    # establish the possible connection C->A
    ModuleUpdCost(nodeB, nodeA, DIRECTED_IN_EDGE, DIRECTED_IN_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # check the neighbors of node B that can be connected in future via edge C=B
    # establish the connection C->A
    ModuleUpdCost(nodeB, nodeA, BI_DIRECTED_EDGE, DIRECTED_IN_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)    		    
    # add - sourya
    # check the non processed neighbors of nodeB that can be connected in future via edge C><B
    # check the possible connection C><A 
    ModuleUpdCost(nodeB, nodeA, NO_EDGE, NO_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # end add - sourya 
    
  # case 3 - A=B connection 
  if (edge_type == BI_DIRECTED_EDGE):    
    ##-----------------------------------------
    ## check non processed neighborhood of nodeA
    ##-----------------------------------------
    # check the non processed neighbors of node A that can be connected in future via edge A->C
    # check the possible connection B->C
    ModuleUpdCost(nodeA, nodeB, DIRECTED_OUT_EDGE, DIRECTED_OUT_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # check the non processed neighbors of node A that can be connected in future via edge C->A 
    # establish the connection C->B
    ModuleUpdCost(nodeA, nodeB, DIRECTED_IN_EDGE, DIRECTED_IN_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # check the non processed neighbors of node A that can be connected in future via edge A=C
    # check the possible connection B=C
    ModuleUpdCost(nodeA, nodeB, BI_DIRECTED_EDGE, BI_DIRECTED_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # add - sourya
    # check the non processed neighbors of node A that can be connected in future via edge A><C
    # check the possible connection B><C
    ModuleUpdCost(nodeA, nodeB, NO_EDGE, NO_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # end add - sourya
    ##-----------------------------------------
    ## check non processed neighborhood of nodeB 
    ##-----------------------------------------
    # check the non processed neighbors of node B that can be connected in future via edge B->C
    # check the connection A->C
    ModuleUpdCost(nodeB, nodeA, DIRECTED_OUT_EDGE, DIRECTED_OUT_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # check the non processed neighbors of node B that can be connected in future via edge C->B 
    # establish the possible connection C->A
    ModuleUpdCost(nodeB, nodeA, DIRECTED_IN_EDGE, DIRECTED_IN_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)    
    # check the non processed neighbors of node B that can be connected in future via edge B=C
    # check the possible connection A=C
    ModuleUpdCost(nodeB, nodeA, BI_DIRECTED_EDGE, BI_DIRECTED_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)    
    # add - sourya
    # check the non processed neighbors of nodeB that can be connected in future via edge B><C
    # check the possible connection A><C  
    ModuleUpdCost(nodeB, nodeA, NO_EDGE, NO_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # end add - sourya
		      
  # case 4 - A><B connection (no connection)
  if (edge_type == NO_EDGE):    
    ##-----------------------------------------
    ## check non processed neighborhood of nodeA 
    ##-----------------------------------------
    # check the non processed neighbors of node A that can be connected in future via edge A->C
    # check the possible connection B><C
    ModuleUpdCost(nodeA, nodeB, DIRECTED_OUT_EDGE, NO_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # check the non processed neighbors of node A that can be connected in future via edge A=C
    # check the possible connection B><C      
    ModuleUpdCost(nodeA, nodeB, BI_DIRECTED_EDGE, NO_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    ##-----------------------------------------
    ## check non processed neighborhood of nodeB 
    ##-----------------------------------------
    # check the non processed neighbors of node B that can be connected in future via edge B->C
    # check the possible connection A><C
    ModuleUpdCost(nodeB, nodeA, DIRECTED_OUT_EDGE, NO_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)
    # check the non processed neighbors of node B that can be connected in future via edge B=C
    # check the possible connection A><C
    ModuleUpdCost(nodeB, nodeA, BI_DIRECTED_EDGE, NO_EDGE, INIT_COST_PRIOR_PROCESS, edge_type)    
