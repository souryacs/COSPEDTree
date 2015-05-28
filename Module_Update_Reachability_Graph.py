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
''' this function finalizes the edge connectivity between 2 nodes with a given input edge type 
parameter derived_edge signifies that for a certain edge type, 
the derived edges associated with the neighborhood is under concern '''
def FinalizeEdgeConnect(Reachability_Graph_Mat, nodeA, nodeB, edge_type, \
			COST_UPDATE_LATEST, derived_edge, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT):
  # if the two nodes are not already connected (originally) then connect with the obtained edge type
  global nodes_connected
  nodes_connected = nodes_connected + 1
  key = (nodeA, nodeB)
  print 'conn idx: ', nodes_connected, 'edge connected === ', nodeA, ' and ', nodeB, 'type: ', edge_type
  nodeA_idx = Complete_Input_Species_List.index(nodeA)
  nodeB_idx = Complete_Input_Species_List.index(nodeB)
  
  if key not in Pair_Reln_Dict:
    #print '===>>>  key : ', key, 'was not in Pair_Reln_Dict -- added for edge type : ', edge_type, 'idx: ', Complete_Input_Species_List.index(nodeA), Complete_Input_Species_List.index(nodeB)
    Pair_Reln_Dict.setdefault(key, Connect_Reln_NodePair(edge_type))
    Pair_Reln_Dict[key]._AddEdgeCount(edge_type)
    Pair_Reln_Dict[key]._SetConnPrVal(False, FRACTION_EDGE_WEIGHT)
  else:
    Pair_Reln_Dict[key]._UpdateFinalEdgeInfo(edge_type)
    # now remove the tuple (nodeA, nodeB) information from the Cost_List_Node_Pair, 
    # for all the individual edge types
    # caution - for NO_EDGE edge type, it may happen that there is only this entry for these node pairs, 
    # within this memory
    # so checking should be done before delete
    for edge_idx in range(4):
      list_key = [nodeA_idx, nodeB_idx, edge_idx, Pair_Reln_Dict[key]._GetEdgeCost_ConnReln(edge_idx)]
      #print 'list key: ', list_key
      # remove this edge information from Cost_List_Node_Pair, if exists
      # to save the subsequent processing time
      if list_key in Cost_List_Node_Pair:
	Cost_List_Node_Pair.remove(list_key)
      # remove this edge information from single_edge_occurrence_list, if exists
      # to save the subsequent processing time
      if list_key in single_edge_occurrence_list:
	single_edge_occurrence_list.remove(list_key)
      
  # now append the node final edge information to individual nodes' final connected list
  PairLeaf_Node_Dict[nodeA]._AddFinalEdge(edge_type, nodeB)
  if (edge_type == BI_DIRECTED_EDGE) or (edge_type == NO_EDGE):
    PairLeaf_Node_Dict[nodeB]._AddFinalEdge(edge_type, nodeA)
  elif (edge_type == DIRECTED_IN_EDGE):
    PairLeaf_Node_Dict[nodeB]._AddFinalEdge(DIRECTED_OUT_EDGE, nodeA)
  elif (edge_type == DIRECTED_OUT_EDGE):
    PairLeaf_Node_Dict[nodeB]._AddFinalEdge(DIRECTED_IN_EDGE, nodeA)

  # for the updated cost settings, this list maintains the edges connected in this iteration
  if (COST_UPDATE_LATEST == 1) and (INIT_COST_PRIOR_PROCESS == 0):
    # the list entry contains two nodes and their connecting edge information
    # basically the purpose of this list is to store the edge information which are considered 
    # for this current iteration of Reachability Graph Update
    # if one edge is already considered then we dont include this edge again, and subsequently do not consider
    sublist = [nodeA_idx, nodeB_idx, edge_type]
    
    if (edge_type == DIRECTED_OUT_EDGE):		# case 1 - edge_type is DIRECTED_OUT_EDGE
      sublist1 = [nodeB_idx, nodeA_idx, DIRECTED_IN_EDGE]
    elif (edge_type == DIRECTED_IN_EDGE):	# case 2 - edge_type is DIRECTED_IN_EDGE
      sublist1 = [nodeB_idx, nodeA_idx, DIRECTED_OUT_EDGE]
    else:	# case 3 - edge_type is BI_DIRECTED_EDGE or NO_EDGE
      sublist1 = [nodeB_idx, nodeA_idx, edge_type]
      
    # check whether this edge is already processed or in the processing list
    if (sublist not in EDGE_PROCESSED_LIST) and (sublist1 not in EDGE_PROCESSED_LIST):
      EDGE_PROCESSED_LIST.append(sublist)
    else:	
      derived_edge = 0		# this is a new connection
    
  # check if the current edge connection is not recursively checked for adjustment of reachability information
  if (derived_edge == 1):
    # third last parameter signifies derived edge connection 
    AdjustReachGraph(Reachability_Graph_Mat, nodeA, nodeB, edge_type, \
		    COST_UPDATE_LATEST, 0, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)

##-----------------------------------------------------
''' this function modules the AdjustReachGraph function
arguments: nodeA --- whose neighborhood (x) needs to be reviewed
	   nodeB --- relationship between this node and neighborhood (x) of nodeA needs to be examined
	   neighborhood_edge_type - this edge type based neighborhood of nodeA to be examined
	   target_edge_type: species the cost of this type of edge between nodeB and x that needs to be updated 
'''
def ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, neighborhood_edge_type, target_edge_type,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT):
  nodeA_neighb = []
  if (neighborhood_edge_type == DIRECTED_IN_EDGE):
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalInEdgeList())
  elif (neighborhood_edge_type == DIRECTED_OUT_EDGE):
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalOutEdgeList())
  elif (neighborhood_edge_type == BI_DIRECTED_EDGE):
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalEqEdgeList())
  else:	# no edge list
    nodeA_neighb.extend(PairLeaf_Node_Dict[nodeA]._GetFinalNoEdgeList())
    
  if nodeB in nodeA_neighb:
    nodeA_neighb.remove(nodeB)	# dont consider nodeB
    
  # update the reachability graph
  if (len(nodeA_neighb) > 0):
    for l in nodeA_neighb:
      new_conn_flag = 0	# reset the new connection flag
      if (target_edge_type == DIRECTED_IN_EDGE):
	key1 = (l, nodeB)
	if (Reachability_Graph_Mat[key1] == 0):
	  Reachability_Graph_Mat[key1] = 1  
	  new_conn_flag = 1
      if (target_edge_type == DIRECTED_OUT_EDGE):
	key1 = (nodeB, l)
	if (Reachability_Graph_Mat[key1] == 0):
	  Reachability_Graph_Mat[key1] = 1
	  new_conn_flag = 1
      if (target_edge_type == BI_DIRECTED_EDGE):
	key1 = (l, nodeB)
	key2 = (nodeB, l)
	if (Reachability_Graph_Mat[key1] == 0) or (Reachability_Graph_Mat[key2] == 0):
	  Reachability_Graph_Mat[key1] = 1  
	  Reachability_Graph_Mat[key2] = 1  
	  new_conn_flag = 1
      if (target_edge_type == NO_EDGE):	# add - sourya
	# check if there is already no edge connection established between these nodes
	if l not in PairLeaf_Node_Dict[nodeB]._GetFinalNoEdgeList():
	  new_conn_flag = 1       
      # now edge connection will be performed, provided that it is a new edge connection
      if (new_conn_flag == 1):
	# now update the edges between the new connection
	kt1 = (nodeB, l)
	kt2 = (l, nodeB)
	#print 'kt1: ', kt1, 'kt2: ', kt2
	if (kt1 not in Pair_Reln_Dict) and (kt2 not in Pair_Reln_Dict):
	  #print 'both not in Pair_Reln_Dict'
	  FinalizeEdgeConnect(Reachability_Graph_Mat, nodeB, l, target_edge_type, \
			      COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
	elif (kt1 in Pair_Reln_Dict):
	  #print 'kt1: ', kt1, ' in Pair_Reln_Dict'
	  FinalizeEdgeConnect(Reachability_Graph_Mat, nodeB, l, target_edge_type, \
			      COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
	else:
	  #print 'kt2: ', kt2, ' in Pair_Reln_Dict'
	  if (target_edge_type == DIRECTED_IN_EDGE):
	    FinalizeEdgeConnect(Reachability_Graph_Mat, l, nodeB, DIRECTED_OUT_EDGE, \
				COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)      
	  elif (target_edge_type == DIRECTED_OUT_EDGE):
	    FinalizeEdgeConnect(Reachability_Graph_Mat, l, nodeB, DIRECTED_IN_EDGE, \
				COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)      
	  else:
	    FinalizeEdgeConnect(Reachability_Graph_Mat, l, nodeB, target_edge_type, \
				COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)      
    
##-----------------------------------------------------
''' this function updates the reachability graph 
on the basis of input edge type between input 2 nodes '''
def AdjustReachGraph(Reachability_Graph_Mat, nodeA, nodeB, edge_type, COST_UPDATE_LATEST,\
		      original_edge, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT):  
  ''' at first mark the current edge in the graph 
  if the edge connection is already established,
  then we do not require for further processing '''
  if (edge_type == DIRECTED_OUT_EDGE):
    key = (nodeA, nodeB)
    if (Reachability_Graph_Mat[key] == 1) and (original_edge == 1):
      # already the edge is connected
      return
    Reachability_Graph_Mat[key] = 1
  if (edge_type == DIRECTED_IN_EDGE):
    key = (nodeB, nodeA)
    if (Reachability_Graph_Mat[key] == 1) and (original_edge == 1):
      # already the edge is connected
      return    
    Reachability_Graph_Mat[key] = 1
  if (edge_type == BI_DIRECTED_EDGE):
    key1 = (nodeA, nodeB)
    key2 = (nodeB, nodeA)
    if (Reachability_Graph_Mat[key1] == 1) \
	and (Reachability_Graph_Mat[key2] == 1) and (original_edge == 1):
      # already the edge is connected
      return
    Reachability_Graph_Mat[key1] = 1
    Reachability_Graph_Mat[key2] = 1
  if (edge_type == NO_EDGE):
    if (nodeA in PairLeaf_Node_Dict[nodeB]._GetFinalNoEdgeList()) and (original_edge == 1):
      # already there is a NO EDGE connection established
      return
  
  # call the function to finalize the edge connectivity between 2 nodes 
  if (original_edge == 1):
    # third from the last argument is 0 
    # it means original (current) edge connection, i.e. it is not derived from an existing edge connection 
    FinalizeEdgeConnect(Reachability_Graph_Mat, nodeA, nodeB, edge_type, \
			COST_UPDATE_LATEST, 0, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)

  ''' now check the neighborhood of the input nodes and adjust reachability '''
  ''' case A - A->B connection '''
  if (edge_type == DIRECTED_OUT_EDGE):
    ''' check the neighbors of nodeA that are connected via edge C->A 
    establish the connection C->B'''
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, DIRECTED_IN_EDGE, DIRECTED_IN_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    ''' check the neighbors of nodeA that are connected via edge C=A
    establish the connection C->B'''      
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, BI_DIRECTED_EDGE, DIRECTED_IN_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    
    ''' check the neighbors of node B that are connected via edge B->C
    establish the connection A->C '''
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, DIRECTED_OUT_EDGE, DIRECTED_OUT_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    ''' check the neighbors of node B that are connected via edge B=C
    establish the connection A->C '''      
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, BI_DIRECTED_EDGE, DIRECTED_OUT_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
		
    # add - sourya
    if 1:
      ''' check the neighbors of nodeA that are connected via edge C><A (no edge connection)
      establish the connection C><B'''            
      ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, NO_EDGE, NO_EDGE,\
		      COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    # end add - sourya 
  
  ''' case B - B->A connection '''
  if (edge_type == DIRECTED_IN_EDGE):
    ''' check the neighbors of node A that are connected via edge A->C
    establish the connection B->C'''
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, DIRECTED_OUT_EDGE, DIRECTED_OUT_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    ''' check the neighbors of node A that are connected via edge A=C 
    establish the connection B->C'''      
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, BI_DIRECTED_EDGE, DIRECTED_OUT_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    
    ''' check the neighbors of node B that are connected via edge C->B
    establish the connection C->A'''
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, DIRECTED_IN_EDGE, DIRECTED_IN_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    ''' check the neighbors of node B that are connected via edge C=B
    establish the connection C->A'''      
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, BI_DIRECTED_EDGE, DIRECTED_IN_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
      
    # add - sourya	
    if 1:
      ''' check the neighbors of node B that are connected via edge C><B (no edge connection)
      establish the connection C><A'''           
      ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, NO_EDGE, NO_EDGE,\
		      COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    # end add - sourya
        
  ''' case C - A=B connection '''
  if (edge_type == BI_DIRECTED_EDGE):
    ''' check the neighbors of node A that are connected via edge A->C
    establish the connection B->C'''  
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, DIRECTED_OUT_EDGE, DIRECTED_OUT_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    ''' check the neighbors of node A that are connected via edge C->A 
    establish the connection C->B'''
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, DIRECTED_IN_EDGE, DIRECTED_IN_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    ''' check the neighbors of node A that are connected via edge A=C 
    establish the connection C=B'''
    # sourya - this is important -- 0 argument ensures the equivalence partition
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, BI_DIRECTED_EDGE, BI_DIRECTED_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)      
		    
    ''' check the neighbors of node B that are connected via edge B->C 
    establish the connection A->C'''	  
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, DIRECTED_OUT_EDGE, DIRECTED_OUT_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    ''' check the neighbors of node B that are connected via edge C->B
    establish the connection C->A'''
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, DIRECTED_IN_EDGE, DIRECTED_IN_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    ''' check the neighbors of node B that are connected via edge B=C 
    establish the connection C=A'''
    # sourya - this is important -- 0 argument ensures the equivalence partition information 
    # to be included in the final edge list
    ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, BI_DIRECTED_EDGE, BI_DIRECTED_EDGE,\
		    COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
      
    # add - sourya	
    if 1:
      ''' check the neighbors of node A that are connected via edge A><C (no edge connection)
      establish the connection B><C'''        
      ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, NO_EDGE, NO_EDGE,\
		      COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
      ''' check the neighbors of node B that are connected via edge C><B (no edge connection)
      establish the connection C><A'''
      ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, NO_EDGE, NO_EDGE,\
		      COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
    # end add - sourya
    
  # add - sourya
  if 1:
    ''' case D - A><B (NO EDGE) connection '''
    if (edge_type == NO_EDGE):
      ''' check the neighbors of node B that are connected by edge B->C
      establish the connection A><C '''
      ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, DIRECTED_OUT_EDGE, NO_EDGE,\
		      COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
      ''' check the neighbors of node B that are connected by edge B=C
      establish the connection A><C '''
      ModuleAdjRchGrph(Reachability_Graph_Mat, nodeB, nodeA, BI_DIRECTED_EDGE, NO_EDGE,\
		      COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
      ''' check the neighbors of node A that are connected via edge A->C
      establish the connection B><C'''  
      ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, DIRECTED_OUT_EDGE, NO_EDGE,\
		      COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
      ''' check the neighbors of node A that are connected via edge A=C
      establish the connection B><C'''  
      ModuleAdjRchGrph(Reachability_Graph_Mat, nodeA, nodeB, BI_DIRECTED_EDGE, NO_EDGE,\
		      COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
  # end add - sourya
