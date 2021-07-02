#! /usr/bin/env python2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import math
import yoda
import argparse
import re
import os

#######################################

parser = argparse.ArgumentParser(description='Plots distributions and computes NP corrections from two Rivet YODA files.')
parser.add_argument('basename',default='d02-x01-y01',help='This is the basename of the table.')
parser.add_argument('yoda0',default='',help='Zeroth YODA file with settings for FNLO table production')
parser.add_argument('yoda1',default='',help='First YODA file with NP=Off')
parser.add_argument('yoda2',default='',help='Second YODA file with NP=On')
parser.add_argument('--yoda3',default='',help='Third YODA file with just MPI On')
parser.add_argument('--out',default='',help='Name of output plot.')

args = parser.parse_args()

yodafile0 = args.yoda0
yodafile1 = args.yoda1
yodafile2 = args.yoda2
if args.yoda3:
    yodafile3 = args.yoda3

## Grabs a Histo1D object (rivet0) that matches the given basename
for key, value in yoda.read(yodafile0).items():
    if re.search(args.basename, key):
        rivet0 = value ##FNLO nominal

for key, value in yoda.read(yodafile1).items():
    if re.search(args.basename, key):
        rivet1 = value ##NP Off

for key, value in yoda.read(yodafile2).items():
    if re.search(args.basename, key):
        rivet2 = value ##NP On

if args.yoda3:
    for key, value in yoda.read(yodafile3).items():
        if re.search(args.basename, key):
            rivet3 = value ##MPI Only

numBins = rivet0.numBins

print "\n--------------> Table: "+str(args.basename)+", Number of bins: "+str(numBins)

if ((str(args.basename) == "d02-x01-y01") or (str(args.basename) == "d03-x01-y01") or (str(args.basename) == "d52-x01-y01") or (str(args.basename) == "d53-x01-y01")):
    xtitle = "Leading Jet pT"
elif ((str(args.basename) == "d06-x01-y01") or (str(args.basename) == "d07-x01-y01") or (str(args.basename) == "d56-x01-y01") or (str(args.basename) == "d57-x01-y01")):
    xtitle = "Muon pT + Leading Jet pT"
elif ((str(args.basename) == "d10-x01-y01") or (str(args.basename) == "d60-x01-y01")):
    xtitle = "HT,2/2"
elif ((str(args.basename) == "d13-x01-y01") or (str(args.basename) == "d63-x01-y01")):
    xtitle = "Muon pT + HT,2/2"
elif ((str(args.basename) == "d16-x01-y01") or (str(args.basename) == "d17-x01-y01") or (str(args.basename) == "d66-x01-y01") or (str(args.basename) == "d67-x01-y01")):
    xtitle = "W pT"
elif ((str(args.basename) == "d20-x01-y01") or (str(args.basename) == "d21-x01-y01") or (str(args.basename) == "d70-x01-y01") or (str(args.basename) == "d71-x01-y01")):
    xtitle = "W pT + Leading Jet pT"
elif ((str(args.basename) == "d24-x01-y01") or (str(args.basename) == "d74-x01-y01")):
    xtitle = "W pT + HT,2/2"

############################################################################################################

binCent_FNLO = []
binWidth_FNLO = []
binEdges_FNLO = []
xs_FNLO = []
xsErr_FNLO = []
percErr_FNLO = []
totXS_FNLO = 0.
for i,b in enumerate(rivet0.bins):
    binCent_FNLO.append(b.xMid)
    binWidth_FNLO.append( (b.xMax-b.xMin) )
    binEdges_FNLO.append(b.xEdges)
    xs_FNLO.append(b.height)
    xsErr_FNLO.append(b.heightErr)
    percErr_FNLO.append( (xsErr_FNLO[i]*100.)/xs_FNLO[i]  )
    totXS_FNLO += binWidth_FNLO[i]*xs_FNLO[i]

print "\n--> for FNLO table filling:"
#print "Bin centers: \n"+str(binCent_FNLO)
print "Diff. xsec values: \n"+str(xs_FNLO)
print "Diff. xsec errs: \n"+str(xsErr_FNLO)
print "Percent error: \n"+str(percErr_FNLO)
#print "Total xsec value: "+str(totXS_FNLO)+" pb ?"

######################################################

binCent_NPOff = []
binWidth_NPOff = []
binEdges_NPOff = []
xs_NPOff = []
xsErr_NPOff = []
percErr_NPOff = []
totXS_NPOff = 0.
for i,b in enumerate(rivet1.bins):
    binCent_NPOff.append(b.xMid)
    binWidth_NPOff.append( (b.xMax-b.xMin) )
    binEdges_NPOff.append(b.xEdges)
    xs_NPOff.append(b.height)
    xsErr_NPOff.append(b.heightErr)
    percErr_NPOff.append( (xsErr_NPOff[i]*100.)/xs_NPOff[i] )
    totXS_NPOff += binWidth_NPOff[i]*xs_NPOff[i]

print "\n--> NP Off:"
#print "Bin centers: \n"+str(binCent_NPOff)
print "Diff. xsec values: \n"+str(xs_NPOff)
print "Diff. xsec errs: \n"+str(xsErr_NPOff)
print "Percent error: \n"+str(percErr_NPOff)
#print "Total xsec value: "+str(totXS_NPOff)+" pb ?" 

######################################################

binCent_NPOn = []
binWidth_NPOn = []
binEdges_NPOn = []
xs_NPOn = []
xsErr_NPOn = []
percErr_NPOn = []
totXS_NPOn = 0.
for i,b in enumerate(rivet2.bins):
    binCent_NPOn.append(b.xMid)
    binWidth_NPOn.append( (b.xMax-b.xMin) )
    binEdges_NPOn.append(b.xEdges)
    xs_NPOn.append(b.height)
    xsErr_NPOn.append(b.heightErr)
    percErr_NPOn.append( (xsErr_NPOn[i]*100.)/xs_NPOn[i] )
    totXS_NPOn += binWidth_NPOn[i]*xs_NPOn[i]

print "\n--> NP On:"
#print "Bin centers: \n"+str(binCent_NPOn)
print "Diff. xsec values: \n"+str(xs_NPOn)
print "Diff. xsec errs: \n"+str(xsErr_NPOn)
print "Percent error: \n"+str(percErr_NPOn)
#print "Total xsec value: "+str(totXS_NPOn)+" pb ?"

######################################################
if args.yoda3:
    binCent_MPI = []
    binWidth_MPI = []
    binEdges_MPI = []
    xs_MPI = []
    xsErr_MPI = []
    percErr_MPI = []
    totXS_MPI = 0.
    for i,b in enumerate(rivet3.bins):
        binCent_MPI.append(b.xMid)
        binWidth_MPI.append( (b.xMax-b.xMin) )
        binEdges_MPI.append(b.xEdges)
        xs_MPI.append(b.height)
        xsErr_MPI.append(b.heightErr)
        percErr_MPI.append( (xsErr_MPI[i]*100.)/xs_MPI[i] )
        totXS_MPI += binWidth_MPI[i]*xs_MPI[i]
    
    print "\n--> MPI Only:"
    #print "Bin centers: \n"+str(binCent_MPI)
    print "Diff. xsec values: \n"+str(xs_MPI)
    print "Diff. xsec errs: \n"+str(xsErr_MPI)
    print "Percent error: \n"+str(percErr_MPI)
    #print "Total xsec value: "+str(totXS_MPI)+" pb ?"

############################################################################################################
## Analysis and plotting

corrNP = []
corrNPerrs = []
corrNPpercErrs = []
for i,b in enumerate(xs_NPOn):
    corrNP.append( xs_NPOn[i]/xs_NPOff[i] )
    corrNPerrs.append( corrNP[i] * math.sqrt( (xsErr_NPOn[i]/xs_NPOn[i])**2. + (xsErr_NPOff[i]/xs_NPOff[i])**2. )  )
    corrNPpercErrs.append(corrNPerrs[i]*100./corrNP[i])

print "\n"
print "--> NP_On/NP_Off for "+str(args.basename)+": \n"+str(corrNP)
print "corrNP errors: \n"+str(corrNPerrs)
print "Percent errors: \n"+str(corrNPpercErrs)
#print "Bin centers: \n"+str(binCent_NPOn)
#print "Bin edges: \n"+str(binEdges_NPOn)


##

PSeffect = []
PSeffecterrs = []
PSeffectpercErrs = []
for i,b in enumerate(xs_NPOff):
    PSeffect.append( xs_NPOff[i]/xs_FNLO[i] )
    PSeffecterrs.append( PSeffect[i] * math.sqrt( (xsErr_NPOff[i]/xs_NPOff[i])**2. + (xsErr_FNLO[i]/xs_FNLO[i])**2. )  )
    PSeffectpercErrs.append(PSeffecterrs[i]*100./PSeffect[i])

print "\n"
print "--> PS_On/PS_Off for "+str(args.basename)+": \n"+str(PSeffect)
print "PS effect errors: \n"+str(PSeffecterrs)
print "Percent errors: \n"+str(PSeffectpercErrs)

##

xErr = [(b/2.) for b in binWidth_NPOn]
if args.yoda3:
    yMax = max( max(xs_FNLO), max(xs_NPOff), max(xs_NPOn), max(xs_MPI) )
    yMin = min( min(xs_FNLO), min(xs_NPOff), min(xs_NPOn), min(xs_MPI) )
else:
    yMax = max( max(xs_FNLO), max(xs_NPOff), max(xs_NPOn) )
    yMin = min( min(xs_FNLO), min(xs_NPOff), min(xs_NPOn) )

##################
## NP Corr Plot

fig, ax = plt.subplots(figsize=(10, 6))
ax.set(xlabel=xtitle+' [GeV]', ylabel='On/Off', title='Non-Pert. Corrections for '+str(args.basename))

ax.yaxis.label.set_size(18)
ax.set(ylim=[0.5,1.5])
#ax.set(ylim=[0.5,2.5])
ax.axhline(y=1, linewidth=1, color='k', linestyle='--')

ax.errorbar(binCent_NPOn, corrNP, xerr=xErr, yerr=corrNPerrs, fmt='ko', capthick=1.5) #y-errors included
#ax.errorbar(binCent_NPOn, corrNP, xerr=xErr, yerr=None, fmt='ko', capthick=1.5) #no y-errors
ax.set_xlim(binCent_NPOn[0]-xErr[0]-10., binCent_NPOn[numBins-1]+xErr[numBins-1]+10.)

if args.out:
    out = args.out
else:
    out = args.basename+'_NPcorr.pdf'
fig.savefig(out)

##################
## PS Effect Plot

fig, ax = plt.subplots(figsize=(10, 6))
ax.set(xlabel=xtitle+' [GeV]', ylabel='On/Off', title='PS Effect for '+str(args.basename))

ax.yaxis.label.set_size(18)
ax.set(ylim=[0.5,1.5])
#ax.set(ylim=[0.5,2.5])
ax.axhline(y=1, linewidth=1, color='k', linestyle='--')

#ax.errorbar(binCent_NPOff, PSeffect, xerr=xErr, yerr=PSeffecterrs, fmt='ko', capthick=1.5) #y-errors included
ax.errorbar(binCent_NPOff, PSeffect, xerr=xErr, yerr=None, fmt='ko', capthick=1.5) #no y-errors

ax.set_xlim(binCent_NPOff[0]-xErr[0]-10., binCent_NPOff[numBins-1]+xErr[numBins-1]+10.)

if args.out:
    out = args.out
else:
    out = args.basename+'_PSeffect.pdf'
fig.savefig(out)

##################
## Plot all xsec distributions

figComp, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 8), gridspec_kw = {'height_ratios':[3, 1]})

#y-errors included -----
#ax1.errorbar(binCent_FNLO, xs_FNLO, xerr=xErr, yerr=xsErr_FNLO, fmt='ko', ecolor='k', capthick=1.5, label='NLO FO')
ax1.errorbar(binCent_FNLO, xs_FNLO, xerr=xErr, yerr=None, fmt='ko', ecolor='k', capthick=1.5, label='NLO FO') ## no errors
ax1.errorbar(binCent_NPOff, xs_NPOff, xerr=xErr, yerr=xsErr_NPOff, fmt='bo', ecolor='b', capthick=1.5, label='NLO+PS')
if args.yoda3:
    ax1.errorbar(binCent_MPI, xs_MPI, xerr=xErr, yerr=xsErr_MPI, fmt='go', ecolor='g',capthick=1.5, label='MPI On')
ax1.errorbar(binCent_NPOn, xs_NPOn, xerr=xErr, yerr=xsErr_NPOn, fmt='ro', ecolor='r',capthick=1.5, label='MPI+HAD+BBR On')
#no y-errors -----
##ax1.errorbar(binCent_FNLO, xs_FNLO, xerr=xErr, yerr=None, fmt='ko', ecolor='k', capthick=1.5, label='NLO')
##ax1.errorbar(binCent_NPOff, xs_NPOff, xerr=xErr, yerr=None, fmt='bo', ecolor='b', capthick=1.5, label='NLO+PS')
##if args.yoda3:
##    ax1.errorbar(binCent_MPI, xs_MPI, xerr=xErr, yerr=None, fmt='go', ecolor='g',capthick=1.5, label='MPI On')
##ax1.errorbar(binCent_NPOn, xs_NPOn, xerr=xErr, yerr=None, fmt='ro', ecolor='r',capthick=1.5, label='MPI+HAD+BBR On')

ax1.legend(loc='lower left', bbox_to_anchor=(0.415, 0.785, 0, 0))
ax1.set_yscale('log')
ax1.set_ylabel(r'd$\sigma$/d$p_{T}$')
ax1.set_xlim(binCent_NPOn[0]-xErr[0]-10., binCent_NPOn[numBins-1]+xErr[numBins-1]+10.)
ax1.set_ylim(yMin-abs(yMin*0.5), yMax+abs(yMax*0.5))

# Now do the ratio subplot
dummy1 = []
dummy2 = []
if args.yoda3:
    dummy3 = []

# Take ratio wrt FNLO nominal
for i,b in enumerate(xs_NPOn):
    dummy1.append( xs_NPOff[i]/xs_FNLO[i] )
    dummy2.append( xs_NPOn[i]/xs_FNLO[i] )
    if args.yoda3:
        dummy3.append( xs_MPI[i]/xs_FNLO[i] )

ax2.errorbar( binCent_NPOff, dummy1, xerr=xErr, yerr=None, fmt='bo', ecolor='b', capthick=1.5, label='NLO+PS' )
if args.yoda3:
    ax2.errorbar( binCent_MPI, dummy3, xerr=xErr, yerr=None, fmt='go', ecolor='g', capthick=1.5, label='MPI On' )
ax2.errorbar( binCent_NPOn, dummy2, xerr=xErr, yerr=None, fmt='ro', ecolor='r', capthick=1.5, label='MPI+HAD+BBR On' )
ax2.axhline(y=1, linewidth=1, linestyle='--', color='k')
ax2.set_ybound(0.5, 1.50)
#ax2.set_ybound(0., 2.0)
ax2.set_ylabel('Ratio to NLO FO')
ax2.set_xlabel(xtitle+' [GeV]')
ax2.xaxis.set_label_coords(0.75, -0.21)

figComp.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in figComp.axes[:-1]], visible=False)

if args.out:
    out = args.out
else:
    out = args.basename+'_xsecs.pdf'
figComp.savefig(out)


#####

#print("\n----->")
#print("NPoff/FNLO:")
#print(str(dummy1))
#print("NPon/FNLO:")
#print(str(dummy2))
#print("NPon/NPoff:")
#print(str(corrNP))

print ("\nFinished!")
