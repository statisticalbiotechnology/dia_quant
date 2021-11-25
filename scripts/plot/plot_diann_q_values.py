#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 11:03:50 2021

@author: ptruong
"""

import pandas as pd
import os 
import matplotlib.pyplot as plt

os.chdir("/hdd_14T/data/PXD002952/20210614_dataset/diaumpire_spectral_lib_20210706/MSFragger_20210707/diann_20210811")


df = pd.read_csv("report.tsv", sep = "\t")

# map float in Protein.Ids to check what is the problem and remove these
float_mapper = lambda x : isinstance(x, float)
df["isfloat"] = df["Protein.Ids"].map(float_mapper)
df[df["isfloat"] == True]["Protein.Ids"]
df = df[df["isfloat"] != True]

# get decoy column
decoy_mapper = lambda x:x.split("_")[0] == "DECOY"
df["decoy"] = df["Protein.Ids"].map(decoy_mapper)


df_run.columns

runs = df.Run.unique()
run = runs[0]


df_run = df[df.Run == run]

df_incorrect = df_run[df_run.decoy == True].sort_values(by = "CScore")
df_correct = df_run[df_run.decoy == False].sort_values(by = "CScore")

df_incorrect["incorrect_q_area"] = df_incorrect["Q.Value"].cumsum()
df_correct["correct_q_area"] =  df_correct["Q.Value"].cumsum()

df_incorrect

##########
df_qVals = pd.DataFrame()

qval_col = "Q.Value"
dfs_qVals = []
for run in runs:
    df_run = df[df.Run == run].sort_values(by = "CScore")
    df_run.set_index("CScore", inplace = True)
    dfs_qVals.append(df_run[qval_col])#.reset_index().drop("index", axis = 1)[qval_col]

for i in dfs_qVals:
    i.plot()
    
    
split_name = lambda x: x.split("_")[5]
df_qVals = df_qVals.rename(split_name, axis = 1)

(1-df_qVals).plot()
ax.set_xlabel("ordered PSM by m_Score")
ax.set_ylabel("m_score")













