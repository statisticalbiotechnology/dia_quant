#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 11:26:00 2022

@author: ptruong
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from parsers.parse_triqler import  parse_triqler
sns.set_context("talk")

file_dir = "/hdd_14T/data/PXD002952/20210614_dataset/result_files_20220214/PS/"

negCol = "Differential HeLa"
posCol = "Differential non-HeLa"
eCol = "Actual Error Rate"

def remove_decoy(df, protein_column):   
    res = df[~df[protein_column].str.contains("DECOY_")].copy(deep=True)
    return res

def countProteins(df, method):
    df = remove_decoy(df, protein_column = "Protein")
    df.dropna(subset=["FDR"], inplace = True)
    df.sort_values(by = "FDR", inplace = True)
    negative = df["Protein"].str.contains("_HUMAN").astype(int).copy(deep=True)
    df[negCol] = negative.cumsum().copy(deep=True)
    df[posCol] = (1-negative).cumsum().copy(deep=True)
    df["method"] = method
    return df

def read_in_files(triqler_file = "triqler_results/fc_0.96",
                  top3_file = "top3_output_diann.csv",
                  msstats_file = "msstat_output.csv",
                  msqrob2_file = "msqrob2_results.tsv"):
    triqler_results = parse_triqler(triqler_file)
    top3_results = pd.read_csv(top3_file, sep = "\t")
    msstats_results = pd.read_csv(msstats_file, sep = ",")
    msqrob2_results = pd.read_csv(msqrob2_file, sep = ",").rename({"Unnamed: 0":"Protein"},axis=1)
    
    #Rename protein, fdr to same name
    triqler_results = triqler_results.rename({"q_value":"FDR", "protein":"Protein"}, axis = 1)
    top3_results = top3_results.rename({"q":"FDR", "ProteinName":"Protein"}, axis = 1)
    msstats_results = msstats_results.rename({"adj.pvalue":"FDR"}, axis = 1)
    msqrob2_results = msqrob2_results.rename({"adjPval":"FDR"}, axis = 1)
    
    methods = ["Triqler", "Top3", "MsStats", "MsqRob2"]
    data = [triqler_results, top3_results, msstats_results, msqrob2_results]
    zipped_files = zip(methods, data)
    return zipped_files


def get_differential_abundance_count(zipped_files):
    dfs = []
    for method, df in zipped_files:
        df_count = countProteins(df, method)
        dfs.append(df_count.loc[:,["Protein", "FDR", posCol, negCol, "method"]])
    
    res = pd.concat(dfs)
    res = res.reset_index().drop("index", axis = 1)
    return res

zipped_files = read_in_files(triqler_file = "triqler_results/fc_0.96",
                  top3_file = "top3_output_diann.csv",
                  msstats_file = "msstat_output.csv",
                  msqrob2_file = "msqrob2_results.tsv")

df_count = get_differential_abundance_count(zipped_files)

# FDR VS ACTUAL FDR ... we need to sort by FC Treshold

for method, df in zipped_files:
    pass

df.sort_values(by = "logFC") # count number of proteins under FC treshold
#df = df_count
#df[eCol] = (df[negCol]/(df[posCol]+df[negCol])).copy(deep=True)

# differential abundance HeLa vs. non-Hela.
sns.lineplot(x = negCol, y = posCol, hue = "method", data = df_count)

# error rate plot
sns.lineplot(x = eCol, y = "FDR", hue = "method", data = df_count)

    g = sns.lineplot(data=er_fdr, x=eCol, y="FDR", hue="method", ci=None)

df_count
