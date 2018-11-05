COSPEDTree (Couplet based Phylogenetic Supertree algorithm, using equivalence partitioning and taxa set formation)
-------------

(Note: a much efficient and of lower running time version, COSPEDBTree (or COSPEDTree-II) is available in GitHub. 
user may use that version).

COSPEDTree is a python package to compute phyloegentic supertree from input trees having conflicting topologies and 
possibly overlapping taxa subsets. The tool proposes phylogenetic relations among individual couplets, and aims 
to resolve the topological conflicts via selecting the most frequent couplet specific relations in an iterative fashion. 
The selected couplet relations are assembled to form a directed acyclic graph (DAG), from which the final supertree 
is generated.

Input
------

Phylogenetic trees with conflicting topologies and possibly overlapping taxa subsets. Input trees can be either in 
NEWICK format or in NEXUS format. However, all input trees should have identical input formats.

Output
--------

Output tree is generated in the NEWICK format.

Dependencies / Installation Requirements
----------------

COSPEDTree is developed in Linux Systems (Ubuntu 12.04), using Python 2.7. 
User needs to install following before using this package:

1) Python 2.7 (available in Ubuntu, by default).

Note: Current implementation of COSPEDTree do not support Python 3. A future release would cover it.

2) Dendropy ( available on the link: https://pythonhosted.org/DendroPy/ )

Note: we have used version 3.12.0 for implementation. Future releases of Dendropy are to be tested and incorporated 
in a separate release.

3) Numpy ( available on the link: http://www.numpy.org/ )

Available via pip (python software installer tool).


Execution 
-------------

COSPEDTree.py is the main executable. Its execution is done by the following command:

python COSPEDTree.py [options]
	  
Details of the options are mentioned below:

  -h, --help            

	show this help message and exit
  
  -I INP_FILENAME, --INPFILE=INP_FILENAME
                        
	Input file containing input set of trees.
                        
  -p INP_FILE_FORMAT, --inpform=INP_FILE_FORMAT
                        
	1 - input file format is NEWICK (default)
	2 - input file format is NEXUS       
	USER MUST PROVIDE either p = 1 or 2
  
  -c, --costupdate      
           
	Boolean option: toggles the default (FALSE) settings.
	if TRUE, updates the cost settings of individual relations after each iteration. 
	Recommended: TRUE
	May incur high running time for large trees.			                
                        

Example of a command:

python COSPEDTree.py -I source_tree_input.txt -p1 > out.txt (redirecting the console)

Output description
--------------------

Output log and detailed execution are printed in console.

A file "output_supertree_newick.tre" is created in the current directory, which contains the generated supertree.

At the end of the output console, performance metrics like SUMFP, sumFN, between the output supertree and the 
input trees are also printed.

Citation
---------

Upon using this package, users need to cite the following articles:

1) Sourya Bhattacharyya, and Jayanta Mukherjee, "COSPEDTree: COuplet Supertree by Equivalence Partitioning of 
taxa set and DAG formation", IEEE/ACM Transactions on Computational Biology and Bioinformatics, pp. 1-1, doi: http://doi.ieeecomputersociety.org/10.1109/TCBB.2014.2366778

2) Sourya Bhattacharyya, and Jayanta Mukhopadhyay, "COuplet Supertree by Equivalence Partitioning of 
taxa set and DAG formation", Proceedings of the 5th ACM Conference on Bioinformatics, Computational 
Biology and Health Informatics (ACM-BCB), Newport, California, September 2014, pages 259-268.



For any queries, please contact
-------------------------------

Sourya Bhattacharyya 

La Jolla Institute for Allergy and Immunology

La Jolla, CA, 92037, USA

<sourya.bhatta@gmail.com>




