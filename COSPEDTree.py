#!/usr/bin/env python


##---------------------------------------------
''' 
this program is used to generate a supertree (consensus) from a set of constituent trees
the input is multiple source trees
each of the trees need to be decomposed to triplets (tree structure, with ordering and tree level information)
then the triplets need to be joined
there may be conflicts among the input tree - we have to select the consensus

Author: Sourya Bhattacharyya
Dept of CSE, IIT Kharagpur
V1.0 - 15.01.2014 - public release
''' 

## Copyright 2013 Sourya Bhattacharyya and Jayanta Mukherjee.
## All rights reserved.
##
## See "LICENSE.txt" for terms and conditions of usage.
##
##---------------------------------------------



# header files and other modules included
import Header
from Header import *

import Class_Cluster_node
from Class_Cluster_node import *
import Class_Connect_Reln_NodePair
from Class_Connect_Reln_NodePair import *
import Class_PairLeaf_Node
from Class_PairLeaf_Node import *

import Module_Cost_Update
from Module_Cost_Update import *
import Module_Cycle_Detection
from Module_Cycle_Detection import *
import Module_Graph_Manipulate
from Module_Graph_Manipulate import *
import Module_LeafReln
from Module_LeafReln import *
import Module_Update_Reachability_Graph
from Module_Update_Reachability_Graph import *

import UtilFunc
from UtilFunc import *

##-----------------------------------------------------
# this function is useful to parse various options for input data processing
def parse_options():
  
  # comment - sourya
  # generally try to use with -s, -n, -u, -c, -q and -t options 
  # dont use -r option generally 
  # -s option produces better performance
  # -c option is essential
  # -q produce better result (equivalence partition)
  # -t option should be used
  
  parser = OptionParser()
  
  parser.add_option("-I", "--INPFILE", \
			  type="string", \
			  action="store", \
			  dest="INP_FILENAME", \
			  default="", \
			  help="name of the input file containing candidate source trees")
  
  parser.add_option("-p", "--inpform", \
			  type="int", \
			  action="store", \
			  dest="inp_file_format", \
			  default=1, \
			  help="1 - input file format is NEWICK (default) \
			  2 - input file format is NEXUS")
  
  #parser.add_option("-n", "--preservenoedge", \
			  #action="store_false", \
			  #dest="preserve_no_edge_type", \
			  #default=True, \
			  #help="if true, then it prioritizes NO edge type - once an edge is marked as NO edge,\
			  #it will not be changed\
			  #- Default TRUE")  
  
  #parser.add_option("-q", "--equivpart", \
			  #action="store_false", \
			  #dest="equivalence_partition", \
			  #default=True, \
			  #help="if true, then it clusters a group of taxa on the basis of equivalence partition\
			  #- Default TRUE")
  
  #parser.add_option("-r", "--rooted", \
			  #action="store_true", \
			  #dest="default_rooted", \
			  #default=False, \
			  #help="if true, then trees are read and processed as rooted trees\
			  #- Default TRUE")
  
  #parser.add_option("-u", "--underscore", \
			  #action="store_false", \
			  #dest="preserve_underscores", \
			  #default=True, \
			  #help="if true, then this option preserves the underscores of the names of taxa\
			  #- Default TRUE")
  
  parser.add_option("-c", "--costupdate", \
			  action="store_false", \
			  dest="cost_func_update", \
			  default=False, \
			  help="if true, then this option updates the edge costs during each iteration of edge connectivity\
			  - Default FALSE")
  
  #parser.add_option("-s", "--singleedgepriority", \
			  #action="store_false", \
			  #dest="single_edge_existence", \
			  #default=True, \
			  #help="if true, then this option connects two taxa in the final supertree\
			  #if those two taxa have only one single relation in the source trees\
			  #- Default TRUE")
  
  #parser.add_option("-t", "--tiecase", \
			  #action="store_false", \
			  #dest="tree_tiecase", \
			  #default=True, \
			  #help="if true, then during selection among multiple edges having equal cost,\
			  #this option prioritizes certain edge types\
			  #- Default TRUE")
  
  #parser.add_option("-i", "--initcost", \
			  #action="store_true", \
			  #dest="init_cost_compl", \
			  #default=False, \
			  #help="if true, then this option uses one single edge cost assignment\
			  #at the beginning to all the edges\
			  #subsequently no update of edge costs is performed,\
			  #and edge selection is carried out with the initial cost settings\
			  #- Default FALSE")
  
  #parser.add_option("-f", "--fractwt", \
			  #action="store_true", \
			  #dest="fraction_edge_weight", \
			  #default=False, \
			  #help="if true, this option uses fractional values of edge weights for cost updation and edge selection\
			  #- Default FALSE")
			  			  
  #parser.add_option("-O", "--OUTFILE", \
			  #type="string", \
			  #action="store", \
			  #dest="OUT_FILENAME", \
			  #default="", \
			  #help="name of the output file containing final supertree and detailed results")
			  
  opts, args = parser.parse_args()
  return opts, args

##-----------------------------------------------------
''' main function '''
def main():  
  opts, args = parse_options()
  
  PRESERVE_NO_EDGE_TYPE = True 	#opts.preserve_no_edge_type
  EQUIV_PART = True #opts.equivalence_partition
  ROOTED_TREE = False #opts.default_rooted
  PRESERVE_UNDERSCORE = True #opts.preserve_underscores
  COST_UPDATE_LATEST = opts.cost_func_update
  SINGLE_EDGE_TYPE_CONN_PRIORITY = True #opts.single_edge_existence
  TREE_TIE_CASE_ENABLE = True #opts.tree_tiecase
  INIT_COST_PRIOR_PROCESS = False #opts.init_cost_compl
  FRACTION_EDGE_WEIGHT = False #opts.fraction_edge_weight
  INPUT_FILE_FORMAT = opts.inp_file_format
  INPUT_FILENAME = opts.INP_FILENAME
  #OUTPUT_FILENAME = opts.OUT_FILENAME
  
  #--------------------------------------
  if (INPUT_FILENAME == ""):
    print '******** THERE IS NO INPUT FILE SPECIFIED - RETURN **********'
    return
    
  #if (OUTPUT_FILENAME == ""):
    ## we can follow the input filename convention to generate the output filename
    #OUTPUT_FILENAME = 'out_detail_result_text_' + INPUT_FILENAME
    #print '***** THERE IS NO EXPLICIT SPECIFICATION OF THE OUTPUT FILE \
	  #SO THE OUTPUT FILENAME IS SET AS ', OUTPUT_FILENAME
  
  #--------------------------------------
  if (INIT_COST_PRIOR_PROCESS == 1):
    # here we enable the cost function parameter as well
    print 'as Initial cost settings option is enabled so the cost update option is also enabled '
    COST_UPDATE_LATEST = 1
  #--------------------------------------
  
  print '================ status of options ================= (1 means ON)'
  print 'PRESERVE_NO_EDGE_TYPE : ', PRESERVE_NO_EDGE_TYPE
  print 'EQUIV_PART: ', EQUIV_PART
  print 'ROOTED_TREE: ', ROOTED_TREE
  print 'PRESERVE_UNDERSCORE: ', PRESERVE_UNDERSCORE
  print 'COST_UPDATE_LATEST: ', COST_UPDATE_LATEST
  print 'SINGLE_EDGE_TYPE_CONN_PRIORITY: ', SINGLE_EDGE_TYPE_CONN_PRIORITY
  print 'TREE_TIE_CASE_ENABLE: ', TREE_TIE_CASE_ENABLE
  print 'INIT_COST_PRIOR_PROCESS: ', INIT_COST_PRIOR_PROCESS
  print 'FRACTION_EDGE_WEIGHT: ', FRACTION_EDGE_WEIGHT
  print '===>>>  processing the file now ======== '
  
  # note the program beginning time 
  start_timestamp = time.time()
  
  # this variable notes the count of input source trees  
  tree_count = 0	
  
  ''' create one dictionary which acts as 2D array
  it is basically the reachability graph (transitive closure of the generated edge connectivity graph)
  its index is combinations of 2 tuples - namely the nodes (taxa) those are connected '''
  Reachability_Graph_Mat = dict()   
  
  #-------------------------------------  
  ''' read the source trees collection and store it in a tree collection structure
  individual elements of this collection is thus a source tree '''
  Species_TreeList = Read_Species_Data(ROOTED_TREE, PRESERVE_UNDERSCORE, INPUT_FILE_FORMAT, INPUT_FILENAME)  
  
  #-------------------------------------
  ''' from the species data, define the pairwise leaf ordering and store it in convenient structure 
  examine each of the source trees
  at first count the no of different taxa '''
  for k in Species_TreeList:
    # "Curr_tree" contains the current source tree
    tree_count = tree_count + 1
    Curr_tree = Tree(k)
    if 0:
      print 'curr tree: ', Curr_tree
    
    ''' update the input taxa list by generating leaves of the current tree 
    "Complete_Input_Species_List" contains the complete input taxa set '''
    leaf_node_list = Generate_Node_List(Curr_tree.leaf_nodes())
    print 'Tree no : ', tree_count, 'no of leaf nodes: ', len(leaf_node_list),\
	  'edge length : ', len(Curr_tree.get_edge_set())	
    
    for i in range(len(leaf_node_list)):
      if leaf_node_list[i] not in Complete_Input_Species_List:
	if 0:
	  print 'added leaf node: ', leaf_node_list[i], 'in complete species list'
	Complete_Input_Species_List.append(leaf_node_list[i])
	''' we also define one node structure "PairLeaf_Node_Dict" marked by a taxa
	current taxa is the key 
	for each taxa, one such structure is defined '''
	key1 = leaf_node_list[i]
	if key1 not in PairLeaf_Node_Dict:
	  if 0:
	    print 'new node in PairLeaf_Node_Dict : ', key1
	  PairLeaf_Node_Dict.setdefault(key1, PairLeaf_Node())


    ''' now for each pair of taxa, we define another structure containing their relation
    that is, they are ancestor / descendent, or no relation at all
    the structure is formed according to the input source trees
    so one pair of taxa may have multiple types of relation (according to different source trees)
    also any relation may have multiple support (no of source trees confirming the relation) '''
    for i in range(len(leaf_node_list) - 1):
      for j in range(i+1, len(leaf_node_list)):
	# keys are formed by leaf (taxa) pairs
	key1 = (leaf_node_list[i], leaf_node_list[j])
	key2 = (leaf_node_list[j], leaf_node_list[i])	
	# we check whether the pair is already existing in the list of taxa pairs
	if (key1 not in Pair_Reln_Dict) and (key2 not in Pair_Reln_Dict):
	  if 0:
	    print 'Pair_Reln_Dict has new element', key1
	  Pair_Reln_Dict.setdefault(key1, Connect_Reln_NodePair(UNDEFINED_EDGE))
	  ''' now we define the relationship between these two taxa 
	  basically we mark particular relation type'''  
	  DefineLeafPairReln(leaf_node_list[i], leaf_node_list[j], Curr_tree)
	elif (key1 in Pair_Reln_Dict):
	  DefineLeafPairReln(leaf_node_list[i], leaf_node_list[j], Curr_tree)
	else:
	  DefineLeafPairReln(leaf_node_list[j], leaf_node_list[i], Curr_tree)

  print '=========== total no of tree nodes ============= : ', len(PairLeaf_Node_Dict)
  print 'len Pair_Reln_Dict : ', len(Pair_Reln_Dict)
    
  data_read_timestamp = time.time()	# note the timestamp
  
  #------------------------------------------------------------
  ''' we also calculate the connection value between each pair of nodes in the output tree
  the value defines the majority of the edge type that is between those 2 nodes '''
  for l in Pair_Reln_Dict:
    ''' calculate the cost associated with each node pair connection for different edge types 
    single_edge_exist means that only one type of edge connection is set between these two nodes '''
    if (SINGLE_EDGE_TYPE_CONN_PRIORITY):
      # detect if only one type of connection exists, during setting the priority values of different edge connections
      single_edge_exist_list = Pair_Reln_Dict[l]._SetConnPrVal(True, FRACTION_EDGE_WEIGHT)
      single_edge_exist = single_edge_exist_list[0]
      edge_type = single_edge_exist_list[1]
    else:
      # detect if only one type of connection exists, during setting the priority values of different edge connections
      single_edge_exist = Pair_Reln_Dict[l]._SetConnPrVal(False, FRACTION_EDGE_WEIGHT)
      edge_type = NO_EDGE	# only used when single_edge_exist is 1

    #------------------------------------------------------------
    """ we calculate the cost metric value between individual pairs of taxa
    previously the cost metric was equal to the priority metric
    now we change it to make it a function of the in / out degrees of the involved taxa pair 
    the parameter false indicates use of old scheme 
    parameter true means use of new scheme """
    #Pair_Reln_Dict[l]._SetCostMetric(0, l[0], l[1])
    #Pair_Reln_Dict[l]._SetCostMetric(1, l[0], l[1])
    Pair_Reln_Dict[l]._SetCostMetric(2, l[0], l[1])
    
    #------------------------------------------------------------
    ''' also update the cost value for individual elements in the list "Cost_List_Node_Pair"
    each list element contains the following values:
    1) index value of node1 (according to the index maintained in the Complete_Input_Species_List
    2) index value of node2 (according to the index maintained in the Complete_Input_Species_List
    3) edge type (one at a time - so there will be 4 entries for each node pair)
    4) edge cost (the cost associated with one particular edge type '''
    node1_index = Complete_Input_Species_List.index(l[0])
    node2_index = Complete_Input_Species_List.index(l[1])    
    if (single_edge_exist == 0):
      for edge_type in range(4):
	sublist = [node1_index, node2_index, edge_type, Pair_Reln_Dict[l]._GetEdgeCost_ConnReln(edge_type)]
	Cost_List_Node_Pair.append(sublist)
    else:
      # for single edge type, assign that particular connection
      sublist = [node1_index, node2_index, edge_type, Pair_Reln_Dict[l]._GetEdgeCost_ConnReln(edge_type)]
      # this connection is only possible between the current examined taxa pairs
      # if SINGLE_EDGE_TYPE_CONN_PRIORITY is TRUE then the information is placed in single_edge_occurrence_list
      # otherwise it is placed in Cost_List_Node_Pair
      if (SINGLE_EDGE_TYPE_CONN_PRIORITY):
	single_edge_occurrence_list.append(sublist)
      else:
	Cost_List_Node_Pair.append(sublist)
    
  #------------------------------------------------------------
  ''' we initialize the Reachability_Graph_Mat
  for all the node pairs possible, this indicate the edges between this two
  convention -  out edge from the first node to the second node '''
  for l1 in PairLeaf_Node_Dict:
    for l2 in PairLeaf_Node_Dict:
      key = (l1, l2)
      Reachability_Graph_Mat.setdefault(key, 0)
    
  #------------------------------------------------------------
  
  ''' we print the original connection status for all the tree nodes '''
  if 1:
    print 'Complete_Input_Species_List:  ', Complete_Input_Species_List
    for l in PairLeaf_Node_Dict:
      print 'printing information for the node ', l
      PairLeaf_Node_Dict[l]._PrintOriginalNodeInfo()      
    for l in Pair_Reln_Dict:
      print 'printing info for the key: ', l
      Pair_Reln_Dict[l]._PrintRelnInfo()    
    
  # this information is printed to know the maximum possible iterations that the while loops will undergo
  print '=========== max connection pair ============= : ', \
	(len(single_edge_occurrence_list) + len(Cost_List_Node_Pair))      

  print 'len single_edge_occurrence_list: ', len(single_edge_occurrence_list)
  print 'len Cost_List_Node_Pair : ', len(Cost_List_Node_Pair)
	
  #-------------------------------------------------
  ''' if this option is enabled then we inspect all the edges of the list (two nodes and the connecting edge type)
  and perform the update cost operation
  after updating all the edge costs, then we go for sorting the list to select the edges having higher cost metric 
  default value of INIT_COST_PRIOR_PROCESS is 0, though '''
  if (INIT_COST_PRIOR_PROCESS == 1):
    # traverse through all the elements of the cost list 
    for cost_list_idx in range(len(Cost_List_Node_Pair)):
      # current sublist element of the cost list
      curr_list_elem = Cost_List_Node_Pair[cost_list_idx]	
      nodeA = Complete_Input_Species_List[curr_list_elem[0]]
      nodeB = Complete_Input_Species_List[curr_list_elem[1]]
      edge_type = curr_list_elem[2]
      conn_score = curr_list_elem[3]
      # now call the update edge cost function
      UpdateEdgeCost_Conn_Reln(nodeA, nodeB, edge_type, COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS)
  
  #-------------------------------------------------
  ''' now we have to sort the Cost_List_Node_Pair according to the edge cost value 
  that is the 4th field of the sublist 
  we use itemgetter construct for the sorting operation '''
  if (TREE_TIE_CASE_ENABLE == 0):
    # here tie cases are not resolved
    Cost_List_Node_Pair.sort(key = itemgetter(3), reverse=True)	# sorting is done in reverse order
  else:
    # here we try to resolve the tie case    
    # insertion sort of the list Cost_List_Node_Pair
    for j in range(1, len(Cost_List_Node_Pair)):
      key_sublist = Cost_List_Node_Pair[j]
      # insert this key_sublist in the sorted sequence Cost_List_Node_Pair[0.....j-1]
      i = j - 1
      # case 1 - if the edge cost of the current sublist is greater than the sorted sequence value
      # then shift the sorted sequence
      # case 2 - if the edge cost are equal but the sorted sequence has NO_EDGE type whereas the new list has 
      # a valid edge type then shift the sorted sequence  
      # case 3 - if the edge cost are equal but the sorted sequence has lower frequency of that edge type 
      # whereas the new list has higher frequency of its edge type then shift the sorted sequence  
      while (i >= 0):
	# if the sorted element cost is greater than the current element cost then no need to move further
	if (Cost_List_Node_Pair[i][3] < key_sublist[3]):
	  i = i - 1
	elif (Cost_List_Node_Pair[i][3] == key_sublist[3]):
	  # for tie case of cost
	  if ((Cost_List_Node_Pair[i][2] == NO_EDGE) and (key_sublist[2] != NO_EDGE)):
	    # no edge has low priority
	    i = i - 1
	  elif (Pair_Reln_Dict[(Complete_Input_Species_List[Cost_List_Node_Pair[i][0]], \
				Complete_Input_Species_List[Cost_List_Node_Pair[i][1]])]._GetConnPrVal(Cost_List_Node_Pair[i][2])\
		< Pair_Reln_Dict[(Complete_Input_Species_List[key_sublist[0]], \
				  Complete_Input_Species_List[key_sublist[1]])]._GetConnPrVal(key_sublist[2])):		#_GetEdgeWeight
	    # higher edge frequency have greater priority
	    i = i - 1
	  else:
	    break
	else:
	  break
      
      # now copy the sublist content to the appropriate location
      if (i < j - 1):
	del Cost_List_Node_Pair[j]
	Cost_List_Node_Pair.insert(i+1, key_sublist)
      
    # if there is provision to include single connectivity edges then we sort that list also
    if (SINGLE_EDGE_TYPE_CONN_PRIORITY):
      # insertion sort of the list single_edge_occurrence_list
      for j in range(1, len(single_edge_occurrence_list)):
	key_sublist = single_edge_occurrence_list[j]
	# insert this key_sublist in the sorted sequence single_edge_occurrence_list[0.....j-1]
	i = j - 1
	# case 1 - if the edge cost of the current sublist is greater than the sorted sequence value
	# then shift the sorted sequence
	# case 2 - if the edge cost are equal but the sorted sequence has NO_EDGE type whereas the new list has 
	# a valid edge type then shift the sorted sequence      
	# case 3 - if the edge cost are equal but the sorted sequence has lower frequency of that edge type 
	# whereas the new list has higher frequency of its edge type then shift the sorted sequence  
	while (i >= 0):
	  # if the sorted element cost is greater than the current element cost then no need to move further
	  if (single_edge_occurrence_list[i][3] < key_sublist[3]):
	    i = i - 1
	  elif (single_edge_occurrence_list[i][3] == key_sublist[3]):
	    # for tie case of cost
	    if ((single_edge_occurrence_list[i][2] == NO_EDGE) and (key_sublist[2] != NO_EDGE)):
	      # no edge has low priority
	      i = i - 1
	    elif (Pair_Reln_Dict[(Complete_Input_Species_List[single_edge_occurrence_list[i][0]], \
				  Complete_Input_Species_List[single_edge_occurrence_list[i][1]])]._GetConnPrVal(single_edge_occurrence_list[i][2])\
		  < Pair_Reln_Dict[(Complete_Input_Species_List[key_sublist[0]], \
				    Complete_Input_Species_List[key_sublist[1]])]._GetConnPrVal(key_sublist[2])):	#_GetEdgeWeight
	    # higher edge frequency have greater priority	
	      i = i - 1
	    else:
	      break
	  else:
	    break

	# now copy the sublist content to the appropriate location
	if (i < j - 1):
	  del single_edge_occurrence_list[j]
	  single_edge_occurrence_list.insert(i+1, key_sublist)
      
  data_initialize_timestamp = time.time()	# note the timestamp
  #-------------------------------------  
  # here we first inspect the case where single edge type between a pair of nodes is predominant
  # we have already stored those cases in a list  
  '''
  # comment - sourya
  
  if (SINGLE_EDGE_TYPE_CONN_PRIORITY):
    if (len(single_edge_occurrence_list) > 0):
      for outlist in single_edge_occurrence_list:
	nodeA = Complete_Input_Species_List[outlist[0]]
	nodeB = Complete_Input_Species_List[outlist[1]]
	edge_type = outlist[2]
	conn_score = Pair_Reln_Dict[(nodeA, nodeB)]._GetEdgeCost_ConnReln(edge_type)
	# in the following routine, we provide the copy of Reachability_Graph_Mat as an argument
	# since the structure will be modified during cycle detection, in those modules
	# to recover the original structure, the copy is given 
	if (CyclePossible(nodeA, nodeB, Reachability_Graph_Mat.copy(), \
			  edge_type, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST) == 0):
	  print '==========>>>>>>>>> SINGLE EDGE --- nodes to be connected next: ', nodeA, nodeB, \
		'edge type: ', edge_type, 'conn score: ', conn_score
	  
	  # also update the reachability graph information
	  # third from the last parameter signifies new edge connection (1 in this case)
	  AdjustReachGraph(Reachability_Graph_Mat, nodeA, nodeB, edge_type, \
			  COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
			  
	  print 'len Cost_List_Node_Pair : ', len(Cost_List_Node_Pair)
	  
	  # this function is called to update the edge score between the two nodes, and also on their neighborhood
	  # only the non processed neighborhood is considered 
	  if (COST_UPDATE_LATEST == 1) and (INIT_COST_PRIOR_PROCESS == 0):
	    # for individual edges connected during this iteration, update the cost of the non-processed neighborhood
	    for list_idx in range(len(EDGE_PROCESSED_LIST)):
	      nodeA = Complete_Input_Species_List[EDGE_PROCESSED_LIST[list_idx][0]]
	      nodeB = Complete_Input_Species_List[EDGE_PROCESSED_LIST[list_idx][1]]
	      edge_type = EDGE_PROCESSED_LIST[list_idx][2]
	      # now call the update edge cost function
	      UpdateEdgeCost_Conn_Reln(nodeA, nodeB, edge_type, COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS)
	    # now reset the EDGE_PROCESSED_LIST structure
	    del EDGE_PROCESSED_LIST[:]
	
  
  # end comment - sourya
  '''
  
  # add - sourya
  if (SINGLE_EDGE_TYPE_CONN_PRIORITY):
    while (0 < len(single_edge_occurrence_list)):
      # extract the 1st element of "single_edge_occurrence_list" 
      # since it is sorted to have max cost at the beginning      
      outlist = single_edge_occurrence_list[0]
      src_node = Complete_Input_Species_List[outlist[0]]
      dest_node = Complete_Input_Species_List[outlist[1]]
      src_to_dest_edge_type = outlist[2]
      conn_score = Pair_Reln_Dict[(src_node, dest_node)]._GetEdgeCost_ConnReln(src_to_dest_edge_type)
      
      # in the following routine, we provide the copy of Reachability_Graph_Mat as an argument
      # since the structure will be modified during cycle detection, in those modules
      # to recover the original structure, the copy is given 
      if (CyclePossible(src_node, dest_node, Reachability_Graph_Mat.copy(), \
			src_to_dest_edge_type, PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST) == 1):
	
	# as this element creates a cycle, remove this element (at 0th index) from the list 
	single_edge_occurrence_list.pop(0)
	if 0:
	  print 'possible cycle -- node1 : ', src_node, \
		' node2: ', dest_node, ' edge type : ', src_to_dest_edge_type
	# call the selective removal function of the particular edge type and the target node type
	# from the structure for individual nodes	      
	if (src_to_dest_edge_type == NO_EDGE) or (src_to_dest_edge_type == BI_DIRECTED_EDGE):
	  dest_to_src_edge_type = src_to_dest_edge_type
	elif (src_to_dest_edge_type == DIRECTED_IN_EDGE):
	  dest_to_src_edge_type = DIRECTED_OUT_EDGE
	else:
	  dest_to_src_edge_type = DIRECTED_IN_EDGE
	# dest_node and src_to_dest_edge_type is removed from the structure of src_node
	PairLeaf_Node_Dict[src_node]._SelectivelyRemoveEdgeOrigConn(src_to_dest_edge_type, dest_node)
	# src_node and dest_to_src_edge_type is removed from the structure of dest_node
	PairLeaf_Node_Dict[dest_node]._SelectivelyRemoveEdgeOrigConn(dest_to_src_edge_type, src_node)
      else:
	# current element does not create a cycle 
	# valid connection is found - append this connection to the final formed DFS
	# update the node counter 
	print '==========>>>>>>>>> SINGLE EDGE --- NEW CONN --- nodes to be connected next: ', src_node, dest_node, \
	      'edge type: ', src_to_dest_edge_type, 'conn score: ', conn_score
	
	# also update the reachability graph information
	# third from the last parameter signifies new edge connection (1 in this case)
	AdjustReachGraph(Reachability_Graph_Mat, src_node, dest_node, src_to_dest_edge_type, \
			COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
				
	# this function is called to update the edge score between the two nodes, and also on their neighborhood
	# only the non processed neighborhood is considered 
	if (COST_UPDATE_LATEST == 1) and (INIT_COST_PRIOR_PROCESS == 0):
	  # for individual edges connected during this iteration, update the cost of the non-processed neighborhood
	  for list_idx in range(len(EDGE_PROCESSED_LIST)):
	    nodeA = Complete_Input_Species_List[EDGE_PROCESSED_LIST[list_idx][0]]
	    nodeB = Complete_Input_Species_List[EDGE_PROCESSED_LIST[list_idx][1]]
	    edge_type = EDGE_PROCESSED_LIST[list_idx][2]
	    # now call the update edge cost function
	    UpdateEdgeCost_Conn_Reln(nodeA, nodeB, edge_type, COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS)
	  # now reset the EDGE_PROCESSED_LIST structure
	  del EDGE_PROCESSED_LIST[:]
    
  # end add - sourya
  
  ##------------------------------------------------------------------
  ''' now we extract one by one, different edge connectivity between 2 nodes
  provided they do not create cycle and also are formed according to maximum consensus rule 
  this will create a connected acyclic tree 
  where each node of the tree is basically a pair of leaves (taxa) of the original source trees '''    
  
  while (0 < len(Cost_List_Node_Pair)):
    # extract the 1st element of "Cost_List_Node_Pair" 
    # since it is sorted to have max cost at the beginning
    curr_list_elem = Cost_List_Node_Pair[0]
    src_node = Complete_Input_Species_List[curr_list_elem[0]]
    dest_node = Complete_Input_Species_List[curr_list_elem[1]]
    src_to_dest_edge_type = curr_list_elem[2]      
    conn_score = curr_list_elem[3]
    
    if (CyclePossible(src_node, dest_node, Reachability_Graph_Mat.copy(), src_to_dest_edge_type,\
		      PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST) == 1):
      # as this element creates a cycle, remove this element (at 0th index) from the list 
      Cost_List_Node_Pair.pop(0)
      if 1:
	print 'possible cycle -- node1 : ', src_node, \
	      ' node2: ', dest_node, ' edge type : ', src_to_dest_edge_type
      # call the selective removal function of the particular edge type and the target node type
      # from the structure for individual nodes	      
      if (src_to_dest_edge_type == NO_EDGE) or (src_to_dest_edge_type == BI_DIRECTED_EDGE):
	dest_to_src_edge_type = src_to_dest_edge_type
      elif (src_to_dest_edge_type == DIRECTED_IN_EDGE):
	dest_to_src_edge_type = DIRECTED_OUT_EDGE
      else:
	dest_to_src_edge_type = DIRECTED_IN_EDGE
      # dest_node and src_to_dest_edge_type is removed from the structure of src_node
      PairLeaf_Node_Dict[src_node]._SelectivelyRemoveEdgeOrigConn(src_to_dest_edge_type, dest_node)
      # src_node and dest_to_src_edge_type is removed from the structure of dest_node
      PairLeaf_Node_Dict[dest_node]._SelectivelyRemoveEdgeOrigConn(dest_to_src_edge_type, src_node)
    else:
      # current element does not create a cycle 
      # valid connection is found - append this connection to the final formed DFS      
      print '==========>>>>>>>>> NEW CONN -- nodes to be connected next: ', src_node, dest_node,\
	    'edge type: ', src_to_dest_edge_type, 'conn score: ', conn_score 
      
      # also update the reachability graph information 
      # third last parameter signifies new edge connection
      AdjustReachGraph(Reachability_Graph_Mat, src_node, dest_node, src_to_dest_edge_type, \
		      COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)
      
      # EDGE_PROCESSED_LIST contains the list of connections that have been established
      # during current iteration (by the function AdjustReachGraph)
      # for each such new connection (already established) A ? B 
      # (where ? denotes a particular edge type)
      # we check the non processed neighborhood of A and B
      # that is, the nodes (taxa) connected to A or B w.r.t candidate source trees
      # from such neighborhood, we can find possible edge connections that can be established in future
      if (COST_UPDATE_LATEST == 1) and (INIT_COST_PRIOR_PROCESS == 0):
	for list_idx in range(len(EDGE_PROCESSED_LIST)):
	  nodeA = Complete_Input_Species_List[EDGE_PROCESSED_LIST[list_idx][0]]
	  nodeB = Complete_Input_Species_List[EDGE_PROCESSED_LIST[list_idx][1]]
	  edge_type = EDGE_PROCESSED_LIST[list_idx][2]
	  # now call the update edge cost function
	  UpdateEdgeCost_Conn_Reln(nodeA, nodeB, edge_type, \
				  COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS)
	# now reset the EDGE_PROCESSED_LIST structure
	del EDGE_PROCESSED_LIST[:]
  
  ##------------------------------------------------------------------  
  # comment - sourya
  '''
  while (1):
    # if the Cost_List_Node_Pair does not contain an element 
    # then break from this loop
    if (0 == len(Cost_List_Node_Pair)):
      break
    # otherwise search for first valid entry in the list 
    # which can be used for next connection
    valid_conn_found = 0
    while (valid_conn_found != 1) and (len(Cost_List_Node_Pair) > 0):
      curr_list_elem = Cost_List_Node_Pair[0]
      src_node = Complete_Input_Species_List[curr_list_elem[0]]
      dest_node = Complete_Input_Species_List[curr_list_elem[1]]
      src_to_dest_edge_type = curr_list_elem[2]      
      # valid_conn_found check if current edge connection yields a cycle - 
      # then we have to check for next valid connection 
      if (CyclePossible(src_node, dest_node, Reachability_Graph_Mat.copy(), src_to_dest_edge_type,\
			PRESERVE_NO_EDGE_TYPE, COST_UPDATE_LATEST) == 0):
	valid_conn_found = 1
      else:
	# as this element creates a cycle, 
	# remove this element (at 0th index) from the list 
	Cost_List_Node_Pair.pop(0)
	# also for this edge type and particular set of nodes, 
	# delete the corresponding other node from original edge list as well
	src_node = Complete_Input_Species_List[curr_list_elem[0]]
	dest_node = Complete_Input_Species_List[curr_list_elem[1]]
	src_to_dest_edge_type = curr_list_elem[2]
	#print 'possible cycle -- node1 : ', src_node, ' node2: ', dest_node, ' edge type : ', src_to_dest_edge_type
	if (src_to_dest_edge_type == NO_EDGE) or (src_to_dest_edge_type == BI_DIRECTED_EDGE):
	  dest_to_src_edge_type = src_to_dest_edge_type
	elif (src_to_dest_edge_type == DIRECTED_IN_EDGE):
	  dest_to_src_edge_type = DIRECTED_OUT_EDGE
	else:
	  dest_to_src_edge_type = DIRECTED_IN_EDGE
	# call the selective removal function of the particular edge type 
	# and the target node from the list of nodes
	# maintained as a list
	PairLeaf_Node_Dict[src_node]._SelectivelyRemoveEdgeOrigConn(src_to_dest_edge_type, dest_node)
	PairLeaf_Node_Dict[dest_node]._SelectivelyRemoveEdgeOrigConn(dest_to_src_edge_type, src_node)
      
    # if valid connection is found then append this connection to the final formed DFS
    if (valid_conn_found == 1):
      # update the node counter 
      nodeA = Complete_Input_Species_List[curr_list_elem[0]]
      nodeB = Complete_Input_Species_List[curr_list_elem[1]]
      edge_type = curr_list_elem[2]
      conn_score = curr_list_elem[3]
      print '==========>>>>>>>>> CONFLICT CONN -- nodes to be connected next: ', nodeA, nodeB,\
	    'edge type: ', edge_type, 'conn score: ', conn_score 
      # also update the reachability graph information 
      # third last parameter signifies new edge connection
      AdjustReachGraph(Reachability_Graph_Mat, nodeA, nodeB, edge_type, \
		      COST_UPDATE_LATEST, 1, INIT_COST_PRIOR_PROCESS, FRACTION_EDGE_WEIGHT)	
		      
      print 'len Cost_List_Node_Pair : ', len(Cost_List_Node_Pair)
      
      # this function is called to update the edge score between the two nodes, and also on their neighborhood
      # only the non processed neighborhood is considered 
      if (COST_UPDATE_LATEST == 1) and (INIT_COST_PRIOR_PROCESS == 0):
	# for individual edges connected during this iteration, update the cost of the non-processed neighborhood
	for list_idx in range(len(EDGE_PROCESSED_LIST)):
	  nodeA = Complete_Input_Species_List[EDGE_PROCESSED_LIST[list_idx][0]]
	  nodeB = Complete_Input_Species_List[EDGE_PROCESSED_LIST[list_idx][1]]
	  edge_type = EDGE_PROCESSED_LIST[list_idx][2]
	  # now call the update edge cost function
	  UpdateEdgeCost_Conn_Reln(nodeA, nodeB, edge_type, COST_UPDATE_LATEST, INIT_COST_PRIOR_PROCESS)
	# now reset the EDGE_PROCESSED_LIST structure
	del EDGE_PROCESSED_LIST[:]
    else:
      break
  '''
  # end comment - sourya
  #-------------------------------------
  # we print the final connection status for all the tree nodes
  if 1:
    for l in PairLeaf_Node_Dict:
      print 'printing information for the node ', l
      PairLeaf_Node_Dict[l]._PrintFinalNodeInfo() 
  
  # we can now clear the content of reachability dictionary from the memory
  Reachability_Graph_Mat.clear()       
  
  # note the timestamp
  reachability_graph_form_timestamp = time.time()
  #-------------------------------------
  ''' now we append each of the tree node (pair of leaves / taxa) to a particular cluster of nodes
  each cluster contains nodes having equality relationship 
  tuple forming equality relationship with current tuple will be inserted in the same cluster '''
  if (EQUIV_PART):
    # this is executed when each set of nodes are clustered based on equivalence partition
    no_of_clusters = 0
    # initialize an empty dequeue structure which can be used for both way insertion
    # though in this program, we'll use only one way insertion
    species_queue = deque()
    for l in PairLeaf_Node_Dict:
      # search for the species which is still not inserted in a partition
      if (PairLeaf_Node_Dict[l]._GetClustInsertStatus() == 0):
	# initialize one new cluster with current species as element 
	no_of_clusters = no_of_clusters + 1
	curr_clust_idx = no_of_clusters
	Cluster_Node_Dict.setdefault(curr_clust_idx, Cluster_node())
	# insert the current species in the queue
	species_queue.append(l)
	# loop until queue is not empty
	while (len(species_queue) > 0):
	  # pop the first element of the queue
	  curr_sp = species_queue.popleft()
	  # for this species l, cluster is assigned
	  Cluster_Node_Dict[curr_clust_idx]._Append_tuple(curr_sp)
	  PairLeaf_Node_Dict[curr_sp]._SetClustInsertStatus()	
	  # search the equivalence partition content by checking eq list 
	  # (which have not been inserted in the cluster)
	  for l2 in PairLeaf_Node_Dict[curr_sp]._GetFinalEqEdgeList():
	    if (PairLeaf_Node_Dict[l2]._GetClustInsertStatus() == 0):
	      # insert the species in the queue
	      species_queue.append(l2)
  else:
    # not equiv partition
    no_of_clusters = 0
    for l in PairLeaf_Node_Dict:
      if (PairLeaf_Node_Dict[l]._GetClustInsertStatus() == 0):
	# initialize one new cluster with current tuple as element 
	no_of_clusters = no_of_clusters + 1
	curr_clust_idx = no_of_clusters
	Cluster_Node_Dict.setdefault(curr_clust_idx, Cluster_node(l))
	# cluster insertion status of this particular node is 1
	PairLeaf_Node_Dict[l]._SetClustInsertStatus()
  #------------------------------------------------------------------------------  
  # here we define a 3D matrix to contain all the elements of the transitive closure (* operation)
  Cluster_Graph_Adj_Mat = []
  for i in xrange(no_of_clusters):
    Cluster_Graph_Adj_Mat.append([])
    for j in xrange(no_of_clusters):
      Cluster_Graph_Adj_Mat[i].append([])
      for k in xrange(no_of_clusters + 1):
	Cluster_Graph_Adj_Mat[i][j].append(0)
  
  # we define a 2D matrix which will store the transitive closure output
  # later it will be compressed to store the transitive reduction output as well
  Cluster_Graph_Trans_Closure_Adj_Mat = []
  for i in xrange(no_of_clusters):
    Cluster_Graph_Trans_Closure_Adj_Mat.append([])
    for j in xrange(no_of_clusters):
      Cluster_Graph_Trans_Closure_Adj_Mat[i].append(0)
  
  ''' now we have to form the edges between this clusters (of nodes)
  say c1 and c2 are two clusters
  we say that there exists an edge between c1 and c2 
  if at least one taxa pair from either cluster are related
  the edge type between the clusters is decided according to the relationship type 
  
  this connectivity information forms the adjacency matrix relation 
  from this initial matrix, we will form its transitive closure '''  
  
  for ci in range(no_of_clusters - 1):
    for cj in range(ci+1, no_of_clusters):
      # list of taxa contained in the first cluster of nodes
      clust1_sp_list = Cluster_Node_Dict[ci+1]._GetSpeciesList()
      # list of taxa contained in the second cluster of nodes
      clust2_sp_list = Cluster_Node_Dict[cj+1]._GetSpeciesList()
      clust1_sp_list_len = len(clust1_sp_list)
      clust2_sp_list_len = len(clust2_sp_list)
      i = 0
      j = 0
      while (i < clust1_sp_list_len):	# and (j < clust2_sp_list_len):
	key1 = clust1_sp_list[i]
	key2 = clust2_sp_list[j]
	# the connectivity can be either out edge or in edge_type
	# since the sibling relationship denotes equivalence partition
	if key2 in PairLeaf_Node_Dict[key1]._GetFinalOutEdgeList():
	  Cluster_Node_Dict[ci+1]._AddOutEdge(cj+1)
	  Cluster_Node_Dict[cj+1]._AddInEdge(ci+1)
	  break
	elif key2 in PairLeaf_Node_Dict[key1]._GetFinalInEdgeList():
	  Cluster_Node_Dict[ci+1]._AddInEdge(cj+1)
	  Cluster_Node_Dict[cj+1]._AddOutEdge(ci+1)
	  break
	else:
	  j = j + 1
	  if (j == clust2_sp_list_len):
	    i = i + 1
	    j = 0
  
  ''' print the cluster information '''
  print '========== cluster information after step 0 ============='
  for i in Cluster_Node_Dict:
    Cluster_Node_Dict[i]._PrintClusterInfo(i)
  
  # note the timestamp
  cluster_of_node_with_init_species_list_form_timestamp = time.time()
  
  #--------------------------------------------------------
  # now from the obtained matrix, generate the transitive closure 
  # Cluster_Graph_Trans_Closure_Adj_Mat stores the transitive closure
  Form_Transitive_Closure(Cluster_Graph_Adj_Mat, Cluster_Graph_Trans_Closure_Adj_Mat, no_of_clusters)
    
  ''' now perform the transitive reduction of the closure 
  this is required to handle the following scenario:
  suppose, there exists a case such that A->C, B->C and A->B
  then in the final graph, only A->B and B->C information needs to be preserved
  in order to form the DAG '''
  CompressDirectedGraph(Cluster_Graph_Trans_Closure_Adj_Mat, no_of_clusters)
    
  # print the cluster information 
  print '========== cluster information after step 1 ============='
  for i in Cluster_Node_Dict:
    Cluster_Node_Dict[i]._PrintClusterInfo(i)
      
  # note the timestamp
  cluster_of_node_refine_species_timestamp1 = time.time()  
  #----------------------------------------------
  ''' now this section constructs the supertree from the generated DAG 
  this is performed by repeatedly extracting the nodes with minimum indegree
  basically we first form a string which represents the supertree '''
  no_of_components = 0	# for forest
  while (1):
    root_clust_node_idx = Extract_Node_Min_Indeg(no_of_clusters)
    if (root_clust_node_idx == -1):
      break
    Tree_Str = PrintNewick(root_clust_node_idx, EQUIV_PART)
    no_of_components = no_of_components + 1
    if (no_of_components == 1):	# first component
      Final_Supertree_Str = Tree_Str
    else:
      Final_Supertree_Str = Final_Supertree_Str + ',' + Tree_Str
  
  # with the final tree string, finally generate the tree result 
  Final_Supertree_Str = '(' + Final_Supertree_Str + ')'
  print '--- final output tree (in newick format): ', Final_Supertree_Str
  
  # now read this super string in a supertree containing all the input taxa
  Supertree_Final = dendropy.Tree.get_from_string(Final_Supertree_Str, schema="newick")	#preserve_underscores=PRESERVE_UNDERSCORE, default_as_rooted=ROOTED_TREE)
  #Supertree_Final.print_plot()  
  
  if 1:
    # write this tree on a separate text file
    outfile = open('output_supertree_newick.tre', 'w')
    outfile.write(Final_Supertree_Str)
    outfile.write('\n \n final tree \n \n')
    outfile.write(Supertree_Final.as_ascii_plot())
    outfile.close()
  
  # final timestamp
  data_process_timestamp = time.time()      
  #----------------------------------------------
    
  # examine each of the source trees and find the FP, FN and RF distance with respect to the generated supertree  
  sumFP = sumFN = 0
  sumRF = 0
  sumLenSrcTree = 0
  sumLenPruneTree = 0
  len_supertree = len(Supertree_Final.get_edge_set())
  print 'total edges of supertree: ', len_supertree
  #print 'taxon set of supertree: ', Supertree_Final.infer_taxa()
  for k in Species_TreeList:
    # input candidate source tree
    Curr_src_tree = Tree(k)
    # corresponding taxa set
    curr_src_tree_taxa = Curr_src_tree.infer_taxa().labels()
    # according to the taxa set, prune the supertree to get the tree portion containing only this taxa set
    pruned_tree = dendropy.Tree(Supertree_Final)
    pruned_tree.retain_taxa_with_labels(curr_src_tree_taxa)
    # edge sets of both the input and output (pruned) trees
    len_curr_src_tree = len(Curr_src_tree.get_edge_set())
    len_pruned_tree = len(pruned_tree.get_edge_set())
    print 'curr tree: ', Curr_src_tree	#, 'len: ', len_curr_src_tree, 'taxon set: ', curr_src_tree_taxa
    print 'pruned tree: ', pruned_tree
    # determine the false positives and the false negatives 
    tup = Curr_src_tree.false_positives_and_negatives(pruned_tree)
    print 'Performance --- src tree len: ', len_curr_src_tree, \
	  'pruned tree len: ', len_pruned_tree, \
	  'FP_int: ', tup[0], 'FN_int: ', tup[1]
    sumFP = sumFP + tup[0]
    sumFN = sumFN + tup[1]
    sumLenSrcTree = sumLenSrcTree + len_curr_src_tree
    sumLenPruneTree = sumLenPruneTree + len_pruned_tree
    sumRF = sumRF + ((tup[0] + tup[1]) / 2.0)

  # print the final result
  print '\n\n\n ===============>>>>>>>>>>>>>>> FINAL RESULTS '
  print '\n absolute sumLenSrcTree: ', sumLenSrcTree, \
	'\n absolute sumLenPruneTree: ', sumLenPruneTree, \
	'\n ******* absolute sumFP: ', sumFP, \
	'\n ******* absolute sumFN: ', sumFN, \
	'\n ******* absolute sumRF: ', sumRF
  print ' ===============>>>>>>>>>>>>>>> IN TERMS OF NORMALIZED \
	  (DIVIDED BY THE SUM OF EDGE LENGTHS OF THE CANDIDATE SOURCE TREES) '''  
  print '\n avg sumFP: ', (sumFP * 1.0) / sumLenSrcTree, \
	'\n sumFN: ', (sumFN * 1.0) / sumLenSrcTree, \
	'\n sumRF: ', (sumRF * 1.0) / sumLenSrcTree
  
  print '\n\n ===============>>>>>>>>>>>>>>> TIME COMPLEXITY OF THE METHOD (in seconds) '
  print '\n reading the data: ', (data_read_timestamp - start_timestamp), \
	'\n initialization of the structure: ', (data_initialize_timestamp - data_read_timestamp), \
	'\n formation of the reachability graph (after loop): ', \
	      (reachability_graph_form_timestamp - data_initialize_timestamp), \
	'\n formation of the clusters (with initial species list and edge connectivity): ', \
	      (cluster_of_node_with_init_species_list_form_timestamp - reachability_graph_form_timestamp), \
	'\n multiple parent (related) problem: ', \
	      (cluster_of_node_refine_species_timestamp1 - cluster_of_node_with_init_species_list_form_timestamp), \
	'\n newick string formation: ', (data_process_timestamp - cluster_of_node_refine_species_timestamp1)
	
  print '\n Total time taken (in seconds) : ', (data_process_timestamp - start_timestamp)

##-----------------------------------------------------

if __name__ == "__main__":
    main() 
