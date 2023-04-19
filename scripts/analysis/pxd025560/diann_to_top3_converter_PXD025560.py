#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 16:52:19 2022

@author: ptruong
"""

import pandas as pd
import numpy as np
import re
import argparse

import os
os.chdir("/hdd_14T/data/PXD025560")

# DIA-NN
def avg_3_largest_precursor_on_run_level(df_run):
    def avg_of_3_largest_precursor(df_run):
        return df_run.groupby("Protein.Ids")["Precursor.Quantity"].apply(lambda x: x.nlargest(3).mean() if len(x.nlargest(3)) >= 2 else np.nan).reset_index()
    
    res = avg_of_3_largest_precursor(df_run)
    experiment_id = np.unique(df_run.histology_idx)[0]
    sample_id = np.unique(df_run.sample_class)[0]
    midx = pd.MultiIndex(levels = [[sample_id],[experiment_id]], codes = [[0],[0]], names = ["sample_id", "experiment_id"])
    df = pd.DataFrame(res.values)
    specie_map = lambda x: x.split("_")[-1]
    #protein_map = lambda x: x.split("_")[-2]
    res["specie"] = res["Protein.Ids"].map(specie_map)
    res["ProteinName"] = res["Protein.Ids"]
    res = res.drop(["Protein.Ids"], axis = 1)
    res = res.set_index(["specie", "ProteinName"])
    df = pd.DataFrame(res.values, columns = midx, index = res.index)
    return df

def avg_3_largest_precursor(df):
    dfs = []
    for run in df.Run.unique(): # for every tun otherwise we mix together proteins from multiple runs when doing top3.
        df_run = df[df.Run == run]
        #if df_run.Run.unique()[0].split("-")[-3] == "GPF":
        #    continue
        df_top3_run_level = avg_3_largest_precursor_on_run_level(df_run)
        dfs.append(df_top3_run_level)
    df = pd.concat(dfs, axis = 1)
    return df

parser = argparse.ArgumentParser(
    description='This scripts formats OpenSwath output with dscore to take the avg of three largest PSM as peptide quantity. The Openswath outputs each sample as a file, therefore we input a file directory to this script. Note: The OpenSwath output with dscore need to be in a seperate directory for themselves.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--input_file', type=str,
                    help='DIA-NN report.tsv file.')

parser.add_argument('--fdr_threshold', type=float,
                    help='fdr_threshold level to cut-off at.')

parser.add_argument('--q_value_column', type=str, default = "q",
        help="DIA-NN output has options 'q', Q.Value', 'Global.Q.Value', 'Protein.Q.Value', 'PG.Q.Value', 'Global.PG.Q.Value', 'GG.Q.Value', 'Translated.Q.Value'.")

parser.add_argument('--output', type=str, default = "diann_top3_input_formatted.csv",
                    help='Name of the output file.')


# parse arguments from command line
args = parser.parse_args()
input_file = args.input_file
q_value_column = args.q_value_column
fdr_threshold = args.fdr_threshold
output = args.output

if __name__ == "__main__":
    print("Reading in: " + input_file)
    df = pd.read_csv(input_file, sep = "\t")
    meta = pd.read_csv("metadata.csv", sep = "/")

    mapper = meta.set_index("SampleID")["Histology"].to_dict()
    metas = []
    for histology in meta.Histology.unique():
        partial_meta = meta[meta.Histology == histology].reset_index().drop("index", axis = 1).reset_index().rename({"index":"histology_idx"}, axis = 1)
        metas.append(partial_meta)
    meta = pd.concat(metas)

    histology_idx_mapper = meta.drop("Histology", axis = 1).set_index("SampleID")["histology_idx"].to_dict()
        
    df["sample_id"] =  df.Run.map(lambda x: re.findall('\d+',x.split("_")[-1])[0]).astype(int)
    df["sample_class"] = df.sample_id.map(mapper)
    df["histology_idx"] =df.sample_id.map(histology_idx_mapper)
    
    df = df[df[q_value_column] < fdr_threshold]
    df = avg_3_largest_precursor(df)
    #print("Generating output file: " + "Ctrl_LT_"+output)
    #print("Generating output file: " + "Ctrl_ST_"+output)
    #print("Generating output file: " + "LT_ST_"+output)
    print("Generating output file: " + output)
    #df.T[df.columns.get_level_values("sample_id").isin(["Ctrl", "LT"])].T.to_csv("Ctrl_LT_"+output, sep = "\t")
    #df.T[df.columns.get_level_values("sample_id").isin(["Ctrl", "ST"])].T.to_csv("Ctrl_ST_"+output, sep = "\t")
    #df.T[df.columns.get_level_values("sample_id").isin(["LT", "ST"])].T.to_csv("LT_ST_"+output, sep = "\t")
    df.to_csv(output, sep = "\t")
    print("Done!")

