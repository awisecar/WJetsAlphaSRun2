
*** To run the Sherpa+Rivet+FastNLO routine to generate FastNLO tables ***


 ==> In order to produce FastNLO tables, we do the following procedure:
1) go to the proper working directory, source the needed environment script
2) if not already done, need to --
  a) compile the Rivet analysis files that are in the "analysis" sub-folder, copy out these files to necessary locations
  b) run the Sherpa run card initialization step
  c) run the process integration step for Sherpa (this can take some time; should use OpenMPI to speed this up by using multiple cores)
3) run the FastNLO table warmup, which stores files in the "mcgrid" sub-directory
4) run the "Sherpa" command again to start the event generation run, with the #events that you want to fill and create the table with
  ^^^ this last step was parallelized to produce many tables at the same time using job submission (in my case, submitting to the Slurm scheduler on the NEU Discovery cluster)

when the Sherpa event generation run is finished, an output FastNLO table will appear in a subdirectory in the "mcgrid" folder; then you want to follow the instructions given in README_table_analysis.txt to analyze the FastNLO table and produce cross section values

=================================================

 == these are example/template commands to do all these steps from scratch ==

 ==> To start, grab the needed environment and go into the directory corresponding to the W + X jets NLO fixed-order calculation you want to run:
<cd into MakeTablesv3 dir>
source sourceEnvV3.sh
<cd into relevant folder to run Sherpa analysis>

 ==> once in folder, compile the Rivet analysis plugin (which uses MCgrid if filling FastNLO tables) and copy analysis files out to relevant Rivet folders
make plugin-fastnlo && make install

 ==> initialize physics processes listed in Sherpa run card, before integrating using OpenMPI
Sherpa -f Run3j-OL.dat INIT_ONLY=1

 ==> compile libraries if using Amegic in matrix-element calculations (should only be using Comix and OpenLoops, and if so, skip this step)
./makelibs

 ==> integrate processes using OpenMPI (remember to turn off/on the correct switches in the run card to use the dummy virtual switch for process integration --> these switches get flipped back again when doing event generation, see Sherpa manual if confused)
nohup mpirun -n 20 Sherpa -f Run3j-OL.dat -e 0 > 3jprocess-NLO.out 2>&1 &

 ==> Note: if the simulation of multiple parton interactions is allowed/specified in run card, have to do an additional integration run (for the fixed order calculation setup, this should be off)

 ==> run table warmup (only run this once in order to set up the table warmup files that are used in subsequent Sherpa event generation runs)
nohup Sherpa -f Run3j-OL.dat -e 10M -R 4334 -A w3jetsout_RivetAnalysis_warmup > 3j-warmup-10M.out 2>&1 &

 ==> then run Sherpa again with higher number of events to fill tables (run as many times as you want tables; make sure to change the random seed); note: this was previously done on the NEU Discovery cluster by submitting individual jobs to run using the "submitSherpaJobs.py" script)
nohup Sherpa -f Run3j-OL.dat -e 70M -R 4335 -A w3jetsout_RivetAnalysis_70M_1 > 3j-filltables-70M-1.out 2>&1 &

=================================================

NOTE: have to point the Openloops install directory given in the Sherpa run card to the correct folder, i.e. by editing the line --
OL_PREFIX=<home directory>/FastNLOInstallv3/OpenLoops-2.0.0;



 ==> example commands for each fixed order calculation:
NOTE: in my experience, if the warmup table is generated with too few events, when you run Sherpa again to get the individual FastNLO tables, you can get "CheckWeightIsFinite" errors, and for some reason when this happens, it crashes the table and makes it UNREADABLE

if the physics processes specified in the Sherpa run cards are already integrated, can just do the following commands (also don’t have to run the "make" commands again if the Rivet analysis is already compiled and installed):

== W+1j Fixed Order Calculation ==	
cd 1j/CMS_2018_WJetsAlphaS_1j_OL/ 
make plugin-fastnlo && make install
nohup Sherpa -f Run1j-OL.dat -e 10M -R 2 -A w1jetsout_tablewarmup > 1j-warmup-10M.out 2>&1 &
(then would have to run the runcard again to get actual tables, using the number of events you want)

== W+2j Fixed Order Calculation ==
cd 2j/CMS_2018_WJetsAlphaS_2j_OL/
make plugin-fastnlo && make install
nohup Sherpa -f Run2j-OL.dat -e 7M -R 2 -A w2jetsout_tablewarmup > 2j-warmup-7M.out 2>&1 &
(then would have to run the runcard again to get actual tables, using the number of events you want)

== W+3j Fixed Order Calculation ==
cd 3j/CMS_2018_WJetsAlphaS_3j_OL/
make plugin-fastnlo && make install
nohup Sherpa -f Run3j-OL.dat -e 10M -R 2 -A w3jetsout_tablewarmup > 3j-warmup-10M.out 2>&1 &
(then would have to run the runcard again to get actual tables, using the number of events you want)

====================================================================================================

 ==> NOTE!

important FastNLO files stored on lxplus here:
/eos/cms/store/group/phys_smp/AnalysisFramework/Baobab/awisecar/wjetsRun2_forFastNLOAnalysis

directory with all of the tarballs needed for installation:
/eos/cms/store/group/phys_smp/AnalysisFramework/Baobab/awisecar/wjetsRun2_forFastNLOAnalysis/FastNLOInstallv3

final versions of the FastNLO tables used (produced by A. Wisecarver):
/eos/cms/store/group/phys_smp/AnalysisFramework/Baobab/awisecar/wjetsRun2_forFastNLOAnalysis/results_FastNLOtables
 >>> within it we have:
d56-x01-y01.merged.tab.gz  
d57-x01-y01.merged.tab.gz

Labeling of tables --
W+1jet  table for Mu Pt + Leading AK8 Jet Pt --> d56-x01-y01
W+2jets table for Mu Pt + Leading AK8 Jet Pt --> d57-x01-y01
W+3jets table for Mu Pt + Leading AK8 Jet Pt --> d58-x01-y01

