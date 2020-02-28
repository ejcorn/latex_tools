# this script detects the order in which you mention supplemental figures within a latex file for a manuscript
# then will reorder your supplemental figure references and supplemental figure files so they go figure 1-N
# the script assumes you can manually take care of your main figures
# it also assumes that all supp figs are referenced at least once in the manuscript or supplement

import numpy as np
import re
import itertools
import glob
import os

homedir = '/Users/Eli/Dropbox/Cornblath_Bassett_Projects/BrainStateTransitions/Submission2/CommBioPublication/'
tex_files = ['brain-state-transitions_v4_final','brain-state-transitions-supplement_v4_final'] # list of tex files -- usually main + supplement

texdocs = [open(homedir+tex_file+'.tex').readlines() for tex_file in tex_files]

def contains(l,pattern):
	# analagous to matlabs contains() function or R grepl() function. finds pattern in each element of a list
	return([pattern in str(x) for x in l])
def unlist(x):
	return(list(itertools.chain.from_iterable(x)))
def setdiff(list1,list2):
	return list(set(list1) - set(list2))

##############################
### Detect reference order ###
##############################

# get the order of references as they appear throughout all the input tex docs
ref_order = list()
texdoc_all = unlist(texdocs) # concatenate both documents
reflines = [texdoc_all[x] for x in np.where(contains(texdoc_all,'\\ref'))[0]] # read only lines with \ref commands
ref_usages = np.array(unlist([re.findall('\\\\ref\{fig:figureS.*?\}',x) for x in reflines]))
indexes = np.unique(ref_usages, return_index=True)[1]
# order of references in text
ref_order = [ref_usages[idx] for idx in sorted(indexes)]

# get the order of labels as they appear throughout all the input tex docs
labellines = [texdoc_all[x] for x in np.where(contains(texdoc_all,'\\label'))[0]]
label_usages = np.array(unlist([re.findall('\\\\label\{fig:figureS.*?\}',x) for x in labellines]))
indexes = np.unique(label_usages, return_index=True)[1]
# order of figure appearance
label_order = [label_usages[idx] for idx in sorted(indexes)]

##########################
### Reorder references ###
##########################

# replace all inline references and figure labels so that all in-text figure reference
# labels are in numerical order, i.e. \ref{fig:figureS1} appears before \ref{fig:figureS2}

old_ref_kernels = ['{'+x.split('f{')[1].split('}')[0] + '}' for x in ref_order] # get core of reference, present in \ref and \label instances
new_ref_kernels = ['{fig:figureS'+str(f) + '}' for f in np.arange(1,len(ref_order)+1)] # new references are figS1-N regardless of old refs
unique_identifier = 'ElIcOrNbLaTh0929234' # temporary identifier so every reference is guaranteed to stay unique and no mix ups
new_refs_tmp_kernel = ['{fig:figureS'+str(f) +unique_identifier+ '}' for f in np.arange(1,len(ref_order)+1)] # make temporary new references to avoid possible mix ups

# first swap out all references

def ref_swap(texdoc,old_refs,new_refs):
	# INPUTS:
	# texdoc: list whose elements contain each line of a tex document
	# fname: file name for new tex doc to be written
	# old_refs: list of references kernels (i.e. fig:figure)
	#
	# OUTPUTS:
	# new_texdoc: list whose elements are those of texdoc, but with
	# all instances of the elements of old_refs
	# replaced by the corresponding index element of new_refs (i.e. new_refs[0] for old_refs[0])
	
	new_texdoc = list()
	for i in range(len(texdoc)):
		s = texdoc[i]
		for idx,ref_kernel in enumerate(old_refs): # loop through each possible reference
			ref_instances = re.findall(ref_kernel,s) # find instances of that reference	-- this is either unnecessary or it avoids unnecessary loops
			for ref_instance in np.unique(np.array(ref_instances)):
				s = s.replace(ref_instance,new_refs[idx]) # replace with temporary new identifier
		new_texdoc.append(s)
	return new_texdoc

# swap in the temporary unique keyss for each reference
new_texdocs = [ref_swap(texdoc,old_ref_kernels,new_refs_tmp_kernel) for texdoc in texdocs] 
# swapout the temporary unique keys for the new ordered keys
new_texdocs = [ref_swap(texdoc,new_refs_tmp_kernel,new_ref_kernels) for texdoc in new_texdocs] 

# write new tex documents with reordered references and figs
for j in range(len(new_texdocs)):
	fname = homedir+tex_files[j]+'_refreorder.tex'
	with open(fname,'w') as fout:
		[fout.write(s) for s in new_texdocs[j]]

## confirm reordering of references in tex doc
# get the order of references as they appear throughout all the input tex docs
ref_order = list()
texdoc_all = unlist(new_texdocs) # concatenate both documents
reflines = [texdoc_all[x] for x in np.where(contains(texdoc_all,'\\ref'))[0]] # read only lines with \ref commands
ref_usages = np.array(unlist([re.findall('\\\\ref\{fig:figureS.*?\}',x) for x in reflines]))
indexes = np.unique(ref_usages, return_index=True)[1]
# order of references in text --- this should output fig:figureS1, fig:figureS2, ...
ref_order = [ref_usages[idx] for idx in sorted(indexes)]

# now at the end, go into your tex files
# and copy and paste your figures so that the labels are in order and you're good