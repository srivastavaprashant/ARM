# ARM
This repository provides the code for ARM, a novel self-attention framework for flexible entity relation extraction from biological literature.

**Authors and Contributors**: *Prashant Srivastava, Saptarshi Bej, Kristian Schultz, Kristina Yordanova, Olaf Wolkenhauer*

**Steps**
1. Create a new folder in root dir named 'Data'.
2. Download Datasets for <a href="https://air.bio.informatik.uni-rostock.de/">AIR</a>, 
                         <a href="https://www.grnpedia.org/trrust/">TRRUST</a>, 
                         <a href="https://geneticassociationdb.nih.gov/">GAD</a>, 
                         <a href="https://biocreative.bioinformatics.udel.edu/news/corpora/chemprot-corpus-biocreative-vi/">ChemProt</a>, 
                         <a href="https://thebiogrid.org/">BioGRID</a>, and 
                         <a href="https://github.com/elangovana/PPI-typed-relation-extractor">Elangovan et al.</a> 
                         and save them in /Data.
                           
2. Register at Entrez Programming Utilities (E-utilities) and obtain Email and api-key. 
3. Create a file named 'config.py' with following code: <br>
```python
entrez_api_key = 'Your-Entrez-email'
entrez_email = 'Your-Entrez-apikey'
```
4. Navigate to /Preprocessing dir and run the jupyter-notebooks for all datasets. <br>
 **_Running all the notebooks in this directory with produce entity normalized datasets that are required in next step._**
5. Run Typed Interactions.ipynb for typed relations Case Study. 
6. Run Untyped Interactions.ipynb for untyped relations Case Study. 
