
***Using the FastNLO code setup:

1. rename your zeroth table to d**-x01-y01-0000.tab
2. gzip all of your tables (“gzip *.tab”)
3. run doMergeTables.py (have to move the python file to the same directory as the tables)
4. run getStatUncert.py
5. cmsenv within CMSSW_7_1_30/src
6. run getASVarFNLO_ME.py, getASVarFNLO_MEPDF.py scripts
7. run getPDFUncert, getScaleUncert (needs newer version of FastNLO, use installation v2; source the environment inside the MakeTablesv2 folder)

If you want to do NP corrections, use yodamerge script:
1. source FNLO environment
2. cmsenv in CMSSW_10_0_0/src

