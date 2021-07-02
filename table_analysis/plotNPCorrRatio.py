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

parser = argparse.ArgumentParser(description='Takes ratios of NLO, NLO+PS, and NLO+PS+MPI+BBR+HAD')
parser.add_argument('tableNUM',default='d03-x01-y01',help='Name of table for NUMERATOR')
parser.add_argument('tableDENOM',default='d02-x01-y01',help='Name of table for DENOMINATOR')
parser.add_argument('yoda0NUM',default='',help='NLO table for NUM')
parser.add_argument('yoda1NUM',default='',help='NLO+PS table for NUM')
parser.add_argument('yoda2NUM',default='',help='NLO+PS+MPI+BBR+HAD for NUM')
parser.add_argument('yoda0DENOM',default='',help='NLO table for DENOM')
parser.add_argument('yoda1DENOM',default='',help='NLO+PS table for DENOM')
parser.add_argument('yoda2DENOM',default='',help='NLO+PS+MPI+BBR+HAD for DENOM')
parser.add_argument('--out',default='',help='Name of output plot.')
args = parser.parse_args()

yodafile0NUM = args.yoda0NUM
yodafile1NUM = args.yoda1NUM
yodafile2NUM = args.yoda2NUM
yodafile0DENOM = args.yoda0DENOM
yodafile1DENOM = args.yoda1DENOM
yodafile2DENOM = args.yoda2DENOM

## Grabs a Histo1D object (e.g. rivet0NUM) that matches the given Rivet tablename
for key, value in yoda.read(yodafile0NUM).items():
    if re.search(args.tableNUM, key):
        rivet0NUM = value
for key, value in yoda.read(yodafile1NUM).items():
    if re.search(args.tableNUM, key):
        rivet1NUM = value
for key, value in yoda.read(yodafile2NUM).items():
    if re.search(args.tableNUM, key):
        rivet2NUM = value
for key, value in yoda.read(yodafile0DENOM).items():
    if re.search(args.tableDENOM, key):
        rivet0DENOM = value
for key, value in yoda.read(yodafile1DENOM).items():
    if re.search(args.tableDENOM, key):
        rivet1DENOM = value
for key, value in yoda.read(yodafile2DENOM).items():
    if re.search(args.tableDENOM, key):
        rivet2DENOM = value

numBins = rivet0NUM.numBins

print "\n--------------> Num: "+str(args.tableNUM)
print "------------> Denom: "+str(args.tableDENOM)
print "Number of bins: "+str(numBins)
print "\n"

xtitle = "pT spectrum [GeV]"
if (((str(args.tableDENOM) == "d02-x01-y01") and (str(args.tableNUM) == "d03-x01-y01")) or ((str(args.tableDENOM) == "d52-x01-y01") and (str(args.tableNUM) == "d53-x01-y01"))):
    xtitle = "Leading Jet pT"
elif (((str(args.tableDENOM) == "d06-x01-y01") and (str(args.tableNUM) == "d07-x01-y01")) or ((str(args.tableDENOM) == "d56-x01-y01") and (str(args.tableNUM) == "d57-x01-y01"))):
    xtitle = "Muon pT + Leading Jet pT"
elif (((str(args.tableDENOM) == "d16-x01-y01") and (str(args.tableNUM) == "d17-x01-y01")) or ((str(args.tableDENOM) == "d66-x01-y01") and (str(args.tableNUM) == "d67-x01-y01"))):
    xtitle = "W pT"
elif (((str(args.tableDENOM) == "d20-x01-y01") and (str(args.tableNUM) == "d21-x01-y01")) or ((str(args.tableDENOM) == "d70-x01-y01") and (str(args.tableNUM) == "d71-x01-y01"))):
    xtitle = "W pT + Leading Jet pT"

############################################################################################################

#NUM data
binCent_0NUM = []
binWidth_0NUM = []
xs_0NUM = []
xsErr_0NUM = []
percErr_0NUM = []
for i,b in enumerate(rivet0NUM.bins):
    binCent_0NUM.append(b.xMid)
    binWidth_0NUM.append(b.xMax-b.xMin)
    xs_0NUM.append(b.height)
    xsErr_0NUM.append(b.heightErr)
    percErr_0NUM.append((xsErr_0NUM[i]*100.)/xs_0NUM[i])

binCent_1NUM = []
binWidth_1NUM = []
xs_1NUM = []
xsErr_1NUM = []
percErr_1NUM = []
for i,b in enumerate(rivet1NUM.bins):
    binCent_1NUM.append(b.xMid)
    binWidth_1NUM.append(b.xMax-b.xMin)
    xs_1NUM.append(b.height)
    xsErr_1NUM.append(b.heightErr)
    percErr_1NUM.append((xsErr_1NUM[i]*100.)/xs_1NUM[i])

binCent_2NUM = []
binWidth_2NUM = []
xs_2NUM = []
xsErr_2NUM = []
percErr_2NUM = []
for i,b in enumerate(rivet2NUM.bins):
    binCent_2NUM.append(b.xMid)
    binWidth_2NUM.append(b.xMax-b.xMin)
    xs_2NUM.append(b.height)
    xsErr_2NUM.append(b.heightErr)
    percErr_2NUM.append((xsErr_2NUM[i]*100.)/xs_2NUM[i])

#DENOM data
binCent_0DENOM = []
binWidth_0DENOM = []
xs_0DENOM = []
xsErr_0DENOM = []
percErr_0DENOM = []
for i,b in enumerate(rivet0DENOM.bins):
    binCent_0DENOM.append(b.xMid)
    binWidth_0DENOM.append(b.xMax-b.xMin)
    xs_0DENOM.append(b.height)
    xsErr_0DENOM.append(b.heightErr)
    percErr_0DENOM.append((xsErr_0DENOM[i]*100.)/xs_0DENOM[i])

binCent_1DENOM = []
binWidth_1DENOM = []
xs_1DENOM = []
xsErr_1DENOM = []
percErr_1DENOM = []
for i,b in enumerate(rivet1DENOM.bins):
    binCent_1DENOM.append(b.xMid)
    binWidth_1DENOM.append(b.xMax-b.xMin)
    xs_1DENOM.append(b.height)
    xsErr_1DENOM.append(b.heightErr)
    percErr_1DENOM.append((xsErr_1DENOM[i]*100.)/xs_1DENOM[i])

binCent_2DENOM = []
binWidth_2DENOM = []
xs_2DENOM = []
xsErr_2DENOM = []
percErr_2DENOM = []
for i,b in enumerate(rivet2DENOM.bins):
    binCent_2DENOM.append(b.xMid)
    binWidth_2DENOM.append(b.xMax-b.xMin)
    xs_2DENOM.append(b.height)
    xsErr_2DENOM.append(b.heightErr)
    percErr_2DENOM.append((xsErr_2DENOM[i]*100.)/xs_2DENOM[i])

print "------------------------------------------------------------------------------------------------------"
print "\n\n-----> NUMERATOR NLO:"
print "Diff. xsec values: \n"+str(xs_0NUM)
print "Diff. xsec errs: \n"+str(xsErr_0NUM)
print "Percent error: \n"+str(percErr_0NUM)
print "\n-----> NUMERATOR NLO+PS:"
print "Diff. xsec values: \n"+str(xs_1NUM)
print "Diff. xsec errs: \n"+str(xsErr_1NUM)
print "Percent error: \n"+str(percErr_1NUM)
print "\n-----> NUMERATOR NLO+PS+MPI+BBR+HAD:"
print "Diff. xsec values: \n"+str(xs_2NUM)
print "Diff. xsec errs: \n"+str(xsErr_2NUM)
print "Percent error: \n"+str(percErr_2NUM)
print "\n-----> DENOMINATOR NLO:"
print "Diff. xsec values: \n"+str(xs_0DENOM)
print "Diff. xsec errs: \n"+str(xsErr_0DENOM)
print "Percent error: \n"+str(percErr_0DENOM)
print "\n-----> DENOMINATOR NLO+PS:"
print "Diff. xsec values: \n"+str(xs_1DENOM)
print "Diff. xsec errs: \n"+str(xsErr_1DENOM)
print "Percent error: \n"+str(percErr_1DENOM)
print "\n-----> DENOMINATOR NLO+PS+MPI+BBR+HAD:"
print "Diff. xsec values: \n"+str(xs_2DENOM)
print "Diff. xsec errs: \n"+str(xsErr_2DENOM)
print "Percent error: \n"+str(percErr_2DENOM)
print "\n"

############################################################################################################
## Analysis

ratio_NLO = []
ratioErr_NLO = []
percErr_NLO = []
ratio_NLOPS = []
ratioErr_NLOPS = []
percErr_NLOPS = []
ratio_NLOPSMPIBBRHAD = []
ratioErr_NLOPSMPIBBRHAD = []
percErr_NLOPSMPIBBRHAD = []

#Take ratios
for i,b in enumerate(xs_0NUM):
    ratio_NLO.append(xs_0NUM[i]/xs_0DENOM[i])
    ratioErr_NLO.append(ratio_NLO[i]*math.sqrt( (xsErr_0NUM[i]/xs_0NUM[i])**2. + (xsErr_0DENOM[i]/xs_0DENOM[i])**2. ))
    percErr_NLO.append((ratioErr_NLO[i]*100.)/ratio_NLO[i])
    ratio_NLOPS.append(xs_1NUM[i]/xs_1DENOM[i])
    ratioErr_NLOPS.append(ratio_NLOPS[i]*math.sqrt( (xsErr_1NUM[i]/xs_1NUM[i])**2. + (xsErr_1DENOM[i]/xs_1DENOM[i])**2. ))
    percErr_NLOPS.append((ratioErr_NLOPS[i]*100.)/ratio_NLOPS[i])
    ratio_NLOPSMPIBBRHAD.append(xs_2NUM[i]/xs_2DENOM[i])
    ratioErr_NLOPSMPIBBRHAD.append(ratio_NLOPSMPIBBRHAD[i]*math.sqrt( (xsErr_2NUM[i]/xs_2NUM[i])**2. + (xsErr_2DENOM[i]/xs_2DENOM[i])**2. ))
    percErr_NLOPSMPIBBRHAD.append((ratioErr_NLOPSMPIBBRHAD[i]*100.)/ratio_NLOPSMPIBBRHAD[i])

print "------------------------------------------------------------------------------------------------------"
print "\n\n-----> Ratio NLO:"
print "Xsec ratio values: \n"+str(ratio_NLO)
print "Xsec ratio errs: \n"+str(ratioErr_NLO)
print "Percent error: \n"+str(percErr_NLO)
print "\n-----> Ratio NLO+PS:"
print "Xsec ratio values: \n"+str(ratio_NLOPS)
print "Xsec ratio errs: \n"+str(ratioErr_NLOPS)
print "Percent error: \n"+str(percErr_NLOPS)
print "\n-----> Ratio NLO+PS+MPI+BBR+HAD:"
print "Xsec ratio values: \n"+str(ratio_NLOPSMPIBBRHAD)
print "Xsec ratio errs: \n"+str(ratioErr_NLOPSMPIBBRHAD)
print "Percent error: \n"+str(percErr_NLOPSMPIBBRHAD)
print "\n"

xErr = [(b/2.) for b in binWidth_0NUM]

## Plot all ratio distributions
figComp, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 8), gridspec_kw = {'height_ratios':[3, 1]})

ax1.errorbar(binCent_0NUM, ratio_NLO, xerr=xErr, yerr=None, fmt='ko', ecolor='k', capthick=1.5, label='NLO') ## no errors
#no errors -----
#ax1.errorbar(binCent_1NUM, ratio_NLOPS, xerr=xErr, yerr=ratioErr_NLOPS, fmt='bo', ecolor='b', capthick=1.5, label='NLO+PS')
#ax1.errorbar(binCent_2NUM, ratio_NLOPSMPIBBRHAD, xerr=xErr, yerr=ratioErr_NLOPSMPIBBRHAD, fmt='ro', ecolor='r',capthick=1.5, label='NLO+PS+MPI+BBR+HAD')
#y-errors included -----
ax1.errorbar(binCent_1NUM, ratio_NLOPS, xerr=xErr, yerr=ratioErr_NLOPS, fmt='bo', ecolor='b', capthick=1.5, label='NLO+PS')
ax1.errorbar(binCent_2NUM, ratio_NLOPSMPIBBRHAD, xerr=xErr, yerr=ratioErr_NLOPSMPIBBRHAD, fmt='ro', ecolor='r',capthick=1.5, label='NLO+PS+MPI+BBR+HAD')

ax1.legend(loc='lower left', bbox_to_anchor=(0.276, -0.02, 0, 0))
ax1.set_ylabel(r'd$\sigma$/d$p_{T}$')
ax1.set_xlim(binCent_0NUM[0]-xErr[0]-10., binCent_0NUM[numBins-1]+xErr[numBins-1]+10.)
ax1.set_ylim(0.02, 1.2)


## Do ratio subplot
subplot_NLOPS = []
subplotErr_NLOPS = []
subplotPercErr_NLOPS = []
subplot_NLOPSMPIBBRHAD = []
subplotErr_NLOPSMPIBBRHAD = []
subplotPercErr_NLOPSMPIBBRHAD = []

for i,b in enumerate(xs_0NUM):
    subplot_NLOPS.append(ratio_NLOPS[i]/ratio_NLO[i])
    subplotErr_NLOPS.append(subplot_NLOPS[i]*math.sqrt( (ratioErr_NLO[i]/ratio_NLO[i])**2. + (ratioErr_NLOPS[i]/ratio_NLOPS[i])**2. ))
    subplotPercErr_NLOPS.append((subplotErr_NLOPS[i]*100.)/subplot_NLOPS[i])
    subplot_NLOPSMPIBBRHAD.append(ratio_NLOPSMPIBBRHAD[i]/ratio_NLO[i])
    subplotErr_NLOPSMPIBBRHAD.append(subplot_NLOPSMPIBBRHAD[i]*math.sqrt( (ratioErr_NLO[i]/ratio_NLO[i])**2. + (ratioErr_NLOPSMPIBBRHAD[i]/ratio_NLOPSMPIBBRHAD[i])**2. ))
    subplotPercErr_NLOPSMPIBBRHAD.append((subplotErr_NLOPSMPIBBRHAD[i]*100.)/subplot_NLOPSMPIBBRHAD[i])

print "------------------------------------------------------------------------------------------------------"
print "\n\n-----> Ratio of R21 NLO+PS/NLO:"
print "Xsec ratio values: \n"+str(subplot_NLOPS)
print "Xsec ratio errs: \n"+str(subplotErr_NLOPS)
print "Percent error: \n"+str(subplotPercErr_NLOPS)
print "\n\n-----> Ratio of R21 NLO+PS+MPI+BBR+HAD/NLO:"
print "Xsec ratio values: \n"+str(subplot_NLOPSMPIBBRHAD)
print "Xsec ratio errs: \n"+str(subplotErr_NLOPSMPIBBRHAD)
print "Percent error: \n"+str(subplotPercErr_NLOPSMPIBBRHAD)
print "\n"

# no errors -----
ax2.errorbar( binCent_1NUM, subplot_NLOPS, xerr=xErr, yerr=None, fmt='bo', ecolor='b', capthick=1.5, label='NLO+PS' )
ax2.errorbar( binCent_2NUM, subplot_NLOPSMPIBBRHAD, xerr=xErr, yerr=None, fmt='ro', ecolor='r', capthick=1.5, label='NLO+PS+MPI+BBR+HAD' )
#y-errors included -----
#ax2.errorbar( binCent_1NUM, subplot_NLOPS, xerr=xErr, yerr=subplotErr_NLOPS, fmt='bo', ecolor='b', capthick=1.5, label='NLO+PS' )
#ax2.errorbar( binCent_2NUM, subplot_NLOPSMPIBBRHAD, xerr=xErr, yerr=subplotErr_NLOPSMPIBBRHAD, fmt='ro', ecolor='r', capthick=1.5, label='NLO+PS+MPI+BBR+HAD' )

ax2.axhline(y=1, linewidth=1, linestyle='--', color='k')
ax2.set_ybound(0.5, 1.5)
ax2.set_ylabel('Ratio to NLO')
ax2.set_xlabel(xtitle+' [GeV]')
ax2.xaxis.set_label_coords(0.75, -0.21)
figComp.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in figComp.axes[:-1]], visible=False)


if args.out:
    out = args.out
else:
    out = 'r21_'+args.tableNUM+'_xsecs.pdf'
    figComp.savefig(out)

###################################
## NP Corr Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.set(xlabel=xtitle+' [GeV]', ylabel='On/Off', title='Non-Pert. Corrections for '+str(xtitle))
ax.yaxis.label.set_size(18)
ax.set(ylim=[0.5,1.5])
ax.axhline(y=1, linewidth=1, color='k', linestyle='--')

ratio_NPCorr = []
ratioErr_NPCorr = []
percErr_NPCorr = []

#Take ratios
for i,b in enumerate(xs_0NUM):
    ratio_NPCorr.append(ratio_NLOPSMPIBBRHAD[i]/ratio_NLOPS[i])
    ratioErr_NPCorr.append(ratio_NPCorr[i]*math.sqrt( (ratioErr_NLOPSMPIBBRHAD[i]/ratio_NLOPSMPIBBRHAD[i])**2. + (ratioErr_NLOPS[i]/ratio_NLOPS[i])**2. ))
    percErr_NPCorr.append((ratioErr_NPCorr[i]*100.)/ratio_NPCorr[i])

ax.errorbar(binCent_0NUM, ratio_NPCorr, xerr=xErr, yerr=ratioErr_NPCorr, fmt='ko', capthick=1.5) #y-errors included

ax.set_xlim(binCent_0NUM[0]-xErr[0]-10., binCent_0NUM[numBins-1]+xErr[numBins-1]+10.)

if args.out:
    out = args.out
else:
    out = 'r21_'+args.tableNUM+'_NPcorr.pdf'
fig.savefig(out)

print "------------------------------------------------------------------------------------------------------"
print "\n\n-----> R21 NP Corrections (NLO+PS+MPI+BBR+HAD)/(NLO+PS):"
print "Xsec ratio values: \n"+str(ratio_NPCorr)
print "Xsec ratio errs: \n"+str(ratioErr_NPCorr)
print "Percent error: \n"+str(percErr_NPCorr)
print "\n"

###################################
## PS Effect Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.set(xlabel=xtitle+' [GeV]', ylabel='On/Off', title='PS Effect for '+str(xtitle))
ax.yaxis.label.set_size(18)
ax.set(ylim=[0.5,1.5])
ax.axhline(y=1, linewidth=1, color='k', linestyle='--')

ratio_PSeffect = []
ratioErr_PSeffect = []
percErr_PSeffect = []

#Take ratios
for i,b in enumerate(xs_0NUM):
    ratio_PSeffect.append(ratio_NLOPS[i]/ratio_NLO[i])
    ratioErr_PSeffect.append(ratio_PSeffect[i]*math.sqrt( (ratioErr_NLOPS[i]/ratio_NLOPS[i])**2. + (ratioErr_NLO[i]/ratio_NLO[i])**2. ))
    percErr_PSeffect.append((ratioErr_PSeffect[i]*100.)/ratio_PSeffect[i])

#ax.errorbar(binCent_0NUM, ratio_PSeffect, xerr=xErr, yerr=ratioErr_PSeffect, fmt='ko', capthick=1.5) #y-errors included
ax.errorbar(binCent_0NUM, ratio_PSeffect, xerr=xErr, yerr=None, fmt='ko', capthick=1.5) #no y-errors

ax.set_xlim(binCent_0NUM[0]-xErr[0]-10., binCent_0NUM[numBins-1]+xErr[numBins-1]+10.)

if args.out:
    out = args.out
else:
    out = 'r21_'+args.tableNUM+'_PSeffect.pdf'
fig.savefig(out)

print "------------------------------------------------------------------------------------------------------"
print "\n\n-----> R21 PS effect (NLO+PS)/(NLO):"
print "Xsec ratio values: \n"+str(ratio_PSeffect)
print "Xsec ratio errs: \n"+str(ratioErr_PSeffect)
print "Percent error: \n"+str(percErr_PSeffect)
print "\n"

print ("\nFinished!")
