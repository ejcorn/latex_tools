# latex_tools
 Tools that automatically edit latex files for scientific publications.

This repository houses scripts that can be used for automatically editing and processing LaTeX files for scientific publication. All scripts were tested on an anaconda distribution of python 3.6.9. In this read me, I will describe each script one by one:

## reforder.py

This script will take in a set of LaTeX .tex documents, identify the order of appearance in the text of each supplemental figure, and then reorder your in text references so that they are all called fig:figureS1, fig:figureS2, and so forth, in order of appearance in the text. This doesn't assume anything about the formatting of your references initially, but will change them all to the fig:figureSX format, including both \ref and \label instances. 

After running the script, you need to manually copy and paste around your figure blocks so that they are in order. You can use this script to check the order of your labels after doing so (`label_order` variable). The script also assumes you will order your main text figures by yourself, but can easily use it to check the order of appearace of references by changing line 33 to 
```python
ref_usages = np.array(unlist([re.findall('\\\\ref\{fig:figure.*?\}',x) for x in reflines]))
```

The script requires 2 input variables:
   - `homedir`: the local path to the directory containing your .tex files
   - `tex_files`: a list of filenames for .tex files to assess, without the extension
