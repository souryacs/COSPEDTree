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
''' this function is the core module for cycle detection --- used to simmplify the code 
arguments: nodeA --- whose neighborhood (x) needs to be reviewed
	   nodeB --- relationship between this node and neighborhood (x) of nodeA needs to be examined
	   nodeA_neighb: specifies the neighborhood (x) of nodeA
	   target_edge_type: species the edge type between nodeB and x that needs to be considered for establishment
'''
def ModuleCycleDetect(cpy_Reach_Grph, nodeA, nodeB, nodeA_neighb, target_edge_type, \
		      curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST): 
  # PRESERVE_NO_EDGE_TYPE variable prevents over-writing previous NO_EDGE connection to some other edge types
  # basically, if a connection tends to overwrite the previous NO_EDGE connection 
  # then the scoring is compared (cost before and after the operation)
  
  if (len(nodeA_neighb) > 0):
    for l in nodeA_neighb:
      # case 1 -------- C->B connection
      if (target_edge_type == DIRECTED_IN_EDGE):
	# we check if previously B->C connection exists - in that case, a cycle is reported
	key2 = (nodeB, l)
	if (cpy_Reach_Grph[key2] == 1):
	  return 1
	#--------------------------------
	# check if there exists previous NO_EDGE connection between l and nodeB
	# for strict preserve cases, NO_EDGE cannot be replaced
	# otherwise the replacement is done with cost checking
	if (PRESERVE_NO_EDGE_TYPE == 1) and (l in PairLeaf_Node_Dict[nodeB]._GetFinalNoEdgeList()): 
	  return 1
	#if (PRESERVE_NO_EDGE_TYPE == 0) and (COST_UPDATE_LATEST == 1):
	if (COST_UPDATE_LATEST == 1):
	  key_temp1 = (nodeB, l)
	  key_temp2 = (l, nodeB)
	  if key_temp1 in Pair_Reln_Dict:
	    if (curr_conn_pr_val <= (Pair_Reln_Dict[key_temp1]._GetConnPrVal(NO_EDGE)\
				      - Pair_Reln_Dict[key_temp1]._GetConnPrVal(DIRECTED_IN_EDGE))):
	      return 1
	  if key_temp2 in Pair_Reln_Dict:
	    if (curr_conn_pr_val <= (Pair_Reln_Dict[key_temp2]._GetConnPrVal(NO_EDGE)\
				      - Pair_Reln_Dict[key_temp2]._GetConnPrVal(DIRECTED_OUT_EDGE))):
	      return 1
	
	#--------------------------------
	key1 = (l, nodeB)
	cpy_Reach_Grph[key1] = 1
      # case 2 -------- B->C connection
      if (target_edge_type == DIRECTED_OUT_EDGE):
	# we check if previously C->B connection exists - in that case, a cycle is reported
	key2 = (l, nodeB)
	if (cpy_Reach_Grph[key2] == 1):
	  return 1
	#--------------------------------
	# check if there exists previous NO_EDGE connection between l and nodeB
	# for strict preserve cases, NO_EDGE cannot be replaced
	# otherwise the replacement is done with cost checking
	if (PRESERVE_NO_EDGE_TYPE == 1) and (l in PairLeaf_Node_Dict[nodeB]._GetFinalNoEdgeList()): 
	  return 1
	#if (PRESERVE_NO_EDGE_TYPE == 0) and (COST_UPDATE_LATEST == 1):
	if (COST_UPDATE_LATEST == 1):	
	  key_temp1 = (nodeB, l)
	  key_temp2 = (l, nodeB)
	  if key_temp1 in Pair_Reln_Dict:
	    if (curr_conn_pr_val <= (Pair_Reln_Dict[key_temp1]._GetConnPrVal(NO_EDGE)\
				      - Pair_Reln_Dict[key_temp1]._GetConnPrVal(DIRECTED_OUT_EDGE))):
	      return 1
	  if key_temp2 in Pair_Reln_Dict:
	    if (curr_conn_pr_val <= (Pair_Reln_Dict[key_temp2]._GetConnPrVal(NO_EDGE)\
				      - Pair_Reln_Dict[key_temp2]._GetConnPrVal(DIRECTED_IN_EDGE))):
	      return 1
	
	#--------------------------------
	key1 = (nodeB, l)
	cpy_Reach_Grph[key1] = 1
      # case 3 -------- B=C connection
      if (target_edge_type == BI_DIRECTED_EDGE):
	# we check whether previously any one of the connection B->C or C->B exists or not
	# in that case, a cycle is reported
	key1 = (l, nodeB)
	key2 = (nodeB, l)
	# update - sourya
	# if there is a previous connection of B->C or C->B then this is a cycle
	# but if a connection B=C is already existing then there is no problem
	if ((cpy_Reach_Grph[key1] == 1) and (cpy_Reach_Grph[key2] != 1))\
	    or ((cpy_Reach_Grph[key1] != 1) and (cpy_Reach_Grph[key2] == 1)):
	  return 1
	#--------------------------------
	# check if there exists previous NO_EDGE connection between l and nodeB
	# for strict preserve cases, NO_EDGE cannot be replaced
	# otherwise the replacement is done with cost checking	
	if (PRESERVE_NO_EDGE_TYPE == 1) and (l in PairLeaf_Node_Dict[nodeB]._GetFinalNoEdgeList()): 
	  return 1
	#if (PRESERVE_NO_EDGE_TYPE == 0) and (COST_UPDATE_LATEST == 1):
	if (COST_UPDATE_LATEST == 1):
	  key_temp1 = (nodeB, l)
	  key_temp2 = (l, nodeB)
	  if key_temp1 in Pair_Reln_Dict:
	    if (curr_conn_pr_val <= (Pair_Reln_Dict[key_temp1]._GetConnPrVal(NO_EDGE)\
				      - Pair_Reln_Dict[key_temp1]._GetConnPrVal(BI_DIRECTED_EDGE))):
	      return 1
	  if key_temp2 in Pair_Reln_Dict:
	    if (curr_conn_pr_val <= (Pair_Reln_Dict[key_temp2]._GetConnPrVal(NO_EDGE)\
				      - Pair_Reln_Dict[key_temp2]._GetConnPrVal(BI_DIRECTED_EDGE))):
	      return 1
	
	#--------------------------------
	cpy_Reach_Grph[key1] = 1  
	cpy_Reach_Grph[key2] = 1  
  
  ''' otherwise return the absence of any cycle '''
  return 0

##-----------------------------------------------------
''' this function checks the possible existence of a cycle based on input edge type between 2 specied nodes
we have to update the copy of reachability graph, and then check for cycle in all possible directions '''
def CyclePossible(nodeA, nodeB, cpy_Reach_Grph, edge_type, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST):
  result = 0
    
  # at first mark the current edge in the graph 
  if (edge_type == DIRECTED_OUT_EDGE):
    key = (nodeA, nodeB)
    otherkey = (nodeB, nodeA)
    # if the other end is already filled up then we return a cycle existence
    if (cpy_Reach_Grph[otherkey] == 1):
      return 1
    cpy_Reach_Grph[key] = 1
  elif (edge_type == DIRECTED_IN_EDGE):
    key = (nodeB, nodeA)
    otherkey = (nodeA, nodeB)
    # if the other end is already filled up then we return a cycle existence
    if (cpy_Reach_Grph[otherkey] == 1):
      return 1    
    cpy_Reach_Grph[key] = 1
  elif (edge_type == BI_DIRECTED_EDGE):
    key1 = (nodeA, nodeB)
    key2 = (nodeB, nodeA)
    # if any of the ends is already filled up then we return a cycle existence
    if ((cpy_Reach_Grph[key1] == 1) and (cpy_Reach_Grph[key2] != 1))\
	or ((cpy_Reach_Grph[key1] != 1) and (cpy_Reach_Grph[key2] == 1)):
      return 1
    cpy_Reach_Grph[key1] = 1
    cpy_Reach_Grph[key2] = 1
  else:		# NO_EDGE
    # add - sourya
    key1 = (nodeA, nodeB)
    key2 = (nodeB, nodeA)
    if ((cpy_Reach_Grph[key1] == 1) or (cpy_Reach_Grph[key2] == 1)):
      return 1
    # end add - sourya
    
  # determine the current connection value
  if (COST_UPDATE_LATEST == 1):
    key_temp1 = (nodeA, nodeB)
    key_temp2 = (nodeB, nodeA)
    if key_temp1 in Pair_Reln_Dict:
      # here the connection value will be according to the edge type
      curr_conn_pr_val = Pair_Reln_Dict[key_temp1]._GetConnPrVal(edge_type)
    elif key_temp2 in Pair_Reln_Dict:
      # here the connection value requires adjustment of edge type
      if (edge_type == NO_EDGE) or (edge_type == BI_DIRECTED_EDGE):
	curr_conn_pr_val = Pair_Reln_Dict[key_temp2]._GetConnPrVal(edge_type)
      elif (edge_type == DIRECTED_IN_EDGE):
	curr_conn_pr_val = Pair_Reln_Dict[key_temp2]._GetConnPrVal(DIRECTED_OUT_EDGE)
      else:
	curr_conn_pr_val = Pair_Reln_Dict[key_temp2]._GetConnPrVal(DIRECTED_IN_EDGE)
    else:
      curr_conn_pr_val = 0
  else:
    curr_conn_pr_val = 0
    
  ''' now check the neighborhood of the input nodes and adjust reachability '''
  ''' case A - A->B connection '''
  if (edge_type == DIRECTED_OUT_EDGE):
    ''' check neighborhood of nodeA (in edge or bi directed edge) '''
    ''' check the neighbors of nodeA that are connected via edge C->A or C=A
    check the existence of connection B->C -- if it exists then there will be a cycle ''' 
    nodeA_neighb = []
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalInEdgeList())
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalEqEdgeList())
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeA, nodeB, nodeA_neighb, DIRECTED_IN_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result
	  
    ''' check neighborhood of nodeB (out edge or bi directed edge) '''
    ''' check the neighbors of node B that are connected via edge B->C or B=C
    check the existence of connection C->A -- if it exists then there will be a cycle '''    
    nodeB_neighb = []
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalOutEdgeList())
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalEqEdgeList())
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeB, nodeA, nodeB_neighb, DIRECTED_OUT_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result
      
    # add - sourya
    ''' check neighborhood of nodeA (NO_EDGE) --- that is, C><A
    so after A->B, it should be C><B
    but if there exists B->C or B=C, or C->B, then current connection is not allowed '''
    if 0:
      nodeA_neighb = []
      nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalNoEdgeList())
      nodeB_neighb = []
      nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalOutEdgeList())
      nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalEqEdgeList())
      nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalInEdgeList())
      for l in nodeA_neighb:
	if l in nodeB_neighb:
	  return 1
    # end add - sourya
      
  ''' case B - B->A connection '''
  if (edge_type == DIRECTED_IN_EDGE):
    ''' check neighborhood of nodeA (out edge or bi directed edge) '''    
    ''' check the neighbors of node A that are connected via edge A->C or A=C 
    check the existence of connection C->B -- if it exists then there will be a cycle  '''
    nodeA_neighb = []
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalOutEdgeList())
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalEqEdgeList())    
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeA, nodeB, nodeA_neighb, DIRECTED_OUT_EDGE, \
			      curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result    
	  
    ''' check neighborhood of nodeB (in edge or bi directed edge) '''
    ''' check the neighbors of node B that are connected via edge C->B or C=B
    check the existence of connection A->C -- if it exists then there will be a cycle '''
    nodeB_neighb = []
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalInEdgeList())
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalEqEdgeList())    
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeB, nodeA, nodeB_neighb, DIRECTED_IN_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result   
      
    # add - sourya
    ''' check neighborhood of nodeB (NO_EDGE) --- that is, C><B
    so after B->A, it should be C><A
    but if there exists A->C or A=C or C->A, then current connection is not allowed '''
    if 0:
      nodeB_neighb = []
      nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalNoEdgeList())
      nodeA_neighb = []
      nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalOutEdgeList())
      nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalEqEdgeList())
      nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalInEdgeList())
      for l in nodeB_neighb:
	if l in nodeA_neighb:
	  return 1
    # end add - sourya    
      
  ''' case C - A=B connection '''
  if (edge_type == BI_DIRECTED_EDGE):
    ''' check neighborhood of nodeA '''    
    ''' check the neighbors of node A that are connected via edge A->C
    check the existence of connection C->B -- if it exists then there will be a cycle '''  
    nodeA_neighb = []
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalOutEdgeList())
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeA, nodeB, nodeA_neighb, DIRECTED_OUT_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result    
    ''' check the neighbors of node A that are connected via edge C->A 
    check the existence of connection B->C -- if it exists then there will be a cycle '''
    nodeA_neighb = []
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalInEdgeList())
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeA, nodeB, nodeA_neighb, DIRECTED_IN_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result    
    ''' check the neighbors of node A that are connected via edge A=C 
    the target connection is B=C (for satisfying this connection)
    however, if the B and C nodes are already connected via B->C or C->B connection
    then this target connection cannot be established '''    
    nodeA_neighb = []
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalEqEdgeList())    
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeA, nodeB, nodeA_neighb, BI_DIRECTED_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result
    # add - sourya
    ''' check the neighbors of node A that are connected via edge A><C 
    so, for A=B connection, B><C should be ensured
    however, if there is a connection between B and C then it can't be done '''
    if 0:
      nodeA_neighb = []
      nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalNoEdgeList())    
      nodeB_neighb = []
      nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalOutEdgeList())
      nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalInEdgeList())
      nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalEqEdgeList())    
      for l in nodeA_neighb:
	if l in nodeB_neighb:
	  return 1
    # end add - sourya
    
    ''' check neighborhood of nodeB '''    
    ''' check the neighbors of node B that are connected via edge B->C
    check the existence of connection C->A -- if it exists then there will be a cycle '''  
    nodeB_neighb = []
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalOutEdgeList())
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeB, nodeA, nodeB_neighb, DIRECTED_OUT_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result
    ''' check the neighbors of node B that are connected via edge C->B
    check the existence of connection A->C -- if it exists then there will be a cycle '''  
    nodeB_neighb = []
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalInEdgeList())
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeB, nodeA, nodeB_neighb, DIRECTED_IN_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)
    if (result == 1):
      return result
    ''' check the neighbors of node B that are connected via edge B=C 
    the target connection is A=C (for satisfying this connection)
    however, if the A and C nodes are already connected via A->C or C->A connection
    then this target connection cannot be established '''    
    nodeB_neighb = []
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalEqEdgeList())    
    result = ModuleCycleDetect(cpy_Reach_Grph, nodeB, nodeA, nodeB_neighb, BI_DIRECTED_EDGE, \
				curr_conn_pr_val, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST)    
    if (result == 1):
      return result
    # add - sourya
    ''' check the neighbors of node B that are connected via edge B><C 
    so, for A=B connection, A><C should be ensured
    however, if there is a connection between A and C then it can't be done '''
    if 0:
      nodeB_neighb = []
      nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalNoEdgeList())    
      nodeA_neighb = []
      nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalOutEdgeList())
      nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalInEdgeList())
      nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalEqEdgeList())    
      for l in nodeB_neighb:
	if l in nodeA_neighb:
	  return 1
    # end add - sourya
        
  ''' case D - A><B connection '''
  if (edge_type == NO_EDGE):
    # add - sourya
    ''' check the neighbors of node A such that A->C or A=C
    for A><B, B><C should be ensured
    but if there is a connection between B and C then it cannot be done '''
    nodeA_neighb = []
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalOutEdgeList())    
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalEqEdgeList())    
    nodeB_neighb = []
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalOutEdgeList())
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalInEdgeList())
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalEqEdgeList())    
    for l in nodeA_neighb:
      if l in nodeB_neighb:
	return 1

    ''' check the neighbors of node B such that B->C or B=C
    for A><B, A><C should be ensured
    but if there is a connection between A and C then it cannot be done '''
    nodeB_neighb = []
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalOutEdgeList())    
    nodeB_neighb.extend(PairLeaf_Node_Dict[nodeB]._GetFinalEqEdgeList())    
    nodeA_neighb = []
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalOutEdgeList())
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalInEdgeList())
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalEqEdgeList())    
    for l in nodeB_neighb:
      if l in nodeA_neighb:
	return 1
    # end add - sourya
            
  ''' otherwise return the absence of any cycle '''
  return 0
  
