#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:58:08 2022

@author: ptruong
"""

import pandas as pd
import numpy as np
from parsers.parse_triqler import  parse_triqler
import seaborn as sns
import matplotlib.pyplot as plt
import numpy.random as npr
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

def get_fraction_hela(df_in, method):
    df=df_in.copy()
    df.sort_values(by = "FDR", inplace = True)
    df.drop(df[df["Protein"].str.contains("DECOY_")].index, inplace=True)
    df["count_HUMAN"] = df.Protein.str.contains("_HUMAN").astype(int)
    df["count_ECOLI"] = df.Protein.str.contains("_ECOLI").astype(int)
    df["count_YEAST"] = df.Protein.str.contains("_YEAST").astype(int)
    df["cumsum_HUMAN"] = df["count_HUMAN"].cumsum()
    df["cumsum_ECOLI"] = df["count_ECOLI"].cumsum()
    df["cumsum_YEAST"] = df["count_YEAST"].cumsum()
    df["Fraction_HeLa"] = df["cumsum_HUMAN"] / (df["cumsum_HUMAN"] + df["cumsum_ECOLI"] + df["cumsum_YEAST"])
    df["Method"] = method
#    df.fillna(1, inplace = True) # assume NaN is maxed out FDR
    df.FDR = df.FDR.fillna(value = 1)
    #df = df.reset_index().drop("index",axis = 1)
    return df[["FDR", "Fraction_HeLa", "Method"]]

def get_fraction_hela_df(triqler, top3, msstats, msqrob2):
    fdrs = []
    for df, method in zip([triqler, top3, msstats, msqrob2], ["Triqler", "Top3", "MSstats", "MSqRob2"]):
        fdrs.append(get_fraction_hela(df, method))
    df = pd.concat(fdrs)
    df = df.reset_index().drop("index", axis = 1).copy()
    return df

def threshold_fc(df, fc_threshold):
    fc_threshold = 0.0
    df_fc = df[abs(df["log2FC"]) > fc_threshold].copy()
    df_fc["FDR"] = qvalues(df_fc, pcol = "p")["q"] #recompute FDR for thresholded set
    return df_fc


def calibration_plot(df, xlim = [0,0.10], ylim = [0,0.20]):
    fig, axs = plt.subplots(1, 1, figsize=(10,6))
    sns.lineplot(x = "FDR", y = "Fraction_HeLa", data = df, ax = axs, hue = "Method")
    axs.set_xlabel("FDR", fontsize=24)
    axs.set_ylabel(r"Fraction HeLa", fontsize=24)
    axs.tick_params(axis='x', which='major', labelsize=21)#labelrotation=90)
    axs.tick_params(axis='y', which='major', labelsize=21)
    axs.set_xlim(xlim)
    axs.set_ylim(ylim)
    def abline(slope, intercept):
        """Plot a line from slope and intercept"""
        #axes = plt.gca()
        x_vals = np.array(axs.get_xlim())
        y_vals = intercept + slope * x_vals
        axs.plot(x_vals, y_vals, 'k--', alpha = 0.7)
    abline(1,0)
#    print("Outputting : " + output)


def plot(triqler_file, top3_file, msstats_file, msqrob2_file, fc_threshold = 0, xlim = [0,0.10], ylim = [0,0.2]):
    
    #fc_threshold = 0.0 #should be same as triqler fc_eval

    #triqler_file = "triqler_results.csv"
    #top3_file = "top3_results.csv"
    #msstats_file = "msstats_results.csv"
    #msqrob2_file = "msqrob2_results.csv"
    
    triqler = parse_triqler(triqler_file)
    #triqler[~triqler.protein.str.contains("DECOY")]
    triqler["specie"] = triqler.protein.map(lambda x:x.split("_")[1])
    triqler["FDR"] = triqler["q_value"]
    triqler.rename({"protein":"Protein"}, axis = 1, inplace = True)
    top3 = pd.read_csv(top3_file, sep = "\t").rename({"q":"FDR", 'log2(A,B)':"log2FC"}, axis = 1)
    top3.rename({"ProteinName":"Protein"}, axis = 1, inplace = True)
    msstats = pd.read_csv(msstats_file, sep = ",").rename({"adj.pvalue":"FDR", "pvalue":"p"}, axis = 1)
    msstats["specie"] = msstats.Protein.map(lambda x:x.split("_")[1])
    msqrob2 = pd.read_csv(msqrob2_file, sep = ",").rename({"Unnamed: 0":"protein", "adjPval":"FDR", "pval":"p", "logFC":"log2FC"}, axis = 1)
    msqrob2.rename({"protein":"Protein"}, axis = 1, inplace = True)
    msqrob2["specie"] = msqrob2.Protein.map(lambda x:x.split("_")[1])
    msqrob2.rename({"protein":"Protein"}, axis = 1, inplace = True)

    if fc_threshold != 0:
        #triqler = threshold_fc(triqler, fc_threshold)
        top3 = threshold_fc(top3, fc_threshold)
        msstats = threshold_fc(msstats, fc_threshold)
        msqrob2 = threshold_fc(msqrob2, fc_threshold)
        
    df = get_fraction_hela_df(triqler, top3, msstats, msqrob2)
    #df = df[df.Fraction_HeLa != 0] # remove artifical 1 when cumsum
    #df = df[df.FDR != 0] #remove FDR that are 0, these cant be exactly zero...
    calibration_plot(df = df, xlim = xlim, ylim = ylim)

 
def plot_calibration_PT_origo(method = "ID", fc_threshold = 0):
    directory = "results/" + method + "/"
    triqler_file = directory + "triqler_results.csv"
    top3_file = directory + "top3_results.csv"
    msstats_file = directory + "msstats_results.csv"
    msqrob2_file = directory + "msqrob2_results.csv"
    
    fc_threshold = fc_threshold
    xlim = [0, 0.10]
    ylim = [0, 0.2]

    plot(triqler_file, top3_file, msstats_file, msqrob2_file, 
         fc_threshold = fc_threshold, 
         xlim = xlim, ylim = ylim)



