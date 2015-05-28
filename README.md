# COSPEDTree
Couplet based Phylogenetic Supertree algorithm, using equivalence partitioning and taxa set formation

************************************************
Project Topic / Keywords related to this repository
************************************************
Computational Phylogenetics
Phylogenetic Trees
Supertree Algorithm


*********************************
Introduction
*********************************

COSPEDTree is a python based tool for computing supertree from input phylogenetic trees.
Input phylogenetic trees may contain overlapping taxa set.
These trees often exhibit different topologies among constituent taxa set.

Objective is to produce a supertree covering all the input taxa
so that individual taxa subsets exhibit consensus relationships as much as possible.
This is known as satisfying "Maximum agreement property"

However, given the conflicting nature of input trees, often the consensus (most freqent) relations 
among individual taxa subsets may not be reflected in the final supertree. This is because, consensus 
relation among a taxa subset may conflict with the consensus relation of another taxa subset.

Supertree computation is formed using a greedy approach. The method is based on partitioning the input set of taxa based on equivalence relation. The relation is defined between individual taxa pairs (couplet), leading to the 
proposed couplet based supertree technique.

The relationship among a couplet can be of the following three types:
1) ancestor / descendent 
2) sibling 
3) inconclusive relation characteristics. 

The sibling relation is in fact, an equivalence relation. Definition of these relations can be found in our paper (reference provided below).

According to the equivalence relation, input taxa set is partitioned. After that, a Directed Acyclic Graph (DAG) is formed initially. From this DAG, the output tree is generated.

Input source trees can be either in NEWICK format or in NEXUS format. 
However, all the source trees should have identical input formats. 
Output tree is generated in the NEWICK format.

*********************************
Dependencies / Installation Requirements
*********************************
COSPEDTree is developed in Linux Systems (Ubuntu 12.04), using Python 2.7.

User needs to install following before using this package:

1) Python 2.7 (available in Ubuntu, by default)
2) Dendropy ( available on the link: https://pythonhosted.org/DendroPy/ )
3) Numpy ( available on the link: http://www.numpy.org/ )

For systems having Ubuntu with lower versions, please notify in case of any errors. 

*********************************    
Execution 
*********************************

COSPEDTree is to be executed with the following command line options, from a terminal:
(assuming the present working directory contains the source codes)

chmod +x COSPEDTree.py (To change its permission to make it an executable file)

./COSPEDTree.py [options]

*********************
NOTE: 

All the options except the first three, signify toggle / complement of their corresponding DEFAULT values.
First option (help) displays these command line parameters.

It Is Preferable For A Beginner, To Not Use Any Option Other Than The Second And Third Options.
Second option is for specifying the input filename (mandatory)
Third option is for specifying the corresponding file format.
***********************
	  
Details of the options are mentioned below:

  -h, --help            
                    show this help message and exit
  
  -I INP_FILENAME, --INPFILE=INP_FILENAME
                        name of the input file containing candidate source trees (a text file)
                        USER MUST PROVIDE ONE VALID INPUT FILE CONTAINING THE TREE DATA
                        OTHERWISE PROGRAM WILL BREAK FROM EXECUTION
                        
  -p INP_FILE_FORMAT, --inpform=INP_FILE_FORMAT
                        
                        1 - input file format is NEWICK (default)
                        2 - input file format is NEXUS       
                        USER MUST PROVIDE either p = 1 or 2
  

  -c, --costupdate      
                    
                      using this option toggles the corresponding condition
			                if true, then this option performs extensive update 
			                of the edge costs during each iteration of edge connectivity
                      - Default FALSE, that is the option is reset 
			                using this option thus toggles the variable to set, i.e. 
			                opting for dynamic edge cost updation for greedy scoring
			                
                        
*******************
Example of a command 
(followed for the results published in the manuscript)
*******************

  ./COSPEDTree -I source_tree_input.txt -p1 > out.txt

  descriptions:
  1) -I specifies the input filename
  2) source_tree_input.txt : contains the input collection of trees
  3) -p option is for specifying the input tree format
    input file contains the trees in NEWICK format, as specified by the option (-p1) (1 stands for newick)

  All the detailed results (textual descriptions) are redirected to file out.txt
  
  
**********************
GENERATION OF FINAL OUTPUT SUPERTREE
**********************
  
The output tree and all the results are printed at console.
User can redirect the output results to any standard text file by using standard 
redirection operation (>)

Considering the example command above:  
  
  1) The file 'out.txt' contains detail execution results. 
  2) In addition, one output file "output_supertree_newick.tre" is created in the current directory
    it contains the derived supertree information (in both newick string format as well as tree plot)
  3) The tree can be used subsequently for performance metric computation
  4) At the end of the file 'out.txt', users can find the results of metrics SUMFP, sumFN, 
  obtained by comparing the output supertree and the input set of source trees.


*********************************
Utilities
*********************************
COSPEDTree requires O(N^3 + MN^2 lgN) time and O(N^2) space complexity, for N input taxa and M input trees.
Both the time and space complexities are equal or lower than existing species tree construction methods.

******************************
Citation
*********************************
Upon using this package, users need to cite the following articles:

1) Sourya Bhattacharyya, and Jayanta Mukherjee, "COSPEDTree: COuplet Supertree by Equivalence Partitioning of taxa set and DAG formation", IEEE/ACM Transactions on Computational Biology and Bioinformatics, pp. 1-1, doi: http://doi.ieeecomputersociety.org/10.1109/TCBB.2014.2366778

2) Sourya Bhattacharyya, and Jayanta Mukhopadhyay, "COuplet Supertree by Equivalence Partitioning of taxa set and DAG formation", Proceedings of the 5th ACM Conference on Bioinformatics, Computational Biology and Health Informatics (ACM-BCB), Newport, California, September 2014, pages 259-268.


*********************************
For any queries, please contact
*********************************

Sourya Bhattacharyya 
Department of Computer Science and Engineering
Indian Institute of Technology Kharagpur
<sourya.bhatta@gmail.com>




