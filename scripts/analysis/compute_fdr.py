#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 21:01:58 2022

@author: ptruong
"""
import pandas as pd 
import numpy as np
import numpy.random as npr
import argparse

def bootstrap(invec):
    idx = npr.randint(0, len(invec), len(invec))
    return [invec[i] for i in idx]

def estimatePi0(p, numBoot=100, numLambda=100, maxLambda=0.95):
    p.sort()
    n=len(p)
    lambdas=np.linspace(maxLambda/numLambda,maxLambda,numLambda)
    Wls=np.array([n-np.argmax(p>=l) for l in lambdas])
    pi0s=np.array([Wls[i] / (n * (1 - lambdas[i])) for i in range(numLambda)])
    minPi0=np.min(pi0s)
    mse = np.zeros(numLambda)
    for boot in range(numBoot):
        pBoot = bootstrap(p)
        pBoot.sort()
        WlsBoot =np.array([n-np.argmax(pBoot>=l) for l in lambdas])
        pi0sBoot =np.array([WlsBoot[i] / (n *(1 - lambdas[i])) for i in range(numLambda)])
        mse = mse + np.square(pi0sBoot-minPi0)
    minIx = np.argmin(mse)
    return pi0s[minIx]

def qvalues(pvalues, pcol = "p"):
    m = pvalues.shape[0] # The number of p-values
    pvalues.sort_values(pcol,inplace=True) # sort the pvalues in acending order
    pi0 = estimatePi0(list(pvalues[pcol].values))
    print("pi_0 estimated to " + str(pi0))
    
    # calculate a FDR(t) as in Storey & Tibshirani
    num_p = 0.0
    for ix in pvalues.index:
        num_p += 1.0
        fdr = pi0*pvalues.loc[ix,pcol]*m/num_p
        pvalues.loc[ix,"q"] = fdr
    
    # calculate a q(p) as the minimal FDR(t)
    old_q=1.0
    for ix in reversed(list(pvalues.index)):
        q = min(old_q,pvalues.loc[ix,"q"])
        old_q = q
        pvalues.loc[ix,"q"] = q
    return pvalues


def recompute_q_value(filename = "report.tsv", output = "report_recomputed_fdr.tsv", pcol = "Global.Q.Value"):
    df = pd.read_csv(filename,sep="\t")    
    df = qvalues(df, pcol = pcol)
    df.to_csv(output, sep = "\t", index = False)
    
parser = argparse.ArgumentParser(
    description='Recomputes the FDR .',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--input', type=str,
                    help='Input file to compute fdr.')

parser.add_argument('--output', type=str,
                    help='Output name.')

#parser.add_argument('--pcol', type=str,
#                    help='p-value or similar metric columns to be used to recompute the FDR.')

# parse arguments from command line
args = parser.parse_args()
input_file = args.input
output = args.output
#pcol = args.pcol

if __name__ == "__main__":
    recompute_q_value(filename = input_file, output = output, pcol = "Global.Q.Value")
    





