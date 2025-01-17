#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:20:54 2022

@author: ptruong
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import numpy.random as npr

from parsers.parse_triqler import  parse_triqler
import argparse
sns.set_context("talk")


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


def read_in_files(triqler_file = "triqler_results/fc_0.48",
                  top3_file = "top3_results.csv",
                  msstats_file = "msstats_results.csv",
                  msqrob2_file = "msqrob2_results.csv"):
    triqler_results = parse_triqler(triqler_file)
    top3_results = pd.read_csv(top3_file, sep = "\t")
    msstats_results = pd.read_csv(msstats_file, sep = ",")
    msqrob2_results = pd.read_csv(msqrob2_file, sep = ",").rename({"Unnamed: 0":"Protein"},axis=1)
    
    #Rename protein, fdr to same name
    triqler_results = triqler_results.rename({"q_value":"FDR", "protein":"Protein", "log2_fold_change":"log2FC"}, axis = 1)
    top3_results = top3_results.rename({"q":"FDR", "ProteinName":"Protein", "log2(A,B)":"log2FC"}, axis = 1)
    msstats_results = msstats_results.rename({"adj.pvalue":"FDR", "pvalue":"p"}, axis = 1)
    msqrob2_results = msqrob2_results.rename({"adjPval":"FDR", "logFC":"log2FC", "pval":"p"}, axis = 1)
    
    methods = ["Triqler", "Top3", "MsStats", "MsqRob2"]
    data = [triqler_results, top3_results, msstats_results, msqrob2_results]
    zipped_files = zip(methods, data)
    return zipped_files

def calculate_actual_error(df, fc_threshold = 0.6):
    df["abs(log2FC)"] = abs(df.log2FC)
    df = df[~df.Protein.str.contains("_DECOY")]
    df = df[~df["FDR"].isna()]
    df.sort_values("FDR", inplace = True) #fillna 0 or drop na
    df = df[df["abs(log2FC)"] > fc_threshold].copy(deep=True)
    if "p" in df.columns:
        df["FDR"] = qvalues(df,pcol="p")["q"]
   #     df["FDR"] = qvalues(df,pcol="FDR")["q"]
    
    df["count_HUMAN"] = df.Protein.str.contains("_HUMAN").astype(int)
    df["count_ECOLI"] = df.Protein.str.contains("_ECOLI").astype(int)
    df["count_YEAST"] = df.Protein.str.contains("_YEAST").astype(int)
    df["cumsum_HUMAN"] = df["count_HUMAN"].cumsum()
    df["cumsum_ECOLI"] = df["count_ECOLI"].cumsum()
    df["cumsum_YEAST"] = df["count_YEAST"].cumsum()
    
    df["actual_error"] = df["cumsum_HUMAN"] / (df["cumsum_HUMAN"] + df["cumsum_ECOLI"] + df["cumsum_YEAST"])
    return df.loc[:,["Protein", "log2FC", "FDR", "method", "abs(log2FC)", 'count_HUMAN', 'count_ECOLI', 'count_YEAST', 'cumsum_HUMAN', 'cumsum_ECOLI', 'cumsum_YEAST', 'actual_error']]            

def get_actual_error_df(zipped_files, fc_threshold = 0.48):    
    dfs = []
    for method, df in zipped_files:
        df["method"] = method
        if method != "triqler":
            df = calculate_actual_error(df, fc_threshold = fc_threshold)
        else:
            df = calculate_actual_error(df, fc_threshold = 0.0) # triqler don't require fc-thresholding, but use the correct input when computing triqler.
        dfs.append(df)
    res = pd.concat(dfs)
    res = res.reset_index().drop("index", axis = 1)
    return res

def calibration_plot(df, output, xlim = [0,0.05], ylim = [0,0.05]):
    fig, axs = plt.subplots(1, 1, figsize=(10,6))
    #sns.lineplot(x = "FDR", y = "actual_error", data = df, ax = axs, hue = "method")
    sns.lineplot(x = "actual_error", y = "FDR", data = df, ax = axs, hue = "method")
    #axs.set_xlabel(r"\textit{q}-value / FDR ", fontsize=34)
    #axs.set_ylabel("Fraction HeLa", fontsize=38)

    axs.set_xlabel("Actual FDR", fontsize=34)
    axs.set_ylabel(r"Fraction HeLa", fontsize=38)

    axs.tick_params(axis='x', which='major', labelsize=42)#labelrotation=90)
    axs.tick_params(axis='y', which='major', labelsize=42)
    axs.set_xlim(xlim)
    axs.set_ylim(ylim)

    def abline(slope, intercept):
        """Plot a line from slope and intercept"""
        #axes = plt.gca()
        x_vals = np.array(axs.get_xlim())
        y_vals = intercept + slope * x_vals
        axs.plot(x_vals, y_vals, 'k--', alpha = 0.7)
    abline(1,0)
    print("Outputting : " + output)
    plt.savefig(output, bbox_inches="tight")


parser = argparse.ArgumentParser(
    description='This script takes triqler results, top3 results, msstat results and msqrob2 results and plots calibration plots.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--triqler_input', type=str,
                    help='Triqler results file.')

parser.add_argument('--top3_input', type=str,
                    help='Top3 results file.')

parser.add_argument('--msstats_input', type=str,
                    help='MsStats results file.')

parser.add_argument('--msqrob2_input', type=str,
                    help='MSqRob2 results file.')

parser.add_argument('--fc_threshold', type=float,
                    help='Log2FC threshold to apply on Top3, MsStats and MSqRob2 results. NOTE: Triqler does not need Log2FC thresholding. Use the same fold_change_eval parameter when running triqler.')

parser.add_argument('--output', type=str,
                    help='Output name.')

# parse arguments from command line
args = parser.parse_args()
triqler_file = args.triqler_input
top3_file = args.top3_input
msstats_file = args.msstats_input
msqrob2_file = args.msqrob2_input
fc_threshold = args.fc_threshold
output = args.output
                            


if __name__ == "__main__":        
    zipped_files = read_in_files(triqler_file = triqler_file,
                          top3_file = top3_file,
                          msstats_file = msstats_file,
                          msqrob2_file = msqrob2_file)
    
    df = get_actual_error_df(zipped_files, fc_threshold = fc_threshold)
    calibration_plot(df, output, xlim = [0,0.025])



"""
plt.plot(df[df["method"] == "Triqler"].actual_error, df[df["method"] == "Triqler"].FDR)
plt.plot(df[df["method"] == "Top3"].actual_error, df[df["method"] == "Top3"].FDR)
plt.plot(df[df["method"] == "MsStats"].actual_error, df[df["method"] == "MsStats"].FDR)
plt.plot(df[df["method"] == "MsqRob2"].actual_error, df[df["method"] == "MsqRob2"].FDR)        
        

plt.plot(df[df["method"] == "Triqler"].FDR, df[df["method"] == "Triqler"].actual_error)
plt.plot(df[df["method"] == "Top3"].FDR, df[df["method"] == "Top3"].actual_error)
plt.plot(df[df["method"] == "MsStats"].FDR, df[df["method"] == "MsStats"].actual_error)
plt.plot(df[df["method"] == "MsqRob2"].FDR, df[df["method"] == "MsqRob2"].actual_error)        
    

df_methods = []
for method in df.method.unique():
    df_method = df[df.method == method]
    df_method["FDR"] = qvalues(df_method,pcol="p")["q"]

 if "p" in df.columns:
     df["FDR"] = qvalues(df,pcol="p")["q"]
"""




