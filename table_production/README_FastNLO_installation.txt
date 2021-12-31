
*** FastNLO Installation Procedure ***


NOTE:
for all of the main results, we use the setup in FastNLOInstallv3
the setup in FastNLOInstallv2 has been used before to get updated packages needed for some of the analysis scripts I’ve written (see README_table_analysis.txt)
there are only a few differences in package versions between these two installs: see the note down below.


 ==> FastNLO install instructions:

to begin, in the home directory space, do --
mkdir localv3
 
need to also set up these CMSSW versions in home directory (by using the "cmsrel" command) --
CMSSW_7_1_30
CMSSW_10_0_0

then, before running install command, set up needed environment in your ".bash_profile" by putting in the following section (note: this is the set up on the NEU Tier3, i.e. lhct3alv.neu.edu, but the point is to get the correct compiler and Python versions)--

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# set up environment to access CMSSW on NEU Tier3
SCRAM_ARCH=slc6_amd64_gcc481
export SCRAM_ARCH
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch 
source $VO_CMS_SW_DIR/cmsset_default.sh 

#set gcc 4.8.1 as default compiler
source /cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/gcc/4.8.1/etc/profile.d/init.sh

#set python 2.7 for Rivet executables
PYTHONDIR=/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.3
PATH=$PYTHONDIR/bin:$PATH
LD_LIBRARY_PATH=$PYTHONDIR/lib:$LD_LIBRARY_PATH

#set LHAPDF path
LHAPDF_DATA_PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/lhapdf/6.2.1/share/LHAPDF

###### note: can try new environment for v2 installation (motivated by getting newer version of python)
#SCRAM_ARCH=slc6_amd64_gcc493
#export SCRAM_ARCH
#export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
#source $VO_CMS_SW_DIR/cmsset_default.sh
#source /cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/gcc/4.9.3/etc/profile.d/init.sh
#PYTHONDIR=/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/python/2.7.11
#PATH=$PYTHONDIR/bin:$PATH
#LD_LIBRARY_PATH=$PYTHONDIR/lib:$LD_LIBRARY_PATH
#LHAPDF_DATA_PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/lhapdf/6.1.6/share/LHAPDF

export PATH
export LD_LIBRARY_PATH
export PYTHONDIR
export LHAPDF_DATA_PATH
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

next, in the home directory, set up a "FastNLOInstallv3" directory where the installation tarballs and installation script will live --
mkdir FastNLOInstallv3
cd FastNLOInstallv3

then get the tarballs for all of the different software packages --

 >>> tarballs should be available/kept in the SMP EOS space on lxplus in the directory:
/eos/cms/store/group/phys_smp/AnalysisFramework/Baobab/awisecar/wjetsRun2_forFastNLOAnalysis/FastNLOInstallv3

 >>> or, if they are not there, then can possibly still grab tarballs w/ FNLO and all dependencies (Rivet, MCgrid, etc.) from Klaus’ KIT directories via:
wget http://ekpwww.etp.kit.edu/~rabbertz/fnlov2-Test/INSTALL/fnlosrc_install_no-ROOT_201801.tar.gz --progress=bar --user=fnlouser --password=fn@ETP+05
wget http://ekpwww.etp.kit.edu/~rabbertz/fnlov2-Test/INSTALL/fnlosrc_install_201801.csh --progress=bar --user=fnlouser --password=fn@ETP+05
wget http://ekpwww.etp.kit.edu/~rabbertz/fnlov2-Test/INSTALL/root-5.34.26-patched.tar.gz --progress=bar --user=fnlouser --password=fn@ETP+05

 >>> if getting from KIT directory, then would do this to get all of the individual packages:
tar -xvzf fnlosrc_install_no-ROOT_201801.tar.gz
(would then turn off ROOT option and set "ncores" option in install csh script, set them to 0 and 1 respectively)

if using lxplus, install swig in your local folder -- 
tar -xvzf swig-3.0.12.tar.gz
./configure --prefix=/afs/cern.ch/work/a/awisecar/localv3
make 
make install

next, in the FastNLOInstallv3 directory, run the installation command --
 > (would need to change the home directory argument to point to where your home directory is on your machine)
 > (can set a "_" if not using option, also can change the number of cores used inside the script)
./fnlosrc_install_201902.csh <home_directory> localv3 _ 1 0 1 1

upon finishing the installation, this will produce a "fnlo_source.sh" script that is used to set up the environment whenever you want to run any of the packages (i.e. Sherpa, Rivet, etc.)
need to add this to the source script to be able to grab the PDF sets (?) --
 > export LHAPDF_DATA_PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/lhapdf/6.2.1/share/LHAPDF 
then copy the environment shell script setup file to ~/MakeTablesv3 as "sourceEnvV3.sh"

NOTE: all of the Sherpa run cards, Rivet analysis files, i.e. the whole setup was kept in a "MakeTablesv3" folder in the home directory (just for organizational purposes)

>>>>>>>>>>>>>> NOTE >>>>>>>>>>>>>>>>>>>
if you have the packages downloaded already, and the bash_profile is already set up, you can just do (after creating a localv3 directory) --

source /cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/gcc/4.8.1/etc/profile.d/init.sh

tar -xvzf swig-3.0.12.tar.gz
cd swig-3.0.12
./configure --prefix=<home_directory>/localv3
make 
make install
cd ..

./fnlosrc_install_201902.csh <home_directory> localv3 _ 1 0 1 1
^^^ can set the number of cores inside the install script

NOTE: will possibly have to do a workaround to install OpenLoops v2 (see below)
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


 ==> workaround to install OpenLoops v2 (specifically the process libraries?):

NOTE: 
upon first trying to install OpenLoops v2 on my machine, there were some problems, due to the lack of Python3 version needed (?)
if this does not apply to you and the Sherpa executable/commands run okay, then don’t worry (it may just install Openloops2 and then finish installing Sherpa and MCgrid and finish just fine, but may need to install the necessary Openloops process libraries and then re-install Sherpa and MCgrid again to finish the entire process)

===========================
notes for this workaround:

***try installing both sherpa and openloops with the compilers and python version found in CMSSW_10_4_0
- cmsenv’d and then resourced the old compiler (v4.8.1)
- for some reason the python setup in cmssw makes openloops happy
- openloops works so far
- then tried to install sherpa and it failed because it was picking up the MPI version from cmssw
- so then I logged in to my account again to pick the original default environment back up
- if sherpa installs then hopefully everything is fine because everything was installed with the same gcc/g++/gfortran versions
- sherpa installed and then just tried to initialize my run card and everything went fine!

===========================

so once openloops2 is installed, run this command to install the relevant process libraries for W+jets:
./openloops libinstall ppllj ppllj_ew ppllj_nf5 pplnj_ckm pplnjj pplnjj_ckm pplnjj_ew pplnjjj


========================================================================================================================

*** Additional Notes ***


 ==> difference in packages b/t FastNLOInstallv2 and FastNLOInstallv3 installs?

v2 has --
fastnlo_interface_nlojet-2.3.1pre-2657
fastnlo_toolkit-2.3.1-2657
hoppet-1.2.0 
<no swig here?>

v3 has --
fastnlo_interface_nlojet-2.3.1pre-2424
fastnlo_toolkit-2.3.1pre-2441
hoppet-1.1.5 
swig-3.0.12


 ==> installation of additional PDF sets for use when reading FastNLO tables to obtain cross sections:

the files for additional PDF sets can be downloaded from the official LHAPDF website (can use the "wget" command)
then unzip/untar the file, e.g.
tar -zxvf FILE_NAME.tar.gz
and put the files in:
<home directory>/localv3/share/LHAPDF

then set:
export LHAPDF_DATA_PATH=<home directory>/localv3/share/LHAPDF:$LHAPDF_DATA_PATH

PDF sets used before include (names here specify use of the default central alpha-s value):
CT14nlo, CT18nlo, NNPDF30_nlo, NNPDF31_nlo, HERAPDF20_NLO, ABMP16_5_nlo, MSHT20nlo_as118

so then to do the alpha-s variations, grab the following sets (XXX means the different alpha-s values):
CT14nlo_as_0XXX, CT18NLO_as_0XXX, NNPDF30_nlo_as_0XXX, NNPDF31_nlo_as_0XXX, HERAPDF20_NLO_ALPHAS_XXX, ABMP16alsXXX_5_nlo, MSHT20nlo_as_smallrange / MSHT20nlo_as_largerange (different alpha-s values are the different PDF members of this one)
- to get the "MSHT20nlo_as_largerange" set do:
- wget http://www.hep.ucl.ac.uk/msht/Grids/MSHT20nlo_as_largerange.tar.gz

