#!/bin/bash

./plotNPCorr.py d02-x01-y01 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorr.py d06-x01-y01 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorr.py d16-x01-y01 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorr.py d20-x01-y01 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorr.py d52-x01-y01 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorr.py d56-x01-y01 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorr.py d66-x01-y01 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorr.py d70-x01-y01 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda

./plotNPCorr.py d03-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 
./plotNPCorr.py d07-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d10-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d13-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d17-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d21-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d24-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d53-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d57-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d60-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d63-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d67-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d71-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda
./plotNPCorr.py d74-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda

./plotNPCorrRatio.py d03-x01-y01 d02-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorrRatio.py d07-x01-y01 d06-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorrRatio.py d17-x01-y01 d16-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorrRatio.py d21-x01-y01 d20-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorrRatio.py d53-x01-y01 d52-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorrRatio.py d57-x01-y01 d56-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorrRatio.py d67-x01-y01 d66-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda
./plotNPCorrRatio.py d71-x01-y01 d70-x01-y01 2j_NLO-100M.yoda 2j_PS-100M.yoda 2j_PS_NPOn-100M.yoda 1j_NLO-50M.yoda   1j_PS_scale5-50M.yoda 1j_PS_scale5_NPOn-30M.yoda

