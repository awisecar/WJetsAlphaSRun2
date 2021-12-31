#! /usr/bin/env python
import os
import sys
import random
import time
import datetime
import argparse
######################

# NOTE: This script is designed to submit jobs running the Sherpa event generator 
# using the Slurm scheduler on the NEU Discovery cluster
# Currently, the maximum walltime limit for submitted jobs is 24 hours
# and the default memory per core is 1Gb, so have to calculate the number
# of events I can run for each kind of processes within this maximum 24 hour window

# For official documentation on the Discovery cluster from Northeastern Research Computing, see:
# https://rc.northeastern.edu/support/documentation/

# Example for running script to submit jobs:
# ./submitSherpaJobs.py 10 50 
# ./submitSherpaJobs.py 20 150 

######################

# Parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument("process", help="Physics process to submit: W+1J = 10, W+2J = 20; W+3J = 30; add 1 for PS, or add 2 for PS+NP", type=int)
parser.add_argument("numJobs", help="Number of jobs to submit to scheduler", type=int)
args = parser.parse_args()

###########################################

###########################################
#                                         #
#  --- Select the analysis to run!!! ---  #
#                                         #
###########################################

### =======> testing
if (args.process == 0):
    #numJobs = 1
    numEvents = "100000"
    memRequest = "3G"
    runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/19-11-11/1j/CMS_2018_WJetsAlphaS_1j_OL/'
    runCardName = 'Run1j-OL.dat'
    yodaOutRoot = 'w1jetsFO_TEST_100K_'

### --------------------------------------
### ----------- W+1J Processes -----------
### --------------------------------------
# Fixed order (FastNLO tables)
elif (args.process == 10):
    #numEvents = "45M" # works well
    #numEvents = "85M" # too high
    #numEvents = "55M" # some jobs failed
    #numEvents = "52M" # works efficiently, FOR ANALYSIS
    #numEvents = "35M" # temporary, using to speed things up
    numEvents = "17M" # temporary, using to speed things up
    #numEvents = "10M" # FOR TABLE WARMUP
    memRequest = "1G"
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/20-11-11/1j/CMS_2018_WJetsAlphaS_1j_OL/'
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/20-12-15/1j/CMS_2018_WJetsAlphaS_1j_OL/'
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_03_13/1j/CMS_2018_WJetsAlphaS_1j_OL/'
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_04_21/1j/CMS_2018_WJetsAlphaS_1j_OL/'

    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_07_19/1j_AndrewEdit/1j/CMS_2018_WJetsAlphaS_1j_OL/' # 1j_AndrewEdit
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_07_19/1j_JoonBinEdit/1j/CMS_2018_WJetsAlphaS_1j_OL/' # 1j_JoonBinEdit
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_07_19/1j_5flavorCheck/1j/CMS_2018_WJetsAlphaS_1j_OL/' # 1j_5flavorCheck
    runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_07_19/1j_5flavorCheck_take2/1j/CMS_2018_WJetsAlphaS_1j_OL/' # 1j_5flavorCheck_take2

    runCardName = 'Run1j-OL.dat'
    yodaOutRoot = 'w1jetsFO_'+str(numEvents)+'_'
# Fixed order + Parton shower
elif (args.process == 11):
    sys.exit("\nOption not yet implemented... Exiting.\n")
# Fixed order + Parton shower + NP effects
elif (args.process == 12):
    sys.exit("\nOption not yet implemented... Exiting.\n")

### --------------------------------------
### ----------- W+2J Processes -----------
### --------------------------------------
# Fixed order (FastNLO tables)
elif (args.process == 20):

    #numEvents = "25M" # too high
    #numEvents = "17M" # works well
    #numEvents = "14M" # works well, safer than 17M, FOR ANALYSIS (nominal)
    #numEvents = "7M" # FOR TABLE WARMUP
    numEvents = "10M" # temporary, to speed things up...

    memRequest = "1G"

    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/20-11-11/2j/CMS_2018_WJetsAlphaS_2j_OL/'
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/20-12-15/2j/CMS_2018_WJetsAlphaS_2j_OL/'
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_03_13/2j/CMS_2018_WJetsAlphaS_2j_OL/'
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_04_21/2j/CMS_2018_WJetsAlphaS_2j_OL/'
    runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_07_19/2j_JoonBinEdit/2j/CMS_2018_WJetsAlphaS_2j_OL/'

    runCardName = 'Run2j-OL.dat'
    yodaOutRoot = 'w2jetsFO_'+str(numEvents)+'_'
# Fixed order + Parton shower
elif (args.process == 21):
    sys.exit("\nOption not yet implemented... Exiting.\n")
# Fixed order + Parton shower + NP effects
elif (args.process == 22):
    sys.exit("\nOption not yet implemented... Exiting.\n")

### --------------------------------------
### ----------- W+3J Processes -----------
### --------------------------------------
# Fixed order (FastNLO tables)
elif (args.process == 30):
    numEvents = 1900000 # 1.9M events, works well
    #numEvents = "2M" # try this
    memRequest = "3G"
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/20-11-11/3j/CMS_2018_WJetsAlphaS_3j_OL/'
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/20-12-15/3j/CMS_2018_WJetsAlphaS_3j_OL/'
    #runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_04_21/3j/CMS_2018_WJetsAlphaS_3j_OL/'
    runCardLocation = '/home/wisecarver.a/MakeTablesv3/openloops/21_07_19/3j_JoonBinEdit/3j/CMS_2018_WJetsAlphaS_3j_OL/'
    runCardName = 'Run3j-OL.dat'
    yodaOutRoot = 'w3jetsFO_'+str(numEvents)+'_'
# Fixed order + Parton shower
elif (args.process == 31):
    sys.exit("\nOption not yet implemented... Exiting.\n")
# Fixed order + Parton shower + NP effects
elif (args.process == 32):
    sys.exit("\nOption not yet implemented... Exiting.\n")

### --------------------------------------

else:
    sys.exit("\nPlease select proper index for a physics process!\n")

### --------------------------------------

print("\n===> Requesting "+str(args.numJobs)+" jobs for process "+str(args.process))
print("===> Each job is for "+str(numEvents)+" events and will request "+str(memRequest)+" of memory")

###########################################

print("\nBegin submissions script!")

cwd = os.getcwd()
print('Current working directory: '+cwd)

dateTo = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
# NOTE: could add the runCardLocation to where the folder of job scripts goes?
mtmpdir = 'jobs_' + dateTo + '/'
os.system('mkdir -p ' + mtmpdir)
#os.system('mkdir -p ' + runCardLocation + mtmpdir)

# Set the seed for the random number generator
# These random numbers are then used as random seeds for Sherpa commands
random.seed(1025)

print('\n=============================================\n')

###########################################

for i in range(1, args.numJobs+1):

    # --- Assemble Sherpa command to run ---
    # Example Sherpa command:
    # Sherpa -f Run1j-OL.dat -e 1000 -R 4331 -A w1jetsout_RivetAnalysis_50M_1 > 1j-filltables-50M-1.out 2>&1

    randomSeed = random.randint(1, 10000000)
    yodaOutName = yodaOutRoot
    yodaOutName += str(i)

    sherpaCmd  = 'Sherpa -f '
    sherpaCmd += str(runCardName)
    sherpaCmd += ' -e '
    sherpaCmd += str(numEvents)
    sherpaCmd += ' -R '
    sherpaCmd += str(randomSeed)
    sherpaCmd += ' -A '
    sherpaCmd += str(yodaOutName)
    sherpaCmd += ' 2>&1'

    # print(sherpaCmd)

    # --- Assemble Slurm submission script ---
    # --- 1) Job submission specifications
    submit  = '#!/bin/bash\n'
    submit += '#SBATCH --nodes=1\n'
    if (args.process == 0):
        submit += '#SBATCH --time=00:30:00\n' #for testing
    else:
        submit += '#SBATCH --time=23:59:59\n' #for regular jobs
        #submit += '#SBATCH --time=08:59:59\n' # TEMP
    submit += '#SBATCH --job-name=sherpa_process'+str(args.process)+'_job'+str(i)+'\n'
    if (args.process == 0):
        submit += '#SBATCH --partition=express\n'
    else:
        submit += '#SBATCH --partition=short\n'
    submit += '#SBATCH --mem='+str(memRequest)+'\n'
    submit += '#SBATCH --output='+mtmpdir+'sherpa_process'+str(args.process)+'_job'+str(i)+'.out\n\n'
    #submit += '#SBATCH --error=sherpa_process'+str(args.process)+'_job'+str(i)+'.err\n\n'
    # --- 2) Commands to execute
    submit += 'printf "'+str(r'\n')+'Hello %s, your job is on host: $(hostname)" "$USER"\n'
    submit += 'cd '+str(runCardLocation)+'\n'
    submit += 'printf "'+str(r'\n')+'Directory: $(pwd)'+str(r'\n')+'"\n'
    submit += 'ls -latr\n'
    submit += 'printf "'+str(r'\n')+'"\n'
    submit += 'source /home/wisecarver.a/MakeTablesv3/sourceEnvV3.sh\n'
    submit += sherpaCmd + '\n'
    # --- 3) Write commands into shell script
    submitName = mtmpdir+'sherpa_process'+str(args.process)+'_job'+str(i)+'.sh'
    subScript = open(submitName,'w')
    subScript.write(submit+'\n')
    subScript.close()
    os.system('chmod 744 '+submitName)

    # --- Submit job to scheduler! ---
    print('Submitting Sherpa command #'+str(i)+':\n'+str(sherpaCmd)+'\n')
    os.system('sbatch '+str(submitName)) 

print('=============================================')

print('\nQuerying job submissions...')
#os.system('squeue | grep wisecarv')
os.system('squeue -u wisecarver.a')

print("\nFinished!\n")

