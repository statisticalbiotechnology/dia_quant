# About

[Triqler](https://pubmed.ncbi.nlm.nih.gov/30482846/) is a novel software for protein quantification and differential protein identification. It uses probabilistic graphical models to generate posterior distributions for fold changes between treatment groups, highlighting uncertainty rather than hiding it. Conventional (frequentist) methods use filters and imputations to control error rate and often ignore certain error sources. This project aims to benchmark Triqler against MaxQuant (A commonly used tool for protein quantification). 

For this purpose, a data set with 10 samples containing mixtures of Arabidopsis Thaliana, Caenorhabditis Elegans and Homo Sapiens proteins are used. The concentration levels are known. Theoretically, the results from Triqler should be more representative of the de facto protein quantification, since no filters or imputations methods are used, but previous attempts at showing this fact ([here](https://patruong.github.io/bayesProtQuant/)) have shown that imputation methods could severely impact the results obtained by MaxQuant, making it look either much worse or much better by giving it an unfair advantage or disadvantage. One important aspect of this research is therefore how to make a fair comparison of Triqler and MaxQuant. Sub-tasks to answer relating to this aspect is "How do we make a fair imputation if we need to impute values?" and "How do we visualize the comparison in a meaningful and comprehensible way?".



## Related studies and papers

[Integrated identification and quantification error probabilities for shotgun proteomics](https://www.biorxiv.org/content/10.1101/357285v2)

[Integrating identification and quantification uncertainty for differential protein abundance analysis with Triqler](https://www.biorxiv.org/content/10.1101/2020.09.24.311605v1?rss=1)

[A new era in proteomics: spectral library free data independent acquisition (directDIA)](https://theanalyticalscientist.com/fileadmin/tas/issues/App_Notes/05817-biognosys-app-note-supplied.pdf)

[Missing Value chapter of Course Handouts for Bayesian Data Analysis Class](https://bookdown.org/marklhc/notes_bookdown/missing-data.html)

[A foray into Bayesian handling of missing data](http://srmart.in/a-foray-into-bayesian-handling-of-missing-data/)

## ToDO:
- make a write-up about details about the projects.

## Historical log
https://patruong.github.io/bayesProtQuant/

## 2020-10-18 Sunday

Setting up a Rmarkdown log for this project. 


## 2020-10-19 Monday

### Starting up again. 

I just started checking into this project again. Let's start from scratch to get this correct from start. I will check through all the mails related to this.

Annotations that is good to know:
- PG - Protein Group.
- EG - Elution Group (modified peptide, including charge state).
- FG - Fragment Group (modified peptide, including charge state).

/data/Headers.xlsx - contains column info.

R.FileName is the columns for MS-measurement

### Old mail containing relevant information.

All the data is on bose:/media/hdd/matthew/mergespec/data/spectronaut/
The files from the latest try are named PSSS3_triqler_input_renormalized.tsv (triqler input file) and PSSS3_triqler_output_proteins.<x>vs<y>.tsv

The script I used for converting the spectronaut files (they have an xls extension, but they're actually just tab separated files): https://github.com/statisticalbiotechnology/mergespec/blob/master/bin/bayesquant/convert_spectronaut_to_triqler_input.py

The version of triqler I used to generate the data is on a branch called large_scale_optimizations: https://github.com/statisticalbiotechnology/triqler/tree/large_scale_optimizations
However, I'm not entirely sure if this is the same version that I used to generate the files, since I made some changes while working on this. So, if you run triqler yourself with this branch the results might be different. 

Some issues I had to generate a report comparing Triqler to Spectronaut were:
1. we either have their original results (500-PSSS3-precursor_Report.xls), which has a column "PG.Quantity" that contain the protein concentrations, but has missing values as it has been filtered on some FDR. Alternatively, we have their results with decoys ('S500-PSSS3-equ decoy_Report.xls'), which is not filtered on FDR and does not contain missing values, but does not contain a column with the protein quantity and I don't really know how they summarized peptide quantities to protein quantities. The first option seems more reasonable, as this is what they would normally report.
2. with these original results, we have to choose a missing value strategy and this will most likely give them either an unfair disadvantage (impute row average) or an unfair advantage (impute lowest observed value). Imputing the lowest observed value seems to be most in line with the DIA approach and I already created a file with protein concentrations using this strategy (500-PSSS3-precursor_Report.proteins.tsv) which could be useful. For the Triqler results, you can use any of the PSSS3_triqler_output_proteins.<x>vs<y>.tsv (the columns we'll use don't change for different <x> and <y>) and take the columns starting with "S01:S01_R01".

Future steps:
- Sort the proteins by pearson correlation(?) between the true concentrations and predicted concentrations and create graph with the correlation on the x-axis and the number of proteins on the y-axis. Note that the protein concentrations for spectronaut are not log2 transformed, whereas the Triqler protein concentrations are log2 transformed. Also, note that the Triqler results include proteins with high identification PEP, we thus might want to filter the list of proteins on e.g. 1% protein-identification FDR. This should all be relatively easy to do.
- Check if the value of the lowest observed imputed value for the spectronaut data (currently 139.428100585938) matters, since it will most likely affect the pearson correlation, especially if we do a log2 transformation first.
- Check the influence of the number of allowed missing values. The spectronaut data does not seem to include a limit for the number of missing values, while I think I allowed up to 25 (out of 50 samples) missing values per peptide for Triqler. It's a bit hard to compare though, since the missing values for spectronaut would only work on protein level, whereas the missing values for triqler are on peptide level.

#### Correction to mail:
Small correction to the previous mail, I actually allowed up to 35 missing values for Triqler. The concentrations for the C Elegans were dropping off so fast that such a large number was necessary (https://github.com/statisticalbiotechnology/mergespec/blob/735ed743924fa705cb2c1f64509e5a1540add574/bin/bayesquant/calibration.py#L63).

Information about the normalization of the data:
It should have been normalized (locally over the RT gradient) based on the constant Arabidopsis background.

I have generated a new report with now global median normalized data (based on the identified peptides of the constant Arabidopsis background), but also added the unnormalized quantities.

Additionally, the data is FDR unfiltered. You can filter the data by PG.Qvalue (protein group FDR) and EG.Qvalue (Precursor FDR) to get only the filtered data.

And an equal number of decoy are present, can be selected by EG.IsDecoy column.

File: 500-PSSS3-equ decoy_Report-V2-raw-and-normal.zip

According to a exploratory heatmap on this mail the normalization of the data is fine. Although, I do not recall how a heatmap indicates fine normalization.

#### Some info about the data

The PG.Quantity is based on a mix of Top3 intense peptides and reproducibility of identification.

#### Answer too my question about FG.NormalizedMS2PeakArea = 1.0

My Question: "How should we interpret non-decoy peptides with FG.NormalizedMS2PeakArea = 1.0? The PG.Quantities for some of these that I have seen seems to be NaNs. For example like these FG.NormalizedMS2PeakArea."

alues of 1 can come from two sources:

In Spectronaut, small values for quantities (<1) are set to one, these arise from small noise peaks or from local normalization effects.

In both cases were the signals noise or close to noise.

It mostly arises due to the fact that the dynamic range of MS1 and MS2 are not necessarily the same.

In Spectronaut MS1 and MS2 information is used for identification and it can be that one layer is enough. So the quantitative information of the other layer can be very low.

### How to approach this problem from my current position.

I have lot of triqler output, but it is probabily better that i redo and generate new results since I am have forgotten how these was generated, which could cause further problems down the line.

Also, I just noted that the triqler has been updated has new output options for posterior distribution. 

One remaining question is still, how to we report NaNs for the Spectronaut results.

I should also ask my PI if the PSSS3 results from last year are still relevant. 

## 2020-10-20 Tuesday
### Thoughts about how to approach the problem.
The problem was that different imputation methods could severly skew the results. How I could go about this problem is to compare different imputation methods with the result of triqler and argue why the results are bad for spectronaut and good/ok for triqler in each case. E.g. with protein counts, with boxplots etc.

One problem was that triqler had "bad" results for samples where there where low or no samples, because then the protein intensity got close to the prior, which is based on empirical means (meaning that the intensities are much higher than they should be). We could truncate the results, but in a real world case we would not know the samples so we would not be able to remove the results. 

Things to do:
- Think about how the data would be generated in real case, and perform analysis based on this.
- Think about how to handle zero samples.

## 2020-11-06 Friday
### Data-dependent Acquisition and Data Independent Acquisition (DIA).
In data-dependent acquisition (DDA), a protein sample is digested into peptides, ionized and analyzed by mass spectrometry. Peptide signals that rise above a certain treshold (noise level) in a mass spectrum are selected for fragmentation, producing tandem mass spectra (MS/MS) that can be matched to spectra in a database. The mass spectrometer randomly samples peptides for fragmentation and is biased to pick those with strongest signal, which makes it problematic to reproducibly quantify low-abundance peptides (which could hold biological value).  

Data-independent acquisition is an approach to acquisition in Mass Spectrometry which fragments all peptides within a defined mass-to-charge (m/z) windows (as opposed to a select narrow window around "the strongest signal"). The analysis is repeated as the mass spectrometer marches up the full m/z range, which results in accurate peptide quantificaiton without being limited to profiling predefined peptied of interest.    

A potential drawback of the DIA is the existence of multiple peptides in an m/z window. The fragmentation of multiple peptides results in chimeric (multiplexed) spectra which are more complex than single peptide spectra. Procedures for deconvoluting these spectra are required. Two methods for DIA are (OpenSWATH)[https://pubmed.ncbi.nlm.nih.gov/24727770/] and (ISOQUANT)[https://www.nature.com/articles/nmeth.2767]. 

## 2020-11-09 Saturday

spectronautFile: ../data/500-PSSS3-raw-reformatted_dropna_dropdup_decoy_nonShared_again.csv
FDR_treshold: 0.01
Impute: None
Global_impute: False
    
triqlerFile: ../data/triqlerResults_largeScale_minSamp20_FC0_8_adjInt/proteins.XvsY.tsv
FDR_treshold: 0.01





```python
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-2-11ddc2afe7eb> in <module>
          1 import pandas as pd
          2 import numpy as np
    ----> 3 import matplotlib.pyplot as plt
    

    ModuleNotFoundError: No module named 'matplotlib'



```python
def read_in_triqler_x_vs_y_data(filename):
    #filename = "proteins.1vs4.tsv"
    f = open(filename, "r")
    cols = f.readline().split("\n")[0].split("\t")
    n_cols = len(cols)
    vals = []
    for i in f:
        val = i.split("\n")[0].split("\t")[0:n_cols-1]
        peptides = i.split("\n")[0].split("\t")[n_cols-1:]
        val.append(";".join(peptides))
        vals.append(val)
    
    return pd.DataFrame(vals, columns = cols)  
```


```python
# Readin spectronau
file_dir = "~/git/bayesMS/data/old_data_pickled/"
spectronaut = pd.read_pickle(file_dir + "spectronaut.pkl")
# Remove decoy
spectronaut["decoy"] = spectronaut.protein.str.strip().str[:5]
spectronaut = spectronaut[spectronaut["decoy"] != "decoy"]
```


```python
# Readin triqler 

#triqler = pd.read_pickle("triqler.pkl")
file_dir = "/home/ptruong/git/bayesMS/data/triqlerResults_largeScale_minSamp20_FC0_8_adjInt/"
filename = "proteins.2vs6.tsv" 
triqler = read_in_triqler_x_vs_y_data(file_dir + filename)#Choose the sample
triqler["specie"] = triqler.protein.str.strip().str[-5:]
# Remove decoy
triqler["decoy"] = triqler.protein.str.strip().str[:5]
triqler = triqler[triqler["decoy"] != "decoy"]

```


```python
species = ["ARATH", "HUMAN", "CAEEL"]
cols = spectronaut.columns[3:]
cols = pd.DataFrame(cols)

#Sample S02 
specie = 2
sample = 1 # +1 on the sample

max_nan = 0 # set the number of nan
species_spec = spectronaut[spectronaut["specie"] == species[specie]]
species_spec = species_spec.set_index("protein")
start_of_sample_spectronaut = range(2,52,5) # start of samples
sample_s = species_spec.ix[:, start_of_sample_spectronaut[sample]:start_of_sample_spectronaut[sample]+5]
sample_s # 4210
sample_s = sample_s[sample_s.isnull().sum(axis=1) <= max_nan]

sample_s["mean"] =  sample_s.mean(axis=1)
sample_s["median"] = sample_s.median(axis=1)
sample_s["min"] = sample_s.min(axis=1)
sample_s["max"] = sample_s.max(axis=1)



start_of_sample_triqler = range(6,52,5) # start of samples
species_triq = triqler[triqler["specie"] == species[specie]]
species_triq = species_triq.set_index("protein")
sample_t = species_triq.ix[:, start_of_sample_triqler[sample]:start_of_sample_triqler[sample]+5]
sample_t = sample_t.astype(float)

sample_t["mean"] =  sample_t.mean(axis=1)
sample_t["median"] = sample_t.median(axis=1)
sample_t["min"] = sample_t.min(axis=1)
sample_t["max"] = sample_t.max(axis=1)

#reindex sample_t
rename_idx = dict(zip(sample_t.index, sample_t.index.str.strip().str[:-6]))
sample_t = sample_t.rename(index=rename_idx)

# Find overlapping proteins
overlap_set = sample_s.index.intersection(sample_t.index)





```

    /home/ptruong/anaconda3/envs/py36/lib/python3.6/site-packages/ipykernel_launcher.py:13: DeprecationWarning: 
    .ix is deprecated. Please use
    .loc for label based indexing or
    .iloc for positional indexing
    
    See the documentation here:
    http://pandas.pydata.org/pandas-docs/stable/indexing.html#ix-indexer-is-deprecated
      del sys.path[0]
    /home/ptruong/anaconda3/envs/py36/lib/python3.6/site-packages/ipykernel_launcher.py:27: DeprecationWarning: 
    .ix is deprecated. Please use
    .loc for label based indexing or
    .iloc for positional indexing
    
    See the documentation here:
    http://pandas.pydata.org/pandas-docs/stable/indexing.html#ix-indexer-is-deprecated



```python
# Random sample of n
n = 20
protein_sample = pd.DataFrame(overlap_set).sample(n)
protein_sample

sub_sample_t = sample_t.ix[protein_sample.protein]
sub_sample_s = sample_s.ix[protein_sample.protein]


#sample_s["protein"] = sample_s.index
#sample_s 
#sample_t["protein"] = sample_t.index
#sample_t

sub_sample_t["protein"] = sub_sample_t.index
sub_sample_s["protein"] = sub_sample_s.index
```

    /home/ptruong/anaconda3/envs/py36/lib/python3.6/site-packages/ipykernel_launcher.py:6: DeprecationWarning: 
    .ix is deprecated. Please use
    .loc for label based indexing or
    .iloc for positional indexing
    
    See the documentation here:
    http://pandas.pydata.org/pandas-docs/stable/indexing.html#ix-indexer-is-deprecated
      
    /home/ptruong/anaconda3/envs/py36/lib/python3.6/site-packages/ipykernel_launcher.py:7: DeprecationWarning: 
    .ix is deprecated. Please use
    .loc for label based indexing or
    .iloc for positional indexing
    
    See the documentation here:
    http://pandas.pydata.org/pandas-docs/stable/indexing.html#ix-indexer-is-deprecated
      import sys



```python
sub_sample_t
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>S02:S02_R01</th>
      <th>S02:S02_R02</th>
      <th>S02:S02_R03</th>
      <th>S02:S02_R04</th>
      <th>S02:S02_R05</th>
      <th>mean</th>
      <th>median</th>
      <th>min</th>
      <th>max</th>
      <th>protein</th>
    </tr>
    <tr>
      <th>protein</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Q23205</th>
      <td>0.9859</td>
      <td>1.2550</td>
      <td>1.2840</td>
      <td>1.2040</td>
      <td>0.7995</td>
      <td>1.10568</td>
      <td>1.15484</td>
      <td>0.7995</td>
      <td>1.2840</td>
      <td>Q23205</td>
    </tr>
    <tr>
      <th>Q2V0X4</th>
      <td>0.9297</td>
      <td>0.9930</td>
      <td>0.9796</td>
      <td>1.0570</td>
      <td>0.8322</td>
      <td>0.95830</td>
      <td>0.96895</td>
      <td>0.8322</td>
      <td>1.0570</td>
      <td>Q2V0X4</td>
    </tr>
    <tr>
      <th>P34703</th>
      <td>0.7671</td>
      <td>0.7828</td>
      <td>0.8199</td>
      <td>0.7757</td>
      <td>0.7439</td>
      <td>0.77788</td>
      <td>0.77679</td>
      <td>0.7439</td>
      <td>0.8199</td>
      <td>P34703</td>
    </tr>
    <tr>
      <th>O61793</th>
      <td>1.6680</td>
      <td>1.6140</td>
      <td>1.5020</td>
      <td>1.3250</td>
      <td>1.4030</td>
      <td>1.50240</td>
      <td>1.50220</td>
      <td>1.3250</td>
      <td>1.6680</td>
      <td>O61793</td>
    </tr>
    <tr>
      <th>Q9U2V9</th>
      <td>2.4630</td>
      <td>2.2590</td>
      <td>2.0090</td>
      <td>2.1940</td>
      <td>1.6910</td>
      <td>2.12320</td>
      <td>2.15860</td>
      <td>1.6910</td>
      <td>2.4630</td>
      <td>Q9U2V9</td>
    </tr>
    <tr>
      <th>G5ECL3</th>
      <td>1.1710</td>
      <td>0.8818</td>
      <td>1.0340</td>
      <td>0.9105</td>
      <td>0.7678</td>
      <td>0.95302</td>
      <td>0.93176</td>
      <td>0.7678</td>
      <td>1.1710</td>
      <td>G5ECL3</td>
    </tr>
    <tr>
      <th>Q9N588</th>
      <td>0.7893</td>
      <td>1.7660</td>
      <td>1.3230</td>
      <td>1.0530</td>
      <td>0.3292</td>
      <td>1.05210</td>
      <td>1.05255</td>
      <td>0.3292</td>
      <td>1.7660</td>
      <td>Q9N588</td>
    </tr>
    <tr>
      <th>Q20636</th>
      <td>1.0430</td>
      <td>1.0030</td>
      <td>1.0030</td>
      <td>1.1770</td>
      <td>0.8978</td>
      <td>1.02476</td>
      <td>1.01388</td>
      <td>0.8978</td>
      <td>1.1770</td>
      <td>Q20636</td>
    </tr>
    <tr>
      <th>Q9TZC4</th>
      <td>1.0920</td>
      <td>1.2220</td>
      <td>1.1830</td>
      <td>1.1560</td>
      <td>1.2520</td>
      <td>1.18100</td>
      <td>1.18200</td>
      <td>1.0920</td>
      <td>1.2520</td>
      <td>Q9TZC4</td>
    </tr>
    <tr>
      <th>O62146</th>
      <td>10.1200</td>
      <td>8.2050</td>
      <td>7.9570</td>
      <td>7.8600</td>
      <td>9.6830</td>
      <td>8.76500</td>
      <td>8.48500</td>
      <td>7.8600</td>
      <td>10.1200</td>
      <td>O62146</td>
    </tr>
    <tr>
      <th>Q4PIU9</th>
      <td>3.3510</td>
      <td>3.4500</td>
      <td>3.2490</td>
      <td>3.4240</td>
      <td>3.0200</td>
      <td>3.29880</td>
      <td>3.32490</td>
      <td>3.0200</td>
      <td>3.4500</td>
      <td>Q4PIU9</td>
    </tr>
    <tr>
      <th>Q9TZD9</th>
      <td>0.9299</td>
      <td>0.8928</td>
      <td>0.9383</td>
      <td>0.9931</td>
      <td>0.9040</td>
      <td>0.93162</td>
      <td>0.93076</td>
      <td>0.8928</td>
      <td>0.9931</td>
      <td>Q9TZD9</td>
    </tr>
    <tr>
      <th>A0A1X7RC97</th>
      <td>1.1410</td>
      <td>1.0730</td>
      <td>1.0850</td>
      <td>0.9977</td>
      <td>0.9331</td>
      <td>1.04596</td>
      <td>1.05948</td>
      <td>0.9331</td>
      <td>1.1410</td>
      <td>A0A1X7RC97</td>
    </tr>
    <tr>
      <th>O02286</th>
      <td>18.3500</td>
      <td>19.1700</td>
      <td>19.4100</td>
      <td>19.6700</td>
      <td>18.8400</td>
      <td>19.08800</td>
      <td>19.12900</td>
      <td>18.3500</td>
      <td>19.6700</td>
      <td>O02286</td>
    </tr>
    <tr>
      <th>P19626</th>
      <td>11.8000</td>
      <td>11.2600</td>
      <td>11.6900</td>
      <td>12.4900</td>
      <td>11.4700</td>
      <td>11.74200</td>
      <td>11.71600</td>
      <td>11.2600</td>
      <td>12.4900</td>
      <td>P19626</td>
    </tr>
    <tr>
      <th>Q9NAN1</th>
      <td>0.8104</td>
      <td>0.7525</td>
      <td>0.6352</td>
      <td>0.7612</td>
      <td>0.7624</td>
      <td>0.74434</td>
      <td>0.75685</td>
      <td>0.6352</td>
      <td>0.8104</td>
      <td>Q9NAN1</td>
    </tr>
    <tr>
      <th>Q9N585</th>
      <td>0.5011</td>
      <td>0.8069</td>
      <td>0.4862</td>
      <td>0.5113</td>
      <td>0.6124</td>
      <td>0.58358</td>
      <td>0.54744</td>
      <td>0.4862</td>
      <td>0.8069</td>
      <td>Q9N585</td>
    </tr>
    <tr>
      <th>O17268</th>
      <td>1.0740</td>
      <td>0.9896</td>
      <td>0.9896</td>
      <td>1.0120</td>
      <td>0.9896</td>
      <td>1.01096</td>
      <td>1.00028</td>
      <td>0.9896</td>
      <td>1.0740</td>
      <td>O17268</td>
    </tr>
    <tr>
      <th>P90795</th>
      <td>0.7129</td>
      <td>1.0050</td>
      <td>0.9680</td>
      <td>0.4897</td>
      <td>0.3489</td>
      <td>0.70490</td>
      <td>0.70890</td>
      <td>0.3489</td>
      <td>1.0050</td>
      <td>P90795</td>
    </tr>
    <tr>
      <th>Q20228</th>
      <td>10.8100</td>
      <td>11.1400</td>
      <td>11.3000</td>
      <td>11.2300</td>
      <td>12.2800</td>
      <td>11.35200</td>
      <td>11.26500</td>
      <td>10.8100</td>
      <td>12.2800</td>
      <td>Q20228</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Triqler is already run with a FRD treshold

#sns ts plot to to visualize diff
ax = sub_sample_s.plot(x="protein", y = ["mean", "median"])
plt.fill_between(x = "protein", y1 = "min", y2 = "max", data = sub_sample_s, facecolor='green')
plt.title("Spectronaut - random samples")

ax = sub_sample_t.plot(x="protein", y = ["mean", "median"])
plt.fill_between(x = "protein", y1 = "min", y2 = "max", data = sub_sample_t, facecolor='green')
plt.title("Triqler - random samples")

```




    Text(0.5,1,'Triqler - random samples')




    
![png](output_15_1.png)
    



    
![png](output_15_2.png)
    


Code reads in triqler and spectronaut data. Removed decoy proteins. Compute mean, median, min, max and code plot function for mean and median (as lines) and fill-in with min-max borders. 

The code samples n random overlapping proteins from triqler and spectroanut and plots mean and median with min-max borders. 

Things to check in the code:
- Did i forget to treshold triqler data on q-values?
- What is the unit of triqler protein quantification? (Why is there a magnitude of difference)
- What was the normalization used in previous attempt? (within sample normalization, and why did that make sense?)
- Is there a better way to compare than the previous normalization?
- I guess it is between sample relationship that matter?
- Read up on spike-in proteomics? 


## 2020-12-02




```python
os.chdir("/home/ptruong/git/bayesMS/bin")
```


```python
import os 

import pandas as pd
import numpy as np 

```


```python
from read_triqler_output import read_triqler_protein_output_to_df
from triqler_output_df_melter import melt_spectronaut_triqler_formatted, melt_triqler_output
```


```python
# data dir /home/ptruong/git/bayesMS/data/old_data_pickled
```


```python
os.chdir("/home/ptruong/git/bayesMS/data/old_data_pickled")
```


```python
os.listdir()
```




    ['triqler.pkl',
     'spectronaut.pkl',
     'triqlerParams.txt',
     'spectronautParams.txt']




```python
spec = pd.read_pickle(r'spectronaut.pkl')
triq = pd.read_pickle(r'triqler.pkl')

```

Note: To read triqler output data we need to use 

from read_triqler_output import read_triqler_protein_output_to_df

because the peptide seperation is the same as tab-seperation.


```python
os.chdir("/home/ptruong/git/bayesMS/data/triqlerResults_largeScale_minSamp20_FC0_8_adjInt")
```


```python
os.listdir()
```




    ['proteins.6vs8.tsv',
     'proteins.5vs9.tsv',
     'proteins.3vs5.tsv',
     'proteins.4vs10.tsv',
     'proteins.3vs10.tsv',
     'proteins.1vs4.tsv',
     'proteins.5vs6.tsv',
     'proteins.2vs8.tsv',
     'proteins.4vs6.tsv',
     'proteins.2vs6.tsv',
     'proteins.9vs10.tsv',
     'proteins.2vs3.tsv',
     'proteins.7vs8.tsv',
     'proteins.1vs2.tsv',
     'proteins.3vs8.tsv',
     'proteins.3vs6.tsv',
     'proteins.1vs8.tsv',
     'proteins.6vs10.tsv',
     'proteins.5vs10.tsv',
     'proteins.3vs4.tsv',
     'proteins.7vs9.tsv',
     'proteins.1vs7.tsv',
     'proteins.2vs10.tsv',
     'proteins.3vs7.tsv',
     'proteins.8vs9.tsv',
     'proteins.4vs7.tsv',
     'proteins.7vs10.tsv',
     'proteins.2vs7.tsv',
     'proteins.6vs9.tsv',
     'proteins.1vs10.tsv',
     'proteins.4vs9.tsv',
     'proteins.5vs8.tsv',
     'proteins.2vs5.tsv',
     'proteins.1vs9.tsv',
     'proteins.1vs3.tsv',
     'proteins.5vs7.tsv',
     'proteins.1vs6.tsv',
     'proteins.2vs9.tsv',
     'proteins.3vs9.tsv',
     'proteins.6vs7.tsv',
     'proteins.8vs10.tsv',
     'proteins.4vs5.tsv',
     'proteins.4vs8.tsv',
     'proteins.1vs5.tsv',
     'proteins.2vs4.tsv']




```python
triq = read_triqler_protein_output_to_df('proteins.3vs8.tsv')
```


```python
spec.columns
```




    Index(['id', 'specie', 'protein', 'S01:S01_R01', 'S01:S01_R02', 'S01:S01_R03',
           'S01:S01_R04', 'S01:S01_R05', 'S02:S02_R01', 'S02:S02_R02',
           'S02:S02_R03', 'S02:S02_R04', 'S02:S02_R05', 'S03:S03_R01',
           'S03:S03_R02', 'S03:S03_R03', 'S03:S03_R05', 'S03:S04_R05',
           'S04:S04_R01', 'S04:S04_R02', 'S04:S04_R03', 'S04:S04_R04',
           'S04:S04_R05', 'S05:S05_R01', 'S05:S05_R02', 'S05:S05_R03',
           'S05:S05_R04', 'S05:S05_R05', 'S06:S06_R01', 'S06:S06_R02',
           'S06:S06_R03', 'S06:S06_R04', 'S06:S06_R05', 'S07:S07_R01',
           'S07:S07_R02', 'S07:S07_R03', 'S07:S07_R04', 'S07:S07_R05',
           'S08:S08_R01', 'S08:S08_R02', 'S08:S08_R03', 'S08:S08_R04',
           'S08:S08_R05', 'S09:S09_R01', 'S09:S09_R02', 'S09:S09_R03',
           'S09:S09_R04', 'S09:S09_R05', 'S10:S10_R01', 'S10:S10_R02',
           'S10:S10_R03', 'S10:S10_R04', 'S10:S10_R05'],
          dtype='object')



We notice naming error and rename the column S03:S04_R05 to S03:S03_R05


```python
spec = spec.rename(columns={'S03:S04_R05': 'S03:S03_R04'})
```

triqler and spectroanut raw data is presented below. Both data set with 0.01 FDR treshold. 



```python
spec
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>specie</th>
      <th>protein</th>
      <th>S01:S01_R01</th>
      <th>S01:S01_R02</th>
      <th>S01:S01_R03</th>
      <th>S01:S01_R04</th>
      <th>S01:S01_R05</th>
      <th>S02:S02_R01</th>
      <th>S02:S02_R02</th>
      <th>...</th>
      <th>S09:S09_R01</th>
      <th>S09:S09_R02</th>
      <th>S09:S09_R03</th>
      <th>S09:S09_R04</th>
      <th>S09:S09_R05</th>
      <th>S10:S10_R01</th>
      <th>S10:S10_R02</th>
      <th>S10:S10_R03</th>
      <th>S10:S10_R04</th>
      <th>S10:S10_R05</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>203877.890625</td>
      <td>190713.625000</td>
      <td>195925.703125</td>
      <td>150170.421875</td>
      <td>163190.718750</td>
      <td>97127.828125</td>
      <td>195944.765625</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>767819.750000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>decoy_A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>decoy_A0A023T4K3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A0A061ACH4_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A061ACH4</td>
      <td>8781.009766</td>
      <td>10325.387695</td>
      <td>10948.747070</td>
      <td>8789.944336</td>
      <td>11853.339844</td>
      <td>72.113838</td>
      <td>3990.177002</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A0A061ACL3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A061ACL3</td>
      <td>298404.781250</td>
      <td>296928.375000</td>
      <td>309051.406250</td>
      <td>325567.562500</td>
      <td>277911.718750</td>
      <td>144550.265625</td>
      <td>142709.437500</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A0A061ACR1_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A061ACR1</td>
      <td>336096.625000</td>
      <td>354560.000000</td>
      <td>378152.875000</td>
      <td>359206.312500</td>
      <td>387415.562500</td>
      <td>187493.328125</td>
      <td>200906.875000</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>15009</th>
      <td>V6CLV0_CAEEL</td>
      <td>CAEEL</td>
      <td>V6CLV0</td>
      <td>803615.500000</td>
      <td>860085.062500</td>
      <td>897633.250000</td>
      <td>971245.750000</td>
      <td>834293.187500</td>
      <td>400180.968750</td>
      <td>399113.750000</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>15010</th>
      <td>V6CM07_CAEEL</td>
      <td>CAEEL</td>
      <td>V6CM07</td>
      <td>18498.939453</td>
      <td>21163.210938</td>
      <td>19706.724609</td>
      <td>28860.738281</td>
      <td>16341.950195</td>
      <td>13379.542969</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>15011</th>
      <td>X5JA13_ARATH</td>
      <td>ARATH</td>
      <td>X5JA13</td>
      <td>141788.171875</td>
      <td>102453.429688</td>
      <td>97403.984375</td>
      <td>92313.593750</td>
      <td>101041.617188</td>
      <td>125743.546875</td>
      <td>114827.593750</td>
      <td>...</td>
      <td>164211.046875</td>
      <td>85307.000000</td>
      <td>88487.984375</td>
      <td>95901.960938</td>
      <td>81865.812500</td>
      <td>127238.65625</td>
      <td>110625.953125</td>
      <td>98996.132812</td>
      <td>98382.304688</td>
      <td>81635.281250</td>
    </tr>
    <tr>
      <th>15012</th>
      <td>X5JB51_ARATH</td>
      <td>ARATH</td>
      <td>X5JB51</td>
      <td>509657.687500</td>
      <td>625327.125000</td>
      <td>9751.568359</td>
      <td>4141.071289</td>
      <td>25130.304688</td>
      <td>55028.699219</td>
      <td>140951.250000</td>
      <td>...</td>
      <td>164315.000000</td>
      <td>51476.402344</td>
      <td>46677.218750</td>
      <td>41652.757812</td>
      <td>7216.791992</td>
      <td>36751.68750</td>
      <td>59819.433594</td>
      <td>46432.910156</td>
      <td>3826.284180</td>
      <td>48352.703125</td>
    </tr>
    <tr>
      <th>15013</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>NaN</td>
      <td>27413.113281</td>
      <td>21796.166016</td>
      <td>8100.251465</td>
      <td>64.185448</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>370496.218750</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>15014 rows × 53 columns</p>
</div>




```python
triq
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>q_value</th>
      <th>posterior_error_prob</th>
      <th>num_peptides</th>
      <th>protein_id_posterior_error_prob</th>
      <th>log2_fold_change</th>
      <th>diff_exp_prob_1.0</th>
      <th>S01:S01_R01</th>
      <th>S01:S01_R02</th>
      <th>S01:S01_R03</th>
      <th>S01:S01_R04</th>
      <th>...</th>
      <th>S10:S10_R02</th>
      <th>S10:S10_R03</th>
      <th>S10:S10_R04</th>
      <th>S10:S10_R05</th>
      <th>peptides</th>
      <th>specie</th>
      <th>decoy</th>
      <th>id</th>
      <th>protein</th>
      <th>FDR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.284000e-10</td>
      <td>1.284000e-10</td>
      <td>465</td>
      <td>1.284000e-10</td>
      <td>-11.47000</td>
      <td>2.924000e-15</td>
      <td>0.000238</td>
      <td>0.000244</td>
      <td>0.000480</td>
      <td>0.000195</td>
      <td>...</td>
      <td>2.4480</td>
      <td>2.4250</td>
      <td>2.5010</td>
      <td>2.4420</td>
      <td>VKMPDVDISVPK|FKMPFLSISSPK|FKMPEINIK|ISM[16]SEV...</td>
      <td>HUMAN</td>
      <td>False</td>
      <td>Q09666_HUMAN</td>
      <td>Q09666</td>
      <td>1.284000e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.420000e-10</td>
      <td>1.556000e-10</td>
      <td>421</td>
      <td>1.556000e-10</td>
      <td>-10.43000</td>
      <td>8.442000e-14</td>
      <td>0.000804</td>
      <td>0.000450</td>
      <td>0.000397</td>
      <td>0.000422</td>
      <td>...</td>
      <td>2.4030</td>
      <td>2.2490</td>
      <td>2.2650</td>
      <td>2.3440</td>
      <td>SLQEEHVAVAQLR|EAEQEAARR|KQEELQQLEQQR|TISLVIR|I...</td>
      <td>HUMAN</td>
      <td>False</td>
      <td>Q15149_HUMAN</td>
      <td>Q15149</td>
      <td>1.420000e-10</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2.176000e-10</td>
      <td>3.686000e-10</td>
      <td>311</td>
      <td>3.686000e-10</td>
      <td>-10.21000</td>
      <td>2.266000e-14</td>
      <td>0.000641</td>
      <td>0.000293</td>
      <td>0.000492</td>
      <td>0.001091</td>
      <td>...</td>
      <td>2.4610</td>
      <td>2.2850</td>
      <td>2.3040</td>
      <td>2.2670</td>
      <td>EM[16]KPVIFLDVFLPR|LLNFLMK|NLLIFENLIDLKR|YKEVY...</td>
      <td>HUMAN</td>
      <td>False</td>
      <td>P78527-2_HUMAN</td>
      <td>P78527-2</td>
      <td>2.175333e-10</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2.622000e-10</td>
      <td>3.960000e-10</td>
      <td>314</td>
      <td>3.936000e-10</td>
      <td>-9.47600</td>
      <td>2.345000e-12</td>
      <td>0.001133</td>
      <td>0.000662</td>
      <td>0.000671</td>
      <td>0.001489</td>
      <td>...</td>
      <td>2.2670</td>
      <td>2.1890</td>
      <td>2.1260</td>
      <td>2.0830</td>
      <td>LKVNFLPEIITLSK|LSLSNAISTALPLTQLR|INMLVIELK|WAI...</td>
      <td>HUMAN</td>
      <td>False</td>
      <td>Q14204_HUMAN</td>
      <td>Q14204</td>
      <td>2.615500e-10</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5.753000e-10</td>
      <td>1.204000e-09</td>
      <td>238</td>
      <td>1.183000e-09</td>
      <td>-8.84800</td>
      <td>2.112000e-11</td>
      <td>0.001145</td>
      <td>0.002007</td>
      <td>0.001241</td>
      <td>0.001354</td>
      <td>...</td>
      <td>2.2320</td>
      <td>2.0110</td>
      <td>1.9700</td>
      <td>2.0390</td>
      <td>GRSEADSDKNATILELR|NGVGTSSSMGSGVSDDVFSSSR|NLPLA...</td>
      <td>HUMAN</td>
      <td>False</td>
      <td>P15924_HUMAN</td>
      <td>P15924</td>
      <td>4.458400e-10</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>9425</th>
      <td>5.113000e-01</td>
      <td>9.990000e-01</td>
      <td>3</td>
      <td>1.116000e-01</td>
      <td>0.21620</td>
      <td>9.989000e-01</td>
      <td>1.135000</td>
      <td>1.156000</td>
      <td>1.031000</td>
      <td>1.021000</td>
      <td>...</td>
      <td>1.0090</td>
      <td>1.0090</td>
      <td>1.0090</td>
      <td>1.0090</td>
      <td>ESGDQLSVSR|GIGLGLVQQLVK|NAALTVEQSTAELISSFNK</td>
      <td>CAEEL</td>
      <td>False</td>
      <td>P90780_CAEEL</td>
      <td>P90780</td>
      <td>9.970788e-03</td>
    </tr>
    <tr>
      <th>6074</th>
      <td>2.684000e-01</td>
      <td>9.112000e-01</td>
      <td>1</td>
      <td>1.118000e-01</td>
      <td>0.27480</td>
      <td>9.000000e-01</td>
      <td>1.920000</td>
      <td>2.049000</td>
      <td>1.938000</td>
      <td>2.441000</td>
      <td>...</td>
      <td>0.9519</td>
      <td>0.9519</td>
      <td>0.9519</td>
      <td>0.9519</td>
      <td>RIGYGIK</td>
      <td>CAEEL</td>
      <td>False</td>
      <td>Q9TVW5_CAEEL</td>
      <td>Q9TVW5</td>
      <td>9.977931e-03</td>
    </tr>
    <tr>
      <th>11844</th>
      <td>5.984000e-01</td>
      <td>9.999000e-01</td>
      <td>3</td>
      <td>1.119000e-01</td>
      <td>0.02839</td>
      <td>9.999000e-01</td>
      <td>0.988800</td>
      <td>0.981800</td>
      <td>0.988800</td>
      <td>0.988800</td>
      <td>...</td>
      <td>1.0370</td>
      <td>1.0370</td>
      <td>0.8964</td>
      <td>1.1400</td>
      <td>VACGEGATTEKRPAEAAVEL|DLKIPSEDLSNLVEQCLEK|SFEYC...</td>
      <td>HUMAN</td>
      <td>True</td>
      <td>decoy_O96017_HUMAN</td>
      <td>O96017</td>
      <td>9.985081e-03</td>
    </tr>
    <tr>
      <th>9835</th>
      <td>5.295000e-01</td>
      <td>9.994000e-01</td>
      <td>3</td>
      <td>1.121000e-01</td>
      <td>-0.06439</td>
      <td>9.994000e-01</td>
      <td>0.904700</td>
      <td>0.831100</td>
      <td>0.747000</td>
      <td>0.765600</td>
      <td>...</td>
      <td>1.0830</td>
      <td>1.0660</td>
      <td>1.0940</td>
      <td>1.0090</td>
      <td>TGAALLIVPR|VVDTETGISLPR|SQGSQLTEDDVK</td>
      <td>ARATH</td>
      <td>False</td>
      <td>Q9LU36_ARATH</td>
      <td>Q9LU36</td>
      <td>9.992243e-03</td>
    </tr>
    <tr>
      <th>14934</th>
      <td>6.686000e-01</td>
      <td>1.000000e+00</td>
      <td>1</td>
      <td>1.122000e-01</td>
      <td>-0.04344</td>
      <td>1.000000e+00</td>
      <td>1.076000</td>
      <td>1.089000</td>
      <td>1.083000</td>
      <td>0.895800</td>
      <td>...</td>
      <td>1.0540</td>
      <td>1.0590</td>
      <td>1.0180</td>
      <td>0.9144</td>
      <td>AVLTLSK</td>
      <td>CAEEL</td>
      <td>False</td>
      <td>P34479_CAEEL</td>
      <td>P34479</td>
      <td>9.999411e-03</td>
    </tr>
  </tbody>
</table>
<p>14258 rows × 62 columns</p>
</div>



The reported protein expressions per run are the expected value of the protein's expression in that run. They represent relative values (not log transformed) to the protein's mean expression across all runs, which itself would correspond to the value 1.0. For example, a value of 1.5 means that the expression in this sample is 50% higher than the mean across all runs. A second example comparing values across samples: if sample1 has a value of 2.0 and sample2 a value of 1.5, it means that the expression in sample1 is 33% higher than in sample2 (2.0/1.5=1.33). We don't necessarily recommend using these values for downstream analysis, as the idea is that the actual value of interest is the fold change between treatment groups rather than between samples.

The triqler proteins are relative values, so we need to transform spectroanut values to relative values.

We should also treshold the triqler results on protein_id_posterior_error_prob


```python
print(sum(triq.protein_id_posterior_error_prob < 0.01))
```

    11162



```python
print("%s : %i" % ("triqler number of protein ids", int(sum(triq.protein_id_posterior_error_prob < 0.01))))
print("%s : %i" % ("spectronaut number of protein ids", int(len(spec))))
```

    triqler number of protein ids : 11162
    spectronaut number of protein ids : 15014


Spectronaut has higher than protein count, but looking at the data above we can see that there are plenty of NaN among samples in the spectronaut. We need to fix this.

We could do this by saying that proteins with more than 2 or 3 NaN in a samples if left out. 

We wrangle triq and spec data to melted df for easier data manipulation. Scripts for this can be found in 

"from triqler_output_df_melter import melt_spectronaut_triqler_formatted, melt_triqler_output"




```python
triq = melt_triqler_output(triq)
spec = melt_spectronaut_triqler_formatted(spec)
```


```python
spec
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>specie</th>
      <th>protein</th>
      <th>sample</th>
      <th>run</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R01</td>
      <td>203877.890625</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R02</td>
      <td>190713.625000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R03</td>
      <td>195925.703125</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R04</td>
      <td>150170.421875</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R05</td>
      <td>163190.718750</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>750695</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R01</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750696</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R02</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750697</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R03</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750698</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R04</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750699</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R05</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>750700 rows × 6 columns</p>
</div>




```python
spec
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>specie</th>
      <th>protein</th>
      <th>sample</th>
      <th>run</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R01</td>
      <td>203877.890625</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R02</td>
      <td>190713.625000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R03</td>
      <td>195925.703125</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R04</td>
      <td>150170.421875</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R05</td>
      <td>163190.718750</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>750695</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R01</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750696</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R02</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750697</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R03</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750698</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R04</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750699</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R05</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>750700 rows × 6 columns</p>
</div>



Now, we can work with the melted dataframes.


### Summary :
- made script for reading in triqler output.
- melting script implemented.
- run jobs on kebnekaise with posterior distributions output and default parameters.
- run jobs on kebnekaise with posterior distributions output and min_samples = 10.
- run jobs on kebnekaise with posterior distributions output and min_samples = 1 (Failed: min_samples must be >= 2).

### To do:
- check posterior distribution output format.
- figure out how posterior distribution heatmap plotting works in triqler.
- think about normalization for melted dataframes spec and triq.



## 2020-12-03


Job run on kebnekaise failed because due to exceeding storage. I did wrong in using the storage project. I've contacted the SNIC service to ask for guidance in this. 

Day has been spent writing on Project description.



# Raw data



```python
os.chdir("/home/ptruong/git/bayesMS/data")
```


```python
os.listdir()
```




    ['triqlerResults_largeScale_minSamp20_FC0_8_adjInt',
     'triqler_default_params',
     'PSSS3_raw_sample_top_100000.csv',
     'Headers.xlsx',
     'old_data_pickled']




```python
df = pd.read_csv("PSSS3_raw_sample_top_100000.csv", sep = "\t")
```


```python
df

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>R.Condition</th>
      <th>R.FileName</th>
      <th>PG.Organisms</th>
      <th>PG.ProteinAccessions</th>
      <th>PG.Cscore</th>
      <th>PG.NrOfStrippedSequencesIdentified</th>
      <th>PG.Qvalue</th>
      <th>PG.Quantity</th>
      <th>EG.StrippedSequence</th>
      <th>EG.IsDecoy</th>
      <th>EG.PrecursorId</th>
      <th>EG.PEP</th>
      <th>EG.Qvalue</th>
      <th>EG.Cscore</th>
      <th>FG.NormalizedMS2PeakArea</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Caenorhabditis elegans OX=6239</td>
      <td>A0A023T4K3</td>
      <td>0.182511</td>
      <td>2</td>
      <td>0.000646</td>
      <td>377452.156250</td>
      <td>SFYYLVQDLK</td>
      <td>False</td>
      <td>_SFYYLVQDLK_.2</td>
      <td>0.014793</td>
      <td>0.003878</td>
      <td>2.355977</td>
      <td>731908.023851</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Caenorhabditis elegans OX=6239</td>
      <td>A0A023T4K3</td>
      <td>0.182511</td>
      <td>2</td>
      <td>0.000646</td>
      <td>377452.156250</td>
      <td>EATVSESVLSELKR</td>
      <td>False</td>
      <td>_EATVSESVLSELKR_.3</td>
      <td>0.022104</td>
      <td>0.005114</td>
      <td>2.073540</td>
      <td>22996.253835</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Caenorhabditis elegans OX=6239</td>
      <td>A0A023T4K3</td>
      <td>0.182511</td>
      <td>2</td>
      <td>0.000646</td>
      <td>377452.156250</td>
      <td>EATVSESVLSELKR</td>
      <td>False</td>
      <td>_EATVSESVLSELKR_.2</td>
      <td>1.000000</td>
      <td>0.762912</td>
      <td>-2.174942</td>
      <td>42741.205204</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Caenorhabditis elegans OX=6239</td>
      <td>A0A023T4K3</td>
      <td>0.182511</td>
      <td>2</td>
      <td>0.000646</td>
      <td>377452.156250</td>
      <td>AADFYVR</td>
      <td>False</td>
      <td>_AADFYVR_.2</td>
      <td>0.009466</td>
      <td>0.015673</td>
      <td>1.283862</td>
      <td>36317.379819</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Caenorhabditis elegans OX=6239</td>
      <td>A0A023T4K3</td>
      <td>0.182511</td>
      <td>2</td>
      <td>0.000646</td>
      <td>377452.156250</td>
      <td>IGALADVNNSKDPDGLR</td>
      <td>False</td>
      <td>_IGALADVNNSKDPDGLR_.3</td>
      <td>0.422581</td>
      <td>0.102376</td>
      <td>0.036027</td>
      <td>22531.007700</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>99995</th>
      <td>99995</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Arabidopsis thaliana</td>
      <td>O23044</td>
      <td>0.304250</td>
      <td>7</td>
      <td>0.000407</td>
      <td>48658.785156</td>
      <td>GLFQSDSALTTNPTTLSNINR</td>
      <td>False</td>
      <td>_GLFQSDSALTTNPTTLSNINR_.2</td>
      <td>0.377402</td>
      <td>0.064631</td>
      <td>-0.746827</td>
      <td>9815.095549</td>
    </tr>
    <tr>
      <th>99996</th>
      <td>99996</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Arabidopsis thaliana</td>
      <td>O23044</td>
      <td>0.304250</td>
      <td>7</td>
      <td>0.000407</td>
      <td>48658.785156</td>
      <td>KTFDLSYYQLVLK</td>
      <td>False</td>
      <td>_KTFDLSYYQLVLK_.2</td>
      <td>0.862989</td>
      <td>0.246905</td>
      <td>-1.849602</td>
      <td>70103.139684</td>
    </tr>
    <tr>
      <th>99997</th>
      <td>99997</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Arabidopsis thaliana</td>
      <td>O23044</td>
      <td>NaN</td>
      <td>11</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TGAVGVSR</td>
      <td>True</td>
      <td>_TGAVGVSR_.2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-2.336857</td>
      <td>4658.170465</td>
    </tr>
    <tr>
      <th>99998</th>
      <td>99998</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Arabidopsis thaliana</td>
      <td>O23044</td>
      <td>NaN</td>
      <td>11</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ALTNPDTVR</td>
      <td>True</td>
      <td>_ALTNPDTVR_.2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-1.404710</td>
      <td>8258.498615</td>
    </tr>
    <tr>
      <th>99999</th>
      <td>99999</td>
      <td>S500-PSSS3-S04</td>
      <td>G_D180330_S500-PSSS3-S04_MHRM_R03_T0</td>
      <td>Arabidopsis thaliana</td>
      <td>O23044</td>
      <td>NaN</td>
      <td>11</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>FDGGIFAIK</td>
      <td>True</td>
      <td>_FDGGIFAIK_.2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-1.539223</td>
      <td>3918.578812</td>
    </tr>
  </tbody>
</table>
<p>100000 rows × 16 columns</p>
</div>



## 2020-12-07 Exploring posteriors data




```python
import os

os.chdir("/home/ptruong/git/bayesMS/data/triqler_default_params_posterios")
```


```python
os.listdir()
```




    ['proteins.6vs8.tsv',
     'proteins.5vs9.tsv',
     'proteins.3vs5.tsv',
     'proteins.4vs10.tsv',
     'proteins.3vs10.tsv',
     'proteins.1vs4.tsv',
     'proteins.5vs6.tsv',
     'proteins.2vs8.tsv',
     'proteins.4vs6.tsv',
     'proteins.2vs6.tsv',
     'proteins.9vs10.tsv',
     'proteins.2vs3.tsv',
     'proteins.7vs8.tsv',
     'proteins.1vs2.tsv',
     'proteins.3vs8.tsv',
     'proteins.3vs6.tsv',
     'proteins.1vs8.tsv',
     'proteins.6vs10.tsv',
     'proteins.5vs10.tsv',
     'proteins.3vs4.tsv',
     'proteins.7vs9.tsv',
     'proteins.1vs7.tsv',
     'F_OUT',
     'proteins.2vs10.tsv',
     'proteins.3vs7.tsv',
     'proteins.8vs9.tsv',
     'proteins.4vs7.tsv',
     'proteins.7vs10.tsv',
     'proteins.2vs7.tsv',
     'proteins.6vs9.tsv',
     'proteins.1vs10.tsv',
     'proteins.4vs9.tsv',
     'proteins.5vs8.tsv',
     'proteins.2vs5.tsv',
     'G_OUT',
     'proteins.1vs9.tsv',
     'proteins.1vs3.tsv',
     'proteins.5vs7.tsv',
     'proteins.1vs6.tsv',
     'proteins.2vs9.tsv',
     'proteins.3vs9.tsv',
     'proteins.6vs7.tsv',
     'proteins.8vs10.tsv',
     'proteins.4vs5.tsv',
     'P_OUT',
     'proteins.4vs8.tsv',
     'proteins.1vs5.tsv',
     'proteins.2vs4.tsv']




```python
import pandas as pd
import numpy as np
```


```python
df = pd.read_csv("P_OUT", sep = "\t")
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>protein</th>
      <th>group:run</th>
      <th>-5</th>
      <th>-4.99</th>
      <th>-4.98</th>
      <th>-4.97</th>
      <th>-4.96</th>
      <th>-4.95</th>
      <th>-4.94</th>
      <th>-4.93</th>
      <th>...</th>
      <th>4.91</th>
      <th>4.92</th>
      <th>4.93</th>
      <th>4.94</th>
      <th>4.95</th>
      <th>4.96</th>
      <th>4.97</th>
      <th>4.98</th>
      <th>4.99</th>
      <th>5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S01:S01_R01</td>
      <td>7.645000e-40</td>
      <td>8.081000e-40</td>
      <td>8.542000e-40</td>
      <td>9.029000e-40</td>
      <td>9.544000e-40</td>
      <td>1.009000e-39</td>
      <td>1.066000e-39</td>
      <td>1.127000e-39</td>
      <td>...</td>
      <td>2.770000e-36</td>
      <td>2.482000e-36</td>
      <td>2.225000e-36</td>
      <td>1.995000e-36</td>
      <td>1.789000e-36</td>
      <td>1.605000e-36</td>
      <td>1.440000e-36</td>
      <td>1.292000e-36</td>
      <td>1.160000e-36</td>
      <td>1.042000e-36</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S01:S01_R02</td>
      <td>3.036000e-40</td>
      <td>3.209000e-40</td>
      <td>3.392000e-40</td>
      <td>3.586000e-40</td>
      <td>3.790000e-40</td>
      <td>4.006000e-40</td>
      <td>4.235000e-40</td>
      <td>4.476000e-40</td>
      <td>...</td>
      <td>7.363000e-37</td>
      <td>6.611000e-37</td>
      <td>5.938000e-37</td>
      <td>5.335000e-37</td>
      <td>4.793000e-37</td>
      <td>4.308000e-37</td>
      <td>3.872000e-37</td>
      <td>3.481000e-37</td>
      <td>3.130000e-37</td>
      <td>2.815000e-37</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S01:S01_R03</td>
      <td>7.332000e-40</td>
      <td>7.750000e-40</td>
      <td>8.192000e-40</td>
      <td>8.659000e-40</td>
      <td>9.153000e-40</td>
      <td>9.675000e-40</td>
      <td>1.023000e-39</td>
      <td>1.081000e-39</td>
      <td>...</td>
      <td>2.311000e-36</td>
      <td>2.060000e-36</td>
      <td>1.836000e-36</td>
      <td>1.638000e-36</td>
      <td>1.461000e-36</td>
      <td>1.304000e-36</td>
      <td>1.164000e-36</td>
      <td>1.040000e-36</td>
      <td>9.296000e-37</td>
      <td>8.310000e-37</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S01:S01_R04</td>
      <td>9.449000e-44</td>
      <td>9.988000e-44</td>
      <td>1.056000e-43</td>
      <td>1.116000e-43</td>
      <td>1.180000e-43</td>
      <td>1.247000e-43</td>
      <td>1.318000e-43</td>
      <td>1.393000e-43</td>
      <td>...</td>
      <td>2.771000e-40</td>
      <td>2.479000e-40</td>
      <td>2.219000e-40</td>
      <td>1.987000e-40</td>
      <td>1.779000e-40</td>
      <td>1.594000e-40</td>
      <td>1.428000e-40</td>
      <td>1.280000e-40</td>
      <td>1.148000e-40</td>
      <td>1.030000e-40</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S01:S01_R05</td>
      <td>1.423000e-35</td>
      <td>1.504000e-35</td>
      <td>1.590000e-35</td>
      <td>1.681000e-35</td>
      <td>1.777000e-35</td>
      <td>1.878000e-35</td>
      <td>1.985000e-35</td>
      <td>2.098000e-35</td>
      <td>...</td>
      <td>9.235000e-34</td>
      <td>8.348000e-34</td>
      <td>7.547000e-34</td>
      <td>6.825000e-34</td>
      <td>6.172000e-34</td>
      <td>5.582000e-34</td>
      <td>5.050000e-34</td>
      <td>4.569000e-34</td>
      <td>4.135000e-34</td>
      <td>3.742000e-34</td>
    </tr>
    <tr>
      <th>5</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S02:S02_R01</td>
      <td>1.345000e-30</td>
      <td>1.421000e-30</td>
      <td>1.502000e-30</td>
      <td>1.588000e-30</td>
      <td>1.679000e-30</td>
      <td>1.774000e-30</td>
      <td>1.876000e-30</td>
      <td>1.982000e-30</td>
      <td>...</td>
      <td>2.041000e-28</td>
      <td>1.842000e-28</td>
      <td>1.664000e-28</td>
      <td>1.502000e-28</td>
      <td>1.357000e-28</td>
      <td>1.225000e-28</td>
      <td>1.106000e-28</td>
      <td>9.995000e-29</td>
      <td>9.028000e-29</td>
      <td>8.156000e-29</td>
    </tr>
    <tr>
      <th>6</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S02:S02_R02</td>
      <td>5.609000e-34</td>
      <td>5.929000e-34</td>
      <td>6.267000e-34</td>
      <td>6.624000e-34</td>
      <td>7.002000e-34</td>
      <td>7.401000e-34</td>
      <td>7.823000e-34</td>
      <td>8.269000e-34</td>
      <td>...</td>
      <td>9.408000e-32</td>
      <td>8.481000e-32</td>
      <td>7.647000e-32</td>
      <td>6.896000e-32</td>
      <td>6.219000e-32</td>
      <td>5.609000e-32</td>
      <td>5.060000e-32</td>
      <td>4.565000e-32</td>
      <td>4.119000e-32</td>
      <td>3.717000e-32</td>
    </tr>
    <tr>
      <th>7</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S02:S02_R03</td>
      <td>5.444000e-35</td>
      <td>5.755000e-35</td>
      <td>6.083000e-35</td>
      <td>6.430000e-35</td>
      <td>6.796000e-35</td>
      <td>7.184000e-35</td>
      <td>7.594000e-35</td>
      <td>8.026000e-35</td>
      <td>...</td>
      <td>6.297000e-33</td>
      <td>5.672000e-33</td>
      <td>5.111000e-33</td>
      <td>4.606000e-33</td>
      <td>4.152000e-33</td>
      <td>3.743000e-33</td>
      <td>3.375000e-33</td>
      <td>3.044000e-33</td>
      <td>2.746000e-33</td>
      <td>2.477000e-33</td>
    </tr>
    <tr>
      <th>8</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S02:S02_R04</td>
      <td>2.411000e-35</td>
      <td>2.548000e-35</td>
      <td>2.693000e-35</td>
      <td>2.847000e-35</td>
      <td>3.009000e-35</td>
      <td>3.181000e-35</td>
      <td>3.362000e-35</td>
      <td>3.554000e-35</td>
      <td>...</td>
      <td>2.225000e-34</td>
      <td>2.037000e-34</td>
      <td>1.866000e-34</td>
      <td>1.711000e-34</td>
      <td>1.569000e-34</td>
      <td>1.441000e-34</td>
      <td>1.323000e-34</td>
      <td>1.216000e-34</td>
      <td>1.118000e-34</td>
      <td>1.029000e-34</td>
    </tr>
    <tr>
      <th>9</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S02:S02_R05</td>
      <td>1.096000e-29</td>
      <td>1.158000e-29</td>
      <td>1.224000e-29</td>
      <td>1.294000e-29</td>
      <td>1.368000e-29</td>
      <td>1.446000e-29</td>
      <td>1.528000e-29</td>
      <td>1.615000e-29</td>
      <td>...</td>
      <td>5.117000e-29</td>
      <td>4.766000e-29</td>
      <td>4.441000e-29</td>
      <td>4.141000e-29</td>
      <td>3.862000e-29</td>
      <td>3.604000e-29</td>
      <td>3.365000e-29</td>
      <td>3.143000e-29</td>
      <td>2.937000e-29</td>
      <td>2.746000e-29</td>
    </tr>
    <tr>
      <th>10</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S03:S03_R01</td>
      <td>7.973000e-21</td>
      <td>8.427000e-21</td>
      <td>8.908000e-21</td>
      <td>9.415000e-21</td>
      <td>9.952000e-21</td>
      <td>1.052000e-20</td>
      <td>1.112000e-20</td>
      <td>1.175000e-20</td>
      <td>...</td>
      <td>2.547000e-20</td>
      <td>2.406000e-20</td>
      <td>2.274000e-20</td>
      <td>2.149000e-20</td>
      <td>2.031000e-20</td>
      <td>1.919000e-20</td>
      <td>1.814000e-20</td>
      <td>1.715000e-20</td>
      <td>1.621000e-20</td>
      <td>1.532000e-20</td>
    </tr>
    <tr>
      <th>11</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S03:S03_R02</td>
      <td>1.251000e-21</td>
      <td>1.323000e-21</td>
      <td>1.398000e-21</td>
      <td>1.478000e-21</td>
      <td>1.562000e-21</td>
      <td>1.651000e-21</td>
      <td>1.745000e-21</td>
      <td>1.845000e-21</td>
      <td>...</td>
      <td>3.976000e-21</td>
      <td>3.758000e-21</td>
      <td>3.552000e-21</td>
      <td>3.357000e-21</td>
      <td>3.174000e-21</td>
      <td>3.000000e-21</td>
      <td>2.836000e-21</td>
      <td>2.681000e-21</td>
      <td>2.535000e-21</td>
      <td>2.396000e-21</td>
    </tr>
    <tr>
      <th>12</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S03:S03_R03</td>
      <td>1.081000e-21</td>
      <td>1.143000e-21</td>
      <td>1.208000e-21</td>
      <td>1.277000e-21</td>
      <td>1.350000e-21</td>
      <td>1.427000e-21</td>
      <td>1.508000e-21</td>
      <td>1.594000e-21</td>
      <td>...</td>
      <td>3.377000e-21</td>
      <td>3.195000e-21</td>
      <td>3.022000e-21</td>
      <td>2.858000e-21</td>
      <td>2.703000e-21</td>
      <td>2.557000e-21</td>
      <td>2.419000e-21</td>
      <td>2.288000e-21</td>
      <td>2.164000e-21</td>
      <td>2.047000e-21</td>
    </tr>
    <tr>
      <th>13</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S03:S03_R04</td>
      <td>3.798000e-21</td>
      <td>4.015000e-21</td>
      <td>4.243000e-21</td>
      <td>4.485000e-21</td>
      <td>4.741000e-21</td>
      <td>5.011000e-21</td>
      <td>5.297000e-21</td>
      <td>5.599000e-21</td>
      <td>...</td>
      <td>1.206000e-20</td>
      <td>1.140000e-20</td>
      <td>1.078000e-20</td>
      <td>1.019000e-20</td>
      <td>9.628000e-21</td>
      <td>9.102000e-21</td>
      <td>8.604000e-21</td>
      <td>8.134000e-21</td>
      <td>7.690000e-21</td>
      <td>7.270000e-21</td>
    </tr>
    <tr>
      <th>14</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S03:S03_R05</td>
      <td>1.110000e-20</td>
      <td>1.174000e-20</td>
      <td>1.240000e-20</td>
      <td>1.311000e-20</td>
      <td>1.386000e-20</td>
      <td>1.465000e-20</td>
      <td>1.548000e-20</td>
      <td>1.637000e-20</td>
      <td>...</td>
      <td>3.493000e-20</td>
      <td>3.302000e-20</td>
      <td>3.123000e-20</td>
      <td>2.953000e-20</td>
      <td>2.792000e-20</td>
      <td>2.641000e-20</td>
      <td>2.497000e-20</td>
      <td>2.361000e-20</td>
      <td>2.233000e-20</td>
      <td>2.112000e-20</td>
    </tr>
    <tr>
      <th>15</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S04:S04_R01</td>
      <td>1.058000e-16</td>
      <td>1.118000e-16</td>
      <td>1.182000e-16</td>
      <td>1.249000e-16</td>
      <td>1.321000e-16</td>
      <td>1.396000e-16</td>
      <td>1.476000e-16</td>
      <td>1.560000e-16</td>
      <td>...</td>
      <td>3.293000e-16</td>
      <td>3.115000e-16</td>
      <td>2.947000e-16</td>
      <td>2.788000e-16</td>
      <td>2.637000e-16</td>
      <td>2.495000e-16</td>
      <td>2.360000e-16</td>
      <td>2.233000e-16</td>
      <td>2.112000e-16</td>
      <td>1.998000e-16</td>
    </tr>
    <tr>
      <th>16</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S04:S04_R02</td>
      <td>2.719000e-18</td>
      <td>2.875000e-18</td>
      <td>3.038000e-18</td>
      <td>3.212000e-18</td>
      <td>3.395000e-18</td>
      <td>3.588000e-18</td>
      <td>3.793000e-18</td>
      <td>4.009000e-18</td>
      <td>...</td>
      <td>8.460000e-18</td>
      <td>8.004000e-18</td>
      <td>7.572000e-18</td>
      <td>7.163000e-18</td>
      <td>6.777000e-18</td>
      <td>6.411000e-18</td>
      <td>6.065000e-18</td>
      <td>5.738000e-18</td>
      <td>5.428000e-18</td>
      <td>5.135000e-18</td>
    </tr>
    <tr>
      <th>17</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S04:S04_R03</td>
      <td>5.098000e-17</td>
      <td>5.389000e-17</td>
      <td>5.696000e-17</td>
      <td>6.021000e-17</td>
      <td>6.364000e-17</td>
      <td>6.727000e-17</td>
      <td>7.111000e-17</td>
      <td>7.516000e-17</td>
      <td>...</td>
      <td>1.585000e-16</td>
      <td>1.500000e-16</td>
      <td>1.419000e-16</td>
      <td>1.342000e-16</td>
      <td>1.270000e-16</td>
      <td>1.202000e-16</td>
      <td>1.137000e-16</td>
      <td>1.075000e-16</td>
      <td>1.017000e-16</td>
      <td>9.625000e-17</td>
    </tr>
    <tr>
      <th>18</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S04:S04_R04</td>
      <td>2.126000e-17</td>
      <td>2.247000e-17</td>
      <td>2.376000e-17</td>
      <td>2.511000e-17</td>
      <td>2.654000e-17</td>
      <td>2.806000e-17</td>
      <td>2.965000e-17</td>
      <td>3.135000e-17</td>
      <td>...</td>
      <td>6.612000e-17</td>
      <td>6.255000e-17</td>
      <td>5.918000e-17</td>
      <td>5.599000e-17</td>
      <td>5.297000e-17</td>
      <td>5.011000e-17</td>
      <td>4.741000e-17</td>
      <td>4.485000e-17</td>
      <td>4.243000e-17</td>
      <td>4.014000e-17</td>
    </tr>
    <tr>
      <th>19</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S04:S04_R05</td>
      <td>6.677000e-16</td>
      <td>7.058000e-16</td>
      <td>7.460000e-16</td>
      <td>7.885000e-16</td>
      <td>8.335000e-16</td>
      <td>8.810000e-16</td>
      <td>9.312000e-16</td>
      <td>9.843000e-16</td>
      <td>...</td>
      <td>2.076000e-15</td>
      <td>1.964000e-15</td>
      <td>1.858000e-15</td>
      <td>1.758000e-15</td>
      <td>1.663000e-15</td>
      <td>1.574000e-15</td>
      <td>1.489000e-15</td>
      <td>1.408000e-15</td>
      <td>1.332000e-15</td>
      <td>1.261000e-15</td>
    </tr>
    <tr>
      <th>20</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S05:S05_R01</td>
      <td>4.752000e-15</td>
      <td>5.023000e-15</td>
      <td>5.309000e-15</td>
      <td>5.612000e-15</td>
      <td>5.932000e-15</td>
      <td>6.270000e-15</td>
      <td>6.627000e-15</td>
      <td>7.005000e-15</td>
      <td>...</td>
      <td>1.478000e-14</td>
      <td>1.398000e-14</td>
      <td>1.322000e-14</td>
      <td>1.251000e-14</td>
      <td>1.184000e-14</td>
      <td>1.120000e-14</td>
      <td>1.059000e-14</td>
      <td>1.002000e-14</td>
      <td>9.482000e-15</td>
      <td>8.971000e-15</td>
    </tr>
    <tr>
      <th>21</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S05:S05_R02</td>
      <td>1.389000e-15</td>
      <td>1.468000e-15</td>
      <td>1.552000e-15</td>
      <td>1.640000e-15</td>
      <td>1.734000e-15</td>
      <td>1.833000e-15</td>
      <td>1.937000e-15</td>
      <td>2.047000e-15</td>
      <td>...</td>
      <td>4.319000e-15</td>
      <td>4.086000e-15</td>
      <td>3.865000e-15</td>
      <td>3.657000e-15</td>
      <td>3.460000e-15</td>
      <td>3.273000e-15</td>
      <td>3.096000e-15</td>
      <td>2.929000e-15</td>
      <td>2.771000e-15</td>
      <td>2.622000e-15</td>
    </tr>
    <tr>
      <th>22</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S05:S05_R03</td>
      <td>4.499000e-15</td>
      <td>4.755000e-15</td>
      <td>5.027000e-15</td>
      <td>5.313000e-15</td>
      <td>5.616000e-15</td>
      <td>5.936000e-15</td>
      <td>6.275000e-15</td>
      <td>6.632000e-15</td>
      <td>...</td>
      <td>1.399000e-14</td>
      <td>1.324000e-14</td>
      <td>1.252000e-14</td>
      <td>1.185000e-14</td>
      <td>1.121000e-14</td>
      <td>1.060000e-14</td>
      <td>1.003000e-14</td>
      <td>9.490000e-15</td>
      <td>8.978000e-15</td>
      <td>8.494000e-15</td>
    </tr>
    <tr>
      <th>23</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S05:S05_R04</td>
      <td>2.276000e-15</td>
      <td>2.406000e-15</td>
      <td>2.543000e-15</td>
      <td>2.688000e-15</td>
      <td>2.841000e-15</td>
      <td>3.003000e-15</td>
      <td>3.174000e-15</td>
      <td>3.355000e-15</td>
      <td>...</td>
      <td>7.077000e-15</td>
      <td>6.695000e-15</td>
      <td>6.334000e-15</td>
      <td>5.993000e-15</td>
      <td>5.669000e-15</td>
      <td>5.364000e-15</td>
      <td>5.074000e-15</td>
      <td>4.801000e-15</td>
      <td>4.542000e-15</td>
      <td>4.297000e-15</td>
    </tr>
    <tr>
      <th>24</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S05:S05_R05</td>
      <td>2.830000e-15</td>
      <td>2.992000e-15</td>
      <td>3.162000e-15</td>
      <td>3.343000e-15</td>
      <td>3.533000e-15</td>
      <td>3.735000e-15</td>
      <td>3.948000e-15</td>
      <td>4.173000e-15</td>
      <td>...</td>
      <td>8.802000e-15</td>
      <td>8.327000e-15</td>
      <td>7.878000e-15</td>
      <td>7.453000e-15</td>
      <td>7.051000e-15</td>
      <td>6.671000e-15</td>
      <td>6.311000e-15</td>
      <td>5.970000e-15</td>
      <td>5.648000e-15</td>
      <td>5.344000e-15</td>
    </tr>
    <tr>
      <th>25</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S06:S06_R01</td>
      <td>4.436000e-15</td>
      <td>4.689000e-15</td>
      <td>4.956000e-15</td>
      <td>5.238000e-15</td>
      <td>5.537000e-15</td>
      <td>5.853000e-15</td>
      <td>6.186000e-15</td>
      <td>6.539000e-15</td>
      <td>...</td>
      <td>1.379000e-14</td>
      <td>1.305000e-14</td>
      <td>1.235000e-14</td>
      <td>1.168000e-14</td>
      <td>1.105000e-14</td>
      <td>1.045000e-14</td>
      <td>9.890000e-15</td>
      <td>9.356000e-15</td>
      <td>8.852000e-15</td>
      <td>8.374000e-15</td>
    </tr>
    <tr>
      <th>26</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S06:S06_R02</td>
      <td>2.629000e-15</td>
      <td>2.778000e-15</td>
      <td>2.937000e-15</td>
      <td>3.104000e-15</td>
      <td>3.281000e-15</td>
      <td>3.468000e-15</td>
      <td>3.666000e-15</td>
      <td>3.875000e-15</td>
      <td>...</td>
      <td>8.174000e-15</td>
      <td>7.733000e-15</td>
      <td>7.316000e-15</td>
      <td>6.921000e-15</td>
      <td>6.548000e-15</td>
      <td>6.195000e-15</td>
      <td>5.861000e-15</td>
      <td>5.545000e-15</td>
      <td>5.246000e-15</td>
      <td>4.963000e-15</td>
    </tr>
    <tr>
      <th>27</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S06:S06_R03</td>
      <td>4.414000e-15</td>
      <td>4.665000e-15</td>
      <td>4.931000e-15</td>
      <td>5.212000e-15</td>
      <td>5.509000e-15</td>
      <td>5.824000e-15</td>
      <td>6.156000e-15</td>
      <td>6.507000e-15</td>
      <td>...</td>
      <td>1.372000e-14</td>
      <td>1.298000e-14</td>
      <td>1.228000e-14</td>
      <td>1.162000e-14</td>
      <td>1.099000e-14</td>
      <td>1.040000e-14</td>
      <td>9.840000e-15</td>
      <td>9.310000e-15</td>
      <td>8.807000e-15</td>
      <td>8.332000e-15</td>
    </tr>
    <tr>
      <th>28</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S06:S06_R04</td>
      <td>4.286000e-15</td>
      <td>4.530000e-15</td>
      <td>4.788000e-15</td>
      <td>5.061000e-15</td>
      <td>5.350000e-15</td>
      <td>5.655000e-15</td>
      <td>5.977000e-15</td>
      <td>6.318000e-15</td>
      <td>...</td>
      <td>1.333000e-14</td>
      <td>1.261000e-14</td>
      <td>1.193000e-14</td>
      <td>1.128000e-14</td>
      <td>1.068000e-14</td>
      <td>1.010000e-14</td>
      <td>9.555000e-15</td>
      <td>9.040000e-15</td>
      <td>8.552000e-15</td>
      <td>8.091000e-15</td>
    </tr>
    <tr>
      <th>29</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>S06:S06_R05</td>
      <td>3.043000e-16</td>
      <td>3.216000e-16</td>
      <td>3.400000e-16</td>
      <td>3.594000e-16</td>
      <td>3.799000e-16</td>
      <td>4.015000e-16</td>
      <td>4.244000e-16</td>
      <td>4.486000e-16</td>
      <td>...</td>
      <td>9.463000e-16</td>
      <td>8.952000e-16</td>
      <td>8.469000e-16</td>
      <td>8.012000e-16</td>
      <td>7.580000e-16</td>
      <td>7.171000e-16</td>
      <td>6.785000e-16</td>
      <td>6.419000e-16</td>
      <td>6.072000e-16</td>
      <td>5.745000e-16</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>933870</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S05:S05_R01</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933871</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S05:S05_R02</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933872</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S05:S05_R03</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933873</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S05:S05_R04</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933874</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S05:S05_R05</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933875</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S06:S06_R01</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933876</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S06:S06_R02</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933877</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S06:S06_R03</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933878</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S06:S06_R04</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933879</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S06:S06_R05</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933880</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S07:S07_R01</td>
      <td>2.196000e-14</td>
      <td>2.321000e-14</td>
      <td>2.453000e-14</td>
      <td>2.593000e-14</td>
      <td>2.741000e-14</td>
      <td>2.897000e-14</td>
      <td>3.062000e-14</td>
      <td>3.237000e-14</td>
      <td>...</td>
      <td>6.828000e-14</td>
      <td>6.460000e-14</td>
      <td>6.111000e-14</td>
      <td>5.782000e-14</td>
      <td>5.470000e-14</td>
      <td>5.175000e-14</td>
      <td>4.896000e-14</td>
      <td>4.632000e-14</td>
      <td>4.382000e-14</td>
      <td>4.145000e-14</td>
    </tr>
    <tr>
      <th>933881</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S07:S07_R02</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933882</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S07:S07_R03</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933883</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S07:S07_R04</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933884</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S07:S07_R05</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933885</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S08:S08_R01</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933886</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S08:S08_R02</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933887</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S08:S08_R03</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933888</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S08:S08_R04</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933889</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S08:S08_R05</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933890</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S09:S09_R01</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933891</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S09:S09_R02</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933892</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S09:S09_R03</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933893</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S09:S09_R04</td>
      <td>1.585000e-14</td>
      <td>1.675000e-14</td>
      <td>1.770000e-14</td>
      <td>1.871000e-14</td>
      <td>1.978000e-14</td>
      <td>2.091000e-14</td>
      <td>2.210000e-14</td>
      <td>2.336000e-14</td>
      <td>...</td>
      <td>4.928000e-14</td>
      <td>4.662000e-14</td>
      <td>4.410000e-14</td>
      <td>4.173000e-14</td>
      <td>3.947000e-14</td>
      <td>3.735000e-14</td>
      <td>3.533000e-14</td>
      <td>3.343000e-14</td>
      <td>3.162000e-14</td>
      <td>2.992000e-14</td>
    </tr>
    <tr>
      <th>933894</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S09:S09_R05</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933895</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S10:S10_R01</td>
      <td>1.485000e-14</td>
      <td>1.569000e-14</td>
      <td>1.659000e-14</td>
      <td>1.753000e-14</td>
      <td>1.853000e-14</td>
      <td>1.959000e-14</td>
      <td>2.071000e-14</td>
      <td>2.189000e-14</td>
      <td>...</td>
      <td>4.617000e-14</td>
      <td>4.368000e-14</td>
      <td>4.132000e-14</td>
      <td>3.909000e-14</td>
      <td>3.698000e-14</td>
      <td>3.499000e-14</td>
      <td>3.310000e-14</td>
      <td>3.132000e-14</td>
      <td>2.963000e-14</td>
      <td>2.803000e-14</td>
    </tr>
    <tr>
      <th>933896</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S10:S10_R02</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933897</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S10:S10_R03</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933898</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S10:S10_R04</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
    <tr>
      <th>933899</th>
      <td>decoy_V6CJA9_CAEEL</td>
      <td>S10:S10_R05</td>
      <td>2.340000e-14</td>
      <td>2.473000e-14</td>
      <td>2.614000e-14</td>
      <td>2.763000e-14</td>
      <td>2.921000e-14</td>
      <td>3.087000e-14</td>
      <td>3.263000e-14</td>
      <td>3.449000e-14</td>
      <td>...</td>
      <td>7.275000e-14</td>
      <td>6.883000e-14</td>
      <td>6.512000e-14</td>
      <td>6.161000e-14</td>
      <td>5.828000e-14</td>
      <td>5.514000e-14</td>
      <td>5.216000e-14</td>
      <td>4.935000e-14</td>
      <td>4.669000e-14</td>
      <td>4.417000e-14</td>
    </tr>
  </tbody>
</table>
<p>933900 rows × 1003 columns</p>
</div>



Trying to run the code /home/ptruong/git/triqler/triqler/distribution/python plot_posteriors.py. The following relative imports:

from ..triqler import __version__, __copyright__
from .. import parsers
from .. import hyperparameters
from .. import pgm
from .. import diff_exp


Gives this error


Traceback (most recent call last):

  File "plot_posteriors.py", line 18, in <module>
    
    from ..triqler import __version__, __copyright__
    
ValueError: attempted relative import beyond top-level package
    

How does this relative import work?

    
    
    
 

Plotting worked with:

python -m triqler.distribution.plot_posteriors --protein_id_list protein_list.csv  P_OUT



OUTPUT:



Triqler.distribution.plot_posteriors version 0.6.0
Copyright (c) 2018-2020 Matthew The. All rights reserved.
Written by Matthew The (matthew.the@scilifelab.se) in the
School of Engineering Sciences in Chemistry, Biotechnology and Health at the 
Royal Institute of Technology in Stockholm.
Issued command: plot_posteriors.py --protein_id_list protein_list.csv P_OUT
Protein list posterior plotting not yet supported for protein posteriors


The input F_OUT and G_OUT seem to give the similar response. I need to check if the heatmap plot needs to be run manually.

## 2020-12-08 

In the [triqler manual](https://www.biorxiv.org/content/10.1101/2020.09.24.311605v1.full.pdf). It is specified we should work with original input file (example case: iPRG2016 and we need the peptide quantification file iPRG2016.tsv.pqr.tsv).

In the example case. The following works:

python -m triqler iPRG2016.tsv 

To generate the .tsv.pqr.tsv file. Then we do the protein_id plot.

python -m triqler.distribution.plot_posteriors --protein_id HPRR3730445_poolB iPRG2016.tsv



OUTPUT log:


```python
(py36) ptruong@planck:~/git/triqler/example$ python -m triqler.distribution.plot_posteriors --protein_id HPRR3730445_poolB iPRG2016.tsv 
Triqler.distribution.plot_posteriors version 0.6.0
Copyright (c) 2018-2020 Matthew The. All rights reserved.
Written by Matthew The (matthew.the@scilifelab.se) in the
School of Engineering Sciences in Chemistry, Biotechnology and Health at the 
Royal Institute of Technology in Stockholm.
Issued command: plot_posteriors.py --protein_id HPRR3730445_poolB iPRG2016.tsv
Could not locate peptide quantification file iPRG2016.tsv.pqr.tsv. Run triqler to generate this file.
(py36) ptruong@planck:~/git/triqler/example$ python -m triqler iPRG2016.tsv 
Triqler version 0.6.0
Copyright (c) 2018-2020 Matthew The. All rights reserved.
Written by Matthew The (matthew.the@scilifelab.se) in the
School of Engineering Sciences in Chemistry, Biotechnology and Health at the 
Royal Institute of Technology in Stockholm.
Issued command: triqler.py iPRG2016.tsv
Parsing triqler input file
  Reading row 0
Calculating identification PEPs
  Identified 12113 PSMs at 1% FDR
Selecting best feature per run and spectrum
  featureGroupIdx: 0
Dividing intensities by 100000 for increased readability
Calculating peptide-level identification PEPs
  Identified 1988 peptides at 1% FDR
Writing peptide quant rows to file: iPRG2016.tsv.pqr.tsv
Calculating protein-level identification PEPs
  Identified 349 proteins at 1% FDR
Fitting hyperparameters
  params["muDetect"], params["sigmaDetect"] = 1.056334, 0.372395
  params["muXIC"], params["sigmaXIC"] = 3.276315, 0.953023
  params["muProtein"], params["sigmaProtein"] = 0.066437, 0.239524
  params["muFeatureDiff"], params["sigmaFeatureDiff"] = -0.013907, 0.149265
  params["shapeInGroupStdevs"], params["scaleInGroupStdevs"] = 1.027176, 0.089433
Calculating protein posteriors
  50 / 422 11.85%
  100 / 422 23.70%
  150 / 422 35.55%
  200 / 422 47.39%
  250 / 422 59.24%
  300 / 422 71.09%
  350 / 422 82.94%
  400 / 422 94.79%
Comparing 1:A+B to 2:B
  output file: proteins.1vs2.tsv
  Found 204 target proteins as differentially abundant at 5% FDR
Comparing 1:A+B to 3:A
  output file: proteins.1vs3.tsv
  Found 216 target proteins as differentially abundant at 5% FDR
Comparing 2:B to 3:A
  output file: proteins.2vs3.tsv
  Found 352 target proteins as differentially abundant at 5% FDR
Triqler execution took 28.871479630994145 seconds wall clock time

```


```python

```


```python
(py36) ptruong@planck:~/git/triqler/example$ python -m triqler.distribution.plot_posteriors --protein_id HPRR3730445_poolB iPRG2016.tsv 
Triqler.distribution.plot_posteriors version 0.6.0
Copyright (c) 2018-2020 Matthew The. All rights reserved.
Written by Matthew The (matthew.the@scilifelab.se) in the
School of Engineering Sciences in Chemistry, Biotechnology and Health at the 
Royal Institute of Technology in Stockholm.
Issued command: plot_posteriors.py --protein_id HPRR3730445_poolB iPRG2016.tsv
Could not locate peptide quantification file iPRG2016.tsv.pqr.tsv. Run triqler to generate this file.
(py36) ptruong@planck:~/git/triqler/example$ python -m triqler iPRG2016.tsv 
Triqler version 0.6.0
Copyright (c) 2018-2020 Matthew The. All rights reserved.
Written by Matthew The (matthew.the@scilifelab.se) in the
School of Engineering Sciences in Chemistry, Biotechnology and Health at the 
Royal Institute of Technology in Stockholm.
Issued command: triqler.py iPRG2016.tsv
Parsing triqler input file
  Reading row 0
Calculating identification PEPs
  Identified 12113 PSMs at 1% FDR
Selecting best feature per run and spectrum
  featureGroupIdx: 0
Dividing intensities by 100000 for increased readability
Calculating peptide-level identification PEPs
  Identified 1988 peptides at 1% FDR
Writing peptide quant rows to file: iPRG2016.tsv.pqr.tsv
Calculating protein-level identification PEPs
  Identified 349 proteins at 1% FDR
Fitting hyperparameters
  params["muDetect"], params["sigmaDetect"] = 1.056334, 0.372395
  params["muXIC"], params["sigmaXIC"] = 3.276315, 0.953023
  params["muProtein"], params["sigmaProtein"] = 0.066437, 0.239524
  params["muFeatureDiff"], params["sigmaFeatureDiff"] = -0.013907, 0.149265
  params["shapeInGroupStdevs"], params["scaleInGroupStdevs"] = 1.027176, 0.089433
Calculating protein posteriors
  50 / 422 11.85%
  100 / 422 23.70%
  150 / 422 35.55%
  200 / 422 47.39%
  250 / 422 59.24%
  300 / 422 71.09%
  350 / 422 82.94%
  400 / 422 94.79%
Comparing 1:A+B to 2:B
  output file: proteins.1vs2.tsv
  Found 204 target proteins as differentially abundant at 5% FDR
Comparing 1:A+B to 3:A
  output file: proteins.1vs3.tsv
  Found 216 target proteins as differentially abundant at 5% FDR
Comparing 2:B to 3:A
  output file: proteins.2vs3.tsv
  Found 352 target proteins as differentially abundant at 5% FDR
Triqler execution took 28.871479630994145 seconds wall clock time
(py36) ptruong@planck:~/git/triqler/example$ ls
iPRG2016_ref.proteins.1vs2.tsv	iPRG2016_ref.tsv.pqr.tsv  proteins.1vs2.tsv
iPRG2016_ref.proteins.1vs3.tsv	iPRG2016.tsv		  proteins.1vs3.tsv
iPRG2016_ref.proteins.2vs3.tsv	iPRG2016.tsv.pqr.tsv	  proteins.2vs3.tsv
(py36) ptruong@planck:~/git/triqler/example$ python -m triqler.distribution.plot_posteriors --protein_id HPRR3730445_poolB iPRG2016.tsv 
Triqler.distribution.plot_posteriors version 0.6.0
Copyright (c) 2018-2020 Matthew The. All rights reserved.
Written by Matthew The (matthew.the@scilifelab.se) in the
School of Engineering Sciences in Chemistry, Biotechnology and Health at the 
Royal Institute of Technology in Stockholm.
Issued command: plot_posteriors.py --protein_id HPRR3730445_poolB iPRG2016.tsv
Fitting hyperparameters
  params["muDetect"], params["sigmaDetect"] = 1.056315, 0.372438
  params["muXIC"], params["sigmaXIC"] = 3.276315, 0.953023
  params["muProtein"], params["sigmaProtein"] = 0.066425, 0.239521
  params["muFeatureDiff"], params["sigmaFeatureDiff"] = -0.013907, 0.149265
  params["shapeInGroupStdevs"], params["scaleInGroupStdevs"] = 1.027176, 0.089432

Protein ID: HPRR3730445_poolB

Peptide absolute abundances
760.43	509.03	1028.25	842.80	1610.55	1289.44	nan	nan	nan	combinedPEP=3.4e-06	peptide=R.WTAQGHANHGFVVEVAHLEEK.Q
99.93	166.59	3184.98	1868.59	6260.46	5909.35	nan	nan	59.71	combinedPEP=2.2e-05	peptide=R.LVNQNASRWESFDVTPAVMR.W
10064.52	12531.44	nan	27429.83	26226.20	23061.53nan	242.17	19.53	combinedPEP=0.0023	peptide=R.WESFDVTPAVMR.W

Peptide relative abundances
0.81	0.54	1.09	0.90	1.71	1.37	nan	nan	nan	combinedPEP=3.4e-06	peptide=R.WTAQGHANHGFVVEVAHLEEK.Q
0.12	0.21	3.96	2.32	7.78	7.34	nan	nan	0.07	combinedPEP=2.2e-05	peptide=R.LVNQNASRWESFDVTPAVMR.W
2.70	3.37	nan	7.37	7.05	6.20	nan	0.07	0.01	combinedPEP=0.0023	peptide=R.WESFDVTPAVMR.W

Protein abundance (expected value) and p-value
3.27	2.97	5.48	7.66	13.64	11.55	0.01	0.07	0.02
p-value: 3.2822538226303985e-05

Posterior probability |log2 fold change| < 1.00
  Group A+B vs Group B: 0.130072
  Group A+B vs Group A: 0.000000
  Group B vs Group A: 0.000000

Normal distribution fits for posterior distributions of treatment group relative abundances:
  Group A+B: mu, sigma = 0.472918, 0.114328
  Group B: mu, sigma = 0.918317, 0.071100
  Group A: mu, sigma = -1.782820, 0.269253
(py36) ptruong@planck:~/git/triqler/example$ 

```

Test attempt on PSSS3

and the following set of proteins.

A0A023T4K3_CAEEL

A0A061ACH4_CAEEL

A0A061ACK4_CAEEL

A0A061ACL3_CAEEL

A0A061ACR1_CAEEL

A0A061ACS5_CAEEL

A0A061ACU2_CAEEL

A0A061ACU6_CAEEL

A0A061ACY0_CAEEL

A0A061AD21_CAEEL

A0A061AD39_CAEEL

A0A061AD47_CAEEL

A0A061AE05_CAEEL

A0A061AJ42_CAEEL

A0A061AJK8_CAEEL

A0A061AKY5_CAEEL

A0A061AL58_CAEEL

A0A078BPG0_CAEEL

A0A078BPH9_CAEEL

A0A078BPJ4_CAEEL

There proteins are saved in protein_list.csv

 Command run:
 
 python -m triqler.distribution.plot_posteriors --protein_id_list protein_list.csv PSSS3_triqlerFormatted_nonShared.csv
 
 output plots are in results/2020-12-08

### Working with melted data



```python
import os
```


```python
os.chdir("/home/ptruong/git/bayesMS/bin")
```


```python
import os 

import pandas as pd
import numpy as np 

from read_triqler_output import read_triqler_protein_output_to_df
from triqler_output_df_melter import melt_spectronaut_triqler_formatted, melt_triqler_output
from count_melted import count_melted_for_all_samples

os.chdir("/home/ptruong/git/bayesMS/data/old_data_pickled")
os.listdir()
```




    ['spectronaut.pkl',
     'spectronautParams.txt',
     'triqlerParams.txt',
     'triqler.pkl']




```python
 pd.set_option('display.max_rows', 10)
```


```python
spec = pd.read_pickle(r'spectronaut.pkl')
triq = pd.read_pickle(r'triqler.pkl')

```


```python
os.chdir("/home/ptruong/git/bayesMS/data/triqlerResults_largeScale_minSamp20_FC0_8_adjInt")
```


```python
os.listdir()
```




    ['proteins.6vs8.tsv',
     'proteins.5vs9.tsv',
     'proteins.3vs5.tsv',
     'proteins.4vs10.tsv',
     'proteins.3vs10.tsv',
     'proteins.1vs4.tsv',
     'proteins.5vs6.tsv',
     'proteins.2vs8.tsv',
     'proteins.4vs6.tsv',
     'proteins.2vs6.tsv',
     'proteins.9vs10.tsv',
     'proteins.2vs3.tsv',
     'proteins.7vs8.tsv',
     'proteins.1vs2.tsv',
     'proteins.3vs8.tsv',
     'proteins.3vs6.tsv',
     'proteins.1vs8.tsv',
     'proteins.6vs10.tsv',
     'proteins.5vs10.tsv',
     'proteins.3vs4.tsv',
     'proteins.7vs9.tsv',
     'proteins.1vs7.tsv',
     'proteins.2vs10.tsv',
     'proteins.3vs7.tsv',
     'proteins.8vs9.tsv',
     'proteins.4vs7.tsv',
     'proteins.7vs10.tsv',
     'proteins.2vs7.tsv',
     'proteins.6vs9.tsv',
     'proteins.1vs10.tsv',
     'proteins.4vs9.tsv',
     'proteins.5vs8.tsv',
     'proteins.2vs5.tsv',
     'proteins.1vs9.tsv',
     'proteins.1vs3.tsv',
     'proteins.5vs7.tsv',
     'proteins.1vs6.tsv',
     'proteins.2vs9.tsv',
     'proteins.3vs9.tsv',
     'proteins.6vs7.tsv',
     'proteins.8vs10.tsv',
     'proteins.4vs5.tsv',
     'proteins.4vs8.tsv',
     'proteins.1vs5.tsv',
     'proteins.2vs4.tsv']




```python
triq = read_triqler_protein_output_to_df('proteins.3vs8.tsv')
triq2 = read_triqler_protein_output_to_df('proteins.2vs6.tsv')
```


```python
spec = spec.rename(columns={'S03:S04_R05': 'S03:S03_R04'})
```


```python
triq = melt_triqler_output(triq)
spec = melt_spectronaut_triqler_formatted(spec)
```


```python
triq2=melt_triqler_output(triq2)
```


```python
triq
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>q_value</th>
      <th>posterior_error_prob</th>
      <th>protein</th>
      <th>num_peptides</th>
      <th>protein_id_posterior_error_prob</th>
      <th>log2_fold_change</th>
      <th>diff_exp_prob_0.8</th>
      <th>sample</th>
      <th>run</th>
      <th>value</th>
      <th>peptide</th>
      <th>species</th>
      <th>specie</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R01</td>
      <td>41.3300</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R02</td>
      <td>41.0700</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R03</td>
      <td>38.9800</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R04</td>
      <td>40.1300</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R05</td>
      <td>40.5900</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>543045</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R01</td>
      <td>1.0150</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
    <tr>
      <th>543046</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R02</td>
      <td>1.0360</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
    <tr>
      <th>543047</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R03</td>
      <td>1.0420</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
    <tr>
      <th>543048</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R04</td>
      <td>0.9652</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
    <tr>
      <th>543049</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R05</td>
      <td>0.9473</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
  </tbody>
</table>
<p>543050 rows × 13 columns</p>
</div>




```python
triq2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>q_value</th>
      <th>posterior_error_prob</th>
      <th>protein</th>
      <th>num_peptides</th>
      <th>protein_id_posterior_error_prob</th>
      <th>log2_fold_change</th>
      <th>diff_exp_prob_0.8</th>
      <th>sample</th>
      <th>run</th>
      <th>value</th>
      <th>peptide</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>4.139000</td>
      <td>1.967000e-13</td>
      <td>S01</td>
      <td>R01</td>
      <td>41.3300</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>4.139000</td>
      <td>1.967000e-13</td>
      <td>S01</td>
      <td>R02</td>
      <td>41.0700</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>4.139000</td>
      <td>1.967000e-13</td>
      <td>S01</td>
      <td>R03</td>
      <td>38.9800</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>4.139000</td>
      <td>1.967000e-13</td>
      <td>S01</td>
      <td>R04</td>
      <td>40.1300</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>4.139000</td>
      <td>1.967000e-13</td>
      <td>S01</td>
      <td>R05</td>
      <td>40.5900</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>543045</th>
      <td>6.674000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.007193</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R01</td>
      <td>1.0150</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
    <tr>
      <th>543046</th>
      <td>6.674000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.007193</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R02</td>
      <td>1.0360</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
    <tr>
      <th>543047</th>
      <td>6.674000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.007193</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R03</td>
      <td>1.0420</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
    <tr>
      <th>543048</th>
      <td>6.674000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.007193</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R04</td>
      <td>0.9652</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
    <tr>
      <th>543049</th>
      <td>6.674000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.007193</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R05</td>
      <td>0.9473</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
  </tbody>
</table>
<p>543050 rows × 11 columns</p>
</div>




```python
spec
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>specie</th>
      <th>protein</th>
      <th>sample</th>
      <th>run</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R01</td>
      <td>203877.890625</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R02</td>
      <td>190713.625000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R03</td>
      <td>195925.703125</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R04</td>
      <td>150170.421875</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A0A023T4K3_CAEEL</td>
      <td>CAEEL</td>
      <td>A0A023T4K3</td>
      <td>S01</td>
      <td>R05</td>
      <td>163190.718750</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>750695</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R01</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750696</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R02</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750697</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R03</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750698</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R04</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>750699</th>
      <td>X5M5N0_CAEEL</td>
      <td>CAEEL</td>
      <td>X5M5N0</td>
      <td>S10</td>
      <td>R05</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>750700 rows × 6 columns</p>
</div>



### Lets work with triq...


```python
samples = ["S0"+str(i) for i in range(1,10)] + ["S10"]
```


```python
samples
```




    ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']




```python
triq["specie"] = triq.protein.apply(lambda x: x.split('_')[-1])
```


```python
triq[triq["sample"] == "S01"]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>q_value</th>
      <th>posterior_error_prob</th>
      <th>protein</th>
      <th>num_peptides</th>
      <th>protein_id_posterior_error_prob</th>
      <th>log2_fold_change</th>
      <th>diff_exp_prob_0.8</th>
      <th>sample</th>
      <th>run</th>
      <th>value</th>
      <th>peptide</th>
      <th>species</th>
      <th>specie</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R01</td>
      <td>41.3300</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R02</td>
      <td>41.0700</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R03</td>
      <td>38.9800</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R04</td>
      <td>40.1300</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R05</td>
      <td>40.5900</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
      <td>CAEEL</td>
      <td>CAEEL</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>543000</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S01</td>
      <td>R01</td>
      <td>1.0040</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
    <tr>
      <th>543001</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S01</td>
      <td>R02</td>
      <td>1.0300</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
    <tr>
      <th>543002</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S01</td>
      <td>R03</td>
      <td>1.0300</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
    <tr>
      <th>543003</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S01</td>
      <td>R04</td>
      <td>1.0330</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
    <tr>
      <th>543004</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S01</td>
      <td>R05</td>
      <td>0.9655</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
      <td>ARATH</td>
      <td>ARATH</td>
    </tr>
  </tbody>
</table>
<p>54305 rows × 13 columns</p>
</div>




```python
# Identified protein through all samples
print("%s : %i" % ("triqler number of protein ids", int(sum(triq.protein_id_posterior_error_prob < 0.01))))
print("%s : %i" % ("spectronaut number of protein ids", int(len(spec.dropna()))))

# Identified protein for species across all samples
triq_count = len(triq[triq.specie == "ARATH"])
spec_count = len(spec[spec.specie == "ARATH"].dropna())

print("%s : %i" % ("triqler ARATH number of protein ids", triq_count))
print("%s : %i" % ("spectronaut ARATH number of protein ids", spec_count))

triq_count = len(triq[triq.specie == "CAEEL"])
spec_count = len(spec[spec.specie == "CAEEL"].dropna())

print("%s : %i" % ("triqler CAEEL number of protein ids", triq_count))
print("%s : %i" % ("spectronaut CAEEL number of protein ids", spec_count))

triq_count = len(triq[triq.specie == "HUMAN"])
spec_count = len(spec[spec.specie == "HUMAN"].dropna())

print("%s : %i" % ("triqler HUMAN number of protein ids", triq_count))
print("%s : %i" % ("spectronaut HUMAN number of protein ids", spec_count))
```

    triqler number of protein ids : 543050
    spectronaut number of protein ids : 543601
    triqler ARATH number of protein ids : 189800
    spectronaut ARATH number of protein ids : 218754
    triqler CAEEL number of protein ids : 73600
    spectronaut CAEEL number of protein ids : 58732
    triqler HUMAN number of protein ids : 279650
    spectronaut HUMAN number of protein ids : 266115



```python
samples = ["S0"+str(i) for i in range(1,10)] + ["S10"]

```


```python
samples
```




    ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']




```python

count_melted_for_all_samples(triq, specie = None)

```




    [54305, 54305, 54305, 54305, 54305, 54305, 54305, 54305, 54305, 54305]




```python
count_melted_for_all_samples(triq, specie = "HUMAN")

```




    [27965, 27965, 27965, 27965, 27965, 27965, 27965, 27965, 27965, 27965]




```python
count_melted_for_all_samples(triq, specie = "CAEEL")

```




    [7360, 7360, 7360, 7360, 7360, 7360, 7360, 7360, 7360, 7360]




```python
count_melted_for_all_samples(triq, specie = "ARATH")

```




    [18980, 18980, 18980, 18980, 18980, 18980, 18980, 18980, 18980, 18980]




```python
count_melted_for_all_samples(spec, specie = None)

```




    [43530, 66501, 61173, 57595, 54205, 52857, 52299, 51731, 52031, 51679]




```python
count_melted_for_all_samples(spec, specie = "HUMAN")

```




    [150, 26634, 29423, 29849, 29887, 29977, 30086, 29976, 30193, 29940]




```python
count_melted_for_all_samples(spec, specie = "CAEEL")

```




    [20808, 17464, 9863, 5896, 2566, 1155, 490, 229, 137, 124]




```python
count_melted_for_all_samples(spec, specie = "ARATH")

```




    [22572, 22403, 21887, 21850, 21752, 21725, 21723, 21526, 21701, 21615]



In the above counting we are counting the number identified proteins, without imputation for spec for each sample (i.e. with all 5 runs for each sample, triq is tresholded at 1%PEP and spec is tresholded at 1%FRD).

## 2020-12-09

### Fold change matrix

We can compute a couple of fold change matrices for exploration.

1. triqler posterior distribution differential expression for each proteinXvsY file.
2. triqler fold change differential expression.
3. spectronaut fold change differential expression.

How about the imputations? 
- I want to skip imputation for as long as possible.


### Triqler input should have 1 intensities set to NaN

Coded up this part in bin/script_convert_PSSS3_1toNaN.py

### Normalization

Normalization withing sample and run is performed. The logic is that all proteins from each sample and run should sum to 100%, but I do not know if this is correct after FDR tresholding. 


```python
os.chdir("/home/ptruong/git/bayesMS/bin")
```


```python
from normalize_melted import normalize_within_sample
```


```python
from normalize_melted import get_ratios_from_normalized_melted_df #Why no work??

```


    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-103-c583aa259998> in <module>
    ----> 1 from normalize_melted import get_ratios_from_normalized_melted_df #Why no work??
    

    ImportError: cannot import name 'get_ratios_from_normalized_melted_df'



```python
def get_ratios_from_normalized_melted_df(df, specie):
    """
    input - normalized df (triq, spec)
    output - ratios dataframe
    """
    samples = ["S0"+str(i) for i in range(1,10)] + ["S10"] 
    runs = ["R0" + str(i) for i in range(1,6)]
    
    ratios = []
    for sample in samples:
        ratios_for_sample = []
        for run in runs:
            df_sample = df[df["sample"] == sample]
            df_sample_run = df_sample[df_sample["run"] == run]
            df_sample_run_spec = df_sample_run[df_sample_run["specie"] == specie]
            ratios_for_sample.append(df_sample_run_spec.value.sum())
        ratios.append(ratios_for_sample)
    ratios_df = pd.DataFrame(ratios, index = samples, columns = runs)
    return ratios_df

```


```python
df_spec = normalize_within_sample(spec)
df_triq  = normalize_within_sample(triq)

```

    /home/ptruong/.local/lib/python3.6/site-packages/pandas/core/generic.py:5096: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self[name] = value


### Mixture ratios

Below is a presentation of the mixture ratios of the different species. 

### True ratios as a reminder

| Species     | S01 | S02  | S03   | S04    | S05   | S06    | S07   | S08   | S09   | S10 |
|-------------|-----|------|-------|--------|-------|--------|-------|-------|-------|-----|
| A. thaliana | 0.5 | 0.5  | 0.5   | 0.5    | 0.5   | 0.5    | 0.5   | 0.5   | 0.5   | 0.5 |
| C. elegans  | 0.5 | 0.25 | 0.125 | 0.0625 | 0.031 | 0.0155 | 0.008 | 0.004 | 0.002 | 0   |
| H. sapiens  | 0   | 0.25 | 0.375 | 0.4375 | 0.469 | 0.4845 | 0.492 | 0.496 | 0.498 | 0.5 |

<center><strong>Table 1</strong> . Protein ratios of the ten samples {S01, S02, ..., S10}.</center>

### Triqler normalized within sample ratios


```python
get_ratios_from_normalized_melted_df(df_triq, "HUMAN")

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R01</th>
      <th>R02</th>
      <th>R03</th>
      <th>R04</th>
      <th>R05</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.128203</td>
      <td>0.126626</td>
      <td>0.120877</td>
      <td>0.127743</td>
      <td>0.116869</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>0.289482</td>
      <td>0.291946</td>
      <td>0.290659</td>
      <td>0.287219</td>
      <td>0.290460</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>0.491754</td>
      <td>0.487170</td>
      <td>0.486278</td>
      <td>0.483526</td>
      <td>0.484137</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>0.560859</td>
      <td>0.560926</td>
      <td>0.560348</td>
      <td>0.558908</td>
      <td>0.562115</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>0.601416</td>
      <td>0.598230</td>
      <td>0.592589</td>
      <td>0.593048</td>
      <td>0.590547</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>0.612168</td>
      <td>0.626370</td>
      <td>0.606038</td>
      <td>0.604525</td>
      <td>0.601781</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>0.623440</td>
      <td>0.639131</td>
      <td>0.609387</td>
      <td>0.615723</td>
      <td>0.612576</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>0.615171</td>
      <td>0.708059</td>
      <td>0.620531</td>
      <td>0.620357</td>
      <td>0.613928</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>0.625644</td>
      <td>0.620596</td>
      <td>0.613507</td>
      <td>0.624937</td>
      <td>0.613674</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>0.610641</td>
      <td>0.606414</td>
      <td>0.606816</td>
      <td>0.605386</td>
      <td>0.603594</td>
    </tr>
  </tbody>
</table>
</div>




```python
get_ratios_from_normalized_melted_df(df_triq, "ARATH")

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R01</th>
      <th>R02</th>
      <th>R03</th>
      <th>R04</th>
      <th>R05</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.202221</td>
      <td>0.207353</td>
      <td>0.206096</td>
      <td>0.203861</td>
      <td>0.210821</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>0.263496</td>
      <td>0.264762</td>
      <td>0.266483</td>
      <td>0.266022</td>
      <td>0.270651</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>0.273122</td>
      <td>0.276097</td>
      <td>0.279398</td>
      <td>0.281625</td>
      <td>0.281548</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>0.282105</td>
      <td>0.285016</td>
      <td>0.288407</td>
      <td>0.286770</td>
      <td>0.290583</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>0.290369</td>
      <td>0.291970</td>
      <td>0.297159</td>
      <td>0.295287</td>
      <td>0.298664</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>0.284978</td>
      <td>0.278644</td>
      <td>0.289323</td>
      <td>0.288021</td>
      <td>0.292126</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>0.285500</td>
      <td>0.269952</td>
      <td>0.284272</td>
      <td>0.283905</td>
      <td>0.285864</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>0.277279</td>
      <td>0.225521</td>
      <td>0.279139</td>
      <td>0.277611</td>
      <td>0.278581</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>0.276741</td>
      <td>0.279461</td>
      <td>0.281202</td>
      <td>0.284556</td>
      <td>0.282891</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>0.286438</td>
      <td>0.283075</td>
      <td>0.288762</td>
      <td>0.289589</td>
      <td>0.289557</td>
    </tr>
  </tbody>
</table>
</div>




```python
get_ratios_from_normalized_melted_df(df_triq, "CAEEL")

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R01</th>
      <th>R02</th>
      <th>R03</th>
      <th>R04</th>
      <th>R05</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.669577</td>
      <td>0.666021</td>
      <td>0.673027</td>
      <td>0.668396</td>
      <td>0.672311</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>0.447023</td>
      <td>0.443292</td>
      <td>0.442858</td>
      <td>0.446759</td>
      <td>0.438889</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>0.235124</td>
      <td>0.236733</td>
      <td>0.234325</td>
      <td>0.234849</td>
      <td>0.234315</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>0.157036</td>
      <td>0.154057</td>
      <td>0.151245</td>
      <td>0.154322</td>
      <td>0.147303</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>0.108215</td>
      <td>0.109800</td>
      <td>0.110252</td>
      <td>0.111665</td>
      <td>0.110790</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>0.102855</td>
      <td>0.094986</td>
      <td>0.104640</td>
      <td>0.107454</td>
      <td>0.106093</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>0.091061</td>
      <td>0.090917</td>
      <td>0.106341</td>
      <td>0.100372</td>
      <td>0.101560</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>0.107549</td>
      <td>0.066420</td>
      <td>0.100330</td>
      <td>0.102032</td>
      <td>0.107491</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>0.097615</td>
      <td>0.099942</td>
      <td>0.105291</td>
      <td>0.090508</td>
      <td>0.103435</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>0.102920</td>
      <td>0.110511</td>
      <td>0.104422</td>
      <td>0.105024</td>
      <td>0.106849</td>
    </tr>
  </tbody>
</table>
</div>



### Spectronaut normalized within sample ratios


```python
get_ratios_from_normalized_melted_df(df_spec, "HUMAN")

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R01</th>
      <th>R02</th>
      <th>R03</th>
      <th>R04</th>
      <th>R05</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.000142</td>
      <td>0.006533</td>
      <td>0.000000</td>
      <td>0.000340</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>0.219433</td>
      <td>0.230812</td>
      <td>0.215881</td>
      <td>0.270386</td>
      <td>0.268880</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>0.353454</td>
      <td>0.346912</td>
      <td>0.338908</td>
      <td>0.342514</td>
      <td>0.342131</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>0.378023</td>
      <td>0.380670</td>
      <td>0.387151</td>
      <td>0.385364</td>
      <td>0.387890</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>0.399998</td>
      <td>0.406819</td>
      <td>0.393940</td>
      <td>0.398728</td>
      <td>0.396520</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>0.426578</td>
      <td>0.427706</td>
      <td>0.410134</td>
      <td>0.415170</td>
      <td>0.414603</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>0.440774</td>
      <td>0.442464</td>
      <td>0.420743</td>
      <td>0.419045</td>
      <td>0.454594</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>0.423673</td>
      <td>0.532117</td>
      <td>0.432001</td>
      <td>0.439144</td>
      <td>0.429417</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>0.443085</td>
      <td>0.430571</td>
      <td>0.427718</td>
      <td>0.431624</td>
      <td>0.425632</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>0.412168</td>
      <td>0.416974</td>
      <td>0.411104</td>
      <td>0.419243</td>
      <td>0.414248</td>
    </tr>
  </tbody>
</table>
</div>




```python
get_ratios_from_normalized_melted_df(df_spec, "ARATH")

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R01</th>
      <th>R02</th>
      <th>R03</th>
      <th>R04</th>
      <th>R05</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.718387</td>
      <td>0.709902</td>
      <td>0.717234</td>
      <td>0.719183</td>
      <td>0.715033</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>0.650569</td>
      <td>0.635745</td>
      <td>0.650215</td>
      <td>0.609311</td>
      <td>0.605776</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>0.596266</td>
      <td>0.592043</td>
      <td>0.597642</td>
      <td>0.595323</td>
      <td>0.602168</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>0.591857</td>
      <td>0.587589</td>
      <td>0.584385</td>
      <td>0.578559</td>
      <td>0.581851</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>0.588080</td>
      <td>0.580873</td>
      <td>0.591711</td>
      <td>0.586733</td>
      <td>0.585161</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>0.565183</td>
      <td>0.564956</td>
      <td>0.583932</td>
      <td>0.576295</td>
      <td>0.577756</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>0.555158</td>
      <td>0.552160</td>
      <td>0.578245</td>
      <td>0.573948</td>
      <td>0.542448</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>0.575006</td>
      <td>0.466419</td>
      <td>0.565983</td>
      <td>0.558071</td>
      <td>0.568368</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>0.553483</td>
      <td>0.568904</td>
      <td>0.569775</td>
      <td>0.568369</td>
      <td>0.573979</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>0.587524</td>
      <td>0.579042</td>
      <td>0.587372</td>
      <td>0.580757</td>
      <td>0.583747</td>
    </tr>
  </tbody>
</table>
</div>




```python
get_ratios_from_normalized_melted_df(df_spec, "CAEEL")
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R01</th>
      <th>R02</th>
      <th>R03</th>
      <th>R04</th>
      <th>R05</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.281471</td>
      <td>0.283565</td>
      <td>0.282766</td>
      <td>0.280477</td>
      <td>0.284967</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>0.129998</td>
      <td>0.133443</td>
      <td>0.133904</td>
      <td>0.120304</td>
      <td>0.125345</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>0.050280</td>
      <td>0.061045</td>
      <td>0.063450</td>
      <td>0.062163</td>
      <td>0.055701</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>0.030119</td>
      <td>0.031741</td>
      <td>0.028464</td>
      <td>0.036078</td>
      <td>0.030258</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>0.011922</td>
      <td>0.012308</td>
      <td>0.014349</td>
      <td>0.014539</td>
      <td>0.018319</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>0.008239</td>
      <td>0.007338</td>
      <td>0.005934</td>
      <td>0.008535</td>
      <td>0.007641</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>0.004068</td>
      <td>0.005375</td>
      <td>0.001012</td>
      <td>0.007007</td>
      <td>0.002958</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>0.001320</td>
      <td>0.001464</td>
      <td>0.002016</td>
      <td>0.002785</td>
      <td>0.002215</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>0.003432</td>
      <td>0.000525</td>
      <td>0.002507</td>
      <td>0.000007</td>
      <td>0.000389</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>0.000308</td>
      <td>0.003984</td>
      <td>0.001524</td>
      <td>0.000000</td>
      <td>0.002005</td>
    </tr>
  </tbody>
</table>
</div>




```python
from constants import get_sample_ratios, get_log2FC_ratio_matrix, get_log2FC_ratio_matrices


```


```python

ARATH_FC_matrix, CAEEL_FC_matrix, HUMAN_FC_matrix = get_log2FC_ratio_matrices()
```


```python
ARATH_FC_matrix
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>S01</th>
      <th>S02</th>
      <th>S03</th>
      <th>S04</th>
      <th>S05</th>
      <th>S06</th>
      <th>S07</th>
      <th>S08</th>
      <th>S09</th>
      <th>S10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
CAEEL_FC_matrix
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>S01</th>
      <th>S02</th>
      <th>S03</th>
      <th>S04</th>
      <th>S05</th>
      <th>S06</th>
      <th>S07</th>
      <th>S08</th>
      <th>S09</th>
      <th>S10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>3.000000</td>
      <td>4.011588</td>
      <td>5.011588</td>
      <td>5.965784</td>
      <td>6.965784</td>
      <td>7.965784</td>
      <td>18.931569</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>-1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>3.011588</td>
      <td>4.011588</td>
      <td>4.965784</td>
      <td>5.965784</td>
      <td>6.965784</td>
      <td>17.931569</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>-2.000000</td>
      <td>-1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>2.011588</td>
      <td>3.011588</td>
      <td>3.965784</td>
      <td>4.965784</td>
      <td>5.965784</td>
      <td>16.931569</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>-3.000000</td>
      <td>-2.000000</td>
      <td>-1.000000</td>
      <td>0.000000</td>
      <td>1.011588</td>
      <td>2.011588</td>
      <td>2.965784</td>
      <td>3.965784</td>
      <td>4.965784</td>
      <td>15.931569</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>-4.011588</td>
      <td>-3.011588</td>
      <td>-2.011588</td>
      <td>-1.011588</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>1.954196</td>
      <td>2.954196</td>
      <td>3.954196</td>
      <td>14.919981</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>-5.011588</td>
      <td>-4.011588</td>
      <td>-3.011588</td>
      <td>-2.011588</td>
      <td>-1.000000</td>
      <td>0.000000</td>
      <td>0.954196</td>
      <td>1.954196</td>
      <td>2.954196</td>
      <td>13.919981</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>-5.965784</td>
      <td>-4.965784</td>
      <td>-3.965784</td>
      <td>-2.965784</td>
      <td>-1.954196</td>
      <td>-0.954196</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>12.965784</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>-6.965784</td>
      <td>-5.965784</td>
      <td>-4.965784</td>
      <td>-3.965784</td>
      <td>-2.954196</td>
      <td>-1.954196</td>
      <td>-1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>11.965784</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>-7.965784</td>
      <td>-6.965784</td>
      <td>-5.965784</td>
      <td>-4.965784</td>
      <td>-3.954196</td>
      <td>-2.954196</td>
      <td>-2.000000</td>
      <td>-1.000000</td>
      <td>0.000000</td>
      <td>10.965784</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>-18.931569</td>
      <td>-17.931569</td>
      <td>-16.931569</td>
      <td>-15.931569</td>
      <td>-14.919981</td>
      <td>-13.919981</td>
      <td>-12.965784</td>
      <td>-11.965784</td>
      <td>-10.965784</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
HUMAN_FC_matrix
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>S01</th>
      <th>S02</th>
      <th>S03</th>
      <th>S04</th>
      <th>S05</th>
      <th>S06</th>
      <th>S07</th>
      <th>S08</th>
      <th>S09</th>
      <th>S10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S01</th>
      <td>0.000000</td>
      <td>-17.931569</td>
      <td>-18.516531</td>
      <td>-18.738923</td>
      <td>-18.839228</td>
      <td>-18.886137</td>
      <td>-18.908299</td>
      <td>-18.919981</td>
      <td>-18.925786</td>
      <td>-18.931569</td>
    </tr>
    <tr>
      <th>S02</th>
      <td>17.931569</td>
      <td>0.000000</td>
      <td>-0.584963</td>
      <td>-0.807355</td>
      <td>-0.907660</td>
      <td>-0.954569</td>
      <td>-0.976730</td>
      <td>-0.988412</td>
      <td>-0.994218</td>
      <td>-1.000000</td>
    </tr>
    <tr>
      <th>S03</th>
      <td>18.516531</td>
      <td>0.584963</td>
      <td>0.000000</td>
      <td>-0.222392</td>
      <td>-0.322697</td>
      <td>-0.369606</td>
      <td>-0.391768</td>
      <td>-0.403450</td>
      <td>-0.409255</td>
      <td>-0.415037</td>
    </tr>
    <tr>
      <th>S04</th>
      <td>18.738923</td>
      <td>0.807355</td>
      <td>0.222392</td>
      <td>0.000000</td>
      <td>-0.100305</td>
      <td>-0.147214</td>
      <td>-0.169375</td>
      <td>-0.181057</td>
      <td>-0.186863</td>
      <td>-0.192645</td>
    </tr>
    <tr>
      <th>S05</th>
      <td>18.839228</td>
      <td>0.907660</td>
      <td>0.322697</td>
      <td>0.100305</td>
      <td>0.000000</td>
      <td>-0.046909</td>
      <td>-0.069070</td>
      <td>-0.080752</td>
      <td>-0.086558</td>
      <td>-0.092340</td>
    </tr>
    <tr>
      <th>S06</th>
      <td>18.886137</td>
      <td>0.954569</td>
      <td>0.369606</td>
      <td>0.147214</td>
      <td>0.046909</td>
      <td>0.000000</td>
      <td>-0.022162</td>
      <td>-0.033843</td>
      <td>-0.039649</td>
      <td>-0.045431</td>
    </tr>
    <tr>
      <th>S07</th>
      <td>18.908299</td>
      <td>0.976730</td>
      <td>0.391768</td>
      <td>0.169375</td>
      <td>0.069070</td>
      <td>0.022162</td>
      <td>0.000000</td>
      <td>-0.011682</td>
      <td>-0.017487</td>
      <td>-0.023270</td>
    </tr>
    <tr>
      <th>S08</th>
      <td>18.919981</td>
      <td>0.988412</td>
      <td>0.403450</td>
      <td>0.181057</td>
      <td>0.080752</td>
      <td>0.033843</td>
      <td>0.011682</td>
      <td>0.000000</td>
      <td>-0.005806</td>
      <td>-0.011588</td>
    </tr>
    <tr>
      <th>S09</th>
      <td>18.925786</td>
      <td>0.994218</td>
      <td>0.409255</td>
      <td>0.186863</td>
      <td>0.086558</td>
      <td>0.039649</td>
      <td>0.017487</td>
      <td>0.005806</td>
      <td>0.000000</td>
      <td>-0.005782</td>
    </tr>
    <tr>
      <th>S10</th>
      <td>18.931569</td>
      <td>1.000000</td>
      <td>0.415037</td>
      <td>0.192645</td>
      <td>0.092340</td>
      <td>0.045431</td>
      <td>0.023270</td>
      <td>0.011588</td>
      <td>0.005782</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



### Thoughs on how to compute the fold change differential expression

For FC diff expression could we take the FC_matrix x ratio of the FC to get a treshold for what is considered FC differentially expressed?.

This fold change could for example be 0.8 of the true FC. Where we choose the ratio such that it allows for a small margin, write it as a formula so that we can change this treshold...



## 2020-12-10
### Continuing my work on differential expression

Just coded up from scripts for extracting protein abundances and proteins list from melted dataframes.


```python
os.chdir("/home/ptruong/git/bayesMS/bin")
from extract_from_melt import get_protein_abundance, get_proteins

```


```python
triq
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>q_value</th>
      <th>posterior_error_prob</th>
      <th>protein</th>
      <th>num_peptides</th>
      <th>protein_id_posterior_error_prob</th>
      <th>log2_fold_change</th>
      <th>diff_exp_prob_0.8</th>
      <th>sample</th>
      <th>run</th>
      <th>value</th>
      <th>peptide</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R01</td>
      <td>41.3300</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R02</td>
      <td>41.0700</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R03</td>
      <td>38.9800</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R04</td>
      <td>40.1300</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1.168000e-09</td>
      <td>1.168000e-09</td>
      <td>P02566_CAEEL</td>
      <td>152</td>
      <td>1.167000e-09</td>
      <td>5.84600</td>
      <td>9.828000e-14</td>
      <td>S01</td>
      <td>R05</td>
      <td>40.5900</td>
      <td>ELLLDLPIK;YKQLTHQLEDAEER;HPNFEKPKPPK;DLEEANM[1...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>543045</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R01</td>
      <td>1.0150</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
    <tr>
      <th>543046</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R02</td>
      <td>1.0360</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
    <tr>
      <th>543047</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R03</td>
      <td>1.0420</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
    <tr>
      <th>543048</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R04</td>
      <td>0.9652</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
    <tr>
      <th>543049</th>
      <td>9.537000e-01</td>
      <td>1.000000e+00</td>
      <td>Q0WLB5_ARATH</td>
      <td>66</td>
      <td>1.214000e-08</td>
      <td>-0.01544</td>
      <td>1.000000e+00</td>
      <td>S10</td>
      <td>R05</td>
      <td>0.9473</td>
      <td>DLLLVNLR;VAAYIYK;NFLM[16]EAK;EATSFLLDVLKPNLPEH...</td>
    </tr>
  </tbody>
</table>
<p>543050 rows × 11 columns</p>
</div>




```python
proteins = get_proteins(spec, "HUMAN") #FUNC TEST
proteins = get_proteins(triq, "HUMAN") #FUNC TEST
```


```python
samples = ["S0"+str(i) for i in range(1,10)] + ["S10"] 
species = ["ARATH", "CAEEL", "HUMAN"]

df = df_triq #variable
df = df_spec #variable

sample = samples[0] #Variable
specie = "HUMAN" #variable
protein = "Q8TBA6_HUMAN" #VAR

protein = proteins[0] #iteration variable (if the protein is diff exp)
    
    
```


```python
get_protein_abundance(triq, "S01", "HUMAN", protein) #FUNC TEST

```




    18550    0.7940
    18551    1.3410
    18552    0.4786
    18553    1.6060
    18554    0.1356
    Name: value, dtype: float64



I want to compute a pairwise log2FC between samples for each protein and run. i.e. a dataframe similar to 

| Protein | Run1 | Run2 | Run3 | Run4 | Run5 |
|---------|------|------|------|------|------|
| P1      | .    |      |      |      |      |
| P2      |      | .    |      |      |      |
| ...     |      |      | .    |      |      |
| Pn      |      |      |      | .    | ...  |

will be generated for each pair SX vs XY. Then we can treshold this table and count the logFC differential expression. Either by 

1) Treshold by FC and setting if >3 proteins are differntially expressed than it is a differentially expressed protein or
2) Count the total number of differentially expressed proteins (which should be better for triqler, since we cannot compare with NaN).

However, the code to produce this dataframe (below) is very slow. It takes about 15min for each pairwise matrix to be construction. For 45 comparisons it will take 675min (i.e) 11 hours. I will try to parallize the computation to save some time.


```python
import time
start = time.time()

sample1 = "S02" #Var
sample2 = "S06" #Var
specie = "HUMAN" #Var
protein = proteins[0] #Var

log2FC_array = []
for protein in proteins:
    abundance_sample1 = get_protein_abundance(df, sample1, specie, protein)
    abundance_sample2 = get_protein_abundance(df, sample2, specie, protein)
    log2FC = np.log2(abundance_sample2) - np.log2(abundance_sample1)
    log2FC_array.append(log2FC)
    #break # ADDED JUST IN CASE WE RUN CELL - IT TAKES 15min on Planck.
end = time.time()
print(end-start)

```

    755.7753973007202


The library joblib has a simple process for performing embarrasingly parallell jobs.


```python
# Example script

# Sequential
from math import sqrt
test= []
for i in range(10):
    test.append(sqrt(i**2))

# Parallell
from math import sqrt
from joblib import Parallel, delayed
Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
```




    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]




```python

def parallel_get_protein(df, protein, sample1, sample2, specie):
    abundance_sample1 = get_protein_abundance(df, sample1, specie, protein)
    abundance_sample2 = get_protein_abundance(df, sample2, specie, protein)
    log2FC = np.log2(abundance_sample2.values) - np.log2(abundance_sample1.values)
    return log2FC

import multiprocessing
num_cores = multiprocessing.cpu_count()

sample1 = "S02" #VAR
sample2 = "S06" #VAR
specie = "HUMAN" #VAR
df = triq #VAR



```


```python
parallel_get_protein(df, protein, sample1, sample2, specie)
```




    array([1.25103933, 1.14043778, 1.16028107, 1.14924195, 1.21299372])




```python
start=time.time()
log2FC_array = Parallel(n_jobs=num_cores)(delayed(parallel_get_protein)(df, protein, sample1, sample2, specie) for protein in proteins)
end=time.time()
print(time.time())

```

    exception calling callback for <Future at 0x7f420ded0f60 state=finished raised BrokenProcessPool>
    joblib.externals.loky.process_executor._RemoteTraceback: 
    """
    Traceback (most recent call last):
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/externals/loky/process_executor.py", line 404, in _process_worker
        call_item = call_queue.get(block=True, timeout=timeout)
      File "/home/ptruong/anaconda3/lib/python3.6/multiprocessing/queues.py", line 113, in get
        return _ForkingPickler.loads(res)
    ModuleNotFoundError: No module named 'extract_from_melt'
    """
    
    The above exception was the direct cause of the following exception:
    
    Traceback (most recent call last):
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/externals/loky/_base.py", line 625, in _invoke_callbacks
        callback(self)
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/parallel.py", line 366, in __call__
        self.parallel.dispatch_next()
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/parallel.py", line 799, in dispatch_next
        if not self.dispatch_one_batch(self._original_iterator):
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/parallel.py", line 866, in dispatch_one_batch
        self._dispatch(tasks)
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/parallel.py", line 784, in _dispatch
        job = self._backend.apply_async(batch, callback=cb)
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/_parallel_backends.py", line 531, in apply_async
        future = self._workers.submit(SafeFunction(func))
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/externals/loky/reusable_executor.py", line 178, in submit
        fn, *args, **kwargs)
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/externals/loky/process_executor.py", line 1102, in submit
        raise self._flags.broken
    joblib.externals.loky.process_executor.BrokenProcessPool: A task has failed to un-serialize. Please ensure that the arguments of the function are all picklable.



    ---------------------------------------------------------------------------

    _RemoteTraceback                          Traceback (most recent call last)

    _RemoteTraceback: 
    """
    Traceback (most recent call last):
      File "/home/ptruong/anaconda3/lib/python3.6/site-packages/joblib/externals/loky/process_executor.py", line 404, in _process_worker
        call_item = call_queue.get(block=True, timeout=timeout)
      File "/home/ptruong/anaconda3/lib/python3.6/multiprocessing/queues.py", line 113, in get
        return _ForkingPickler.loads(res)
    ModuleNotFoundError: No module named 'extract_from_melt'
    """

    
    The above exception was the direct cause of the following exception:


    BrokenProcessPool                         Traceback (most recent call last)

    <ipython-input-155-12099593d474> in <module>
          1 start=time.time()
    ----> 2 log2FC_array = Parallel(n_jobs=num_cores)(delayed(parallel_get_protein)(df, protein, sample1, sample2, specie) for protein in proteins)
          3 end=time.time()
          4 print(time.time())


    ~/anaconda3/lib/python3.6/site-packages/joblib/parallel.py in __call__(self, iterable)
       1059 
       1060             with self._backend.retrieval_context():
    -> 1061                 self.retrieve()
       1062             # Make sure that we get a last message telling us we are done
       1063             elapsed_time = time.time() - self._start_time


    ~/anaconda3/lib/python3.6/site-packages/joblib/parallel.py in retrieve(self)
        938             try:
        939                 if getattr(self._backend, 'supports_timeout', False):
    --> 940                     self._output.extend(job.get(timeout=self.timeout))
        941                 else:
        942                     self._output.extend(job.get())


    ~/anaconda3/lib/python3.6/site-packages/joblib/_parallel_backends.py in wrap_future_result(future, timeout)
        540         AsyncResults.get from multiprocessing."""
        541         try:
    --> 542             return future.result(timeout=timeout)
        543         except CfTimeoutError as e:
        544             raise TimeoutError from e


    ~/anaconda3/lib/python3.6/concurrent/futures/_base.py in result(self, timeout)
        430                 raise CancelledError()
        431             elif self._state == FINISHED:
    --> 432                 return self.__get_result()
        433             else:
        434                 raise TimeoutError()


    ~/anaconda3/lib/python3.6/concurrent/futures/_base.py in __get_result(self)
        382     def __get_result(self):
        383         if self._exception:
    --> 384             raise self._exception
        385         else:
        386             return self._result


    ~/anaconda3/lib/python3.6/site-packages/joblib/externals/loky/_base.py in _invoke_callbacks(self)
        623         for callback in self._done_callbacks:
        624             try:
    --> 625                 callback(self)
        626             except BaseException:
        627                 LOGGER.exception('exception calling callback for %r', self)


    ~/anaconda3/lib/python3.6/site-packages/joblib/parallel.py in __call__(self, out)
        364         with self.parallel._lock:
        365             if self.parallel._original_iterator is not None:
    --> 366                 self.parallel.dispatch_next()
        367 
        368 


    ~/anaconda3/lib/python3.6/site-packages/joblib/parallel.py in dispatch_next(self)
        797 
        798         """
    --> 799         if not self.dispatch_one_batch(self._original_iterator):
        800             self._iterating = False
        801             self._original_iterator = None


    ~/anaconda3/lib/python3.6/site-packages/joblib/parallel.py in dispatch_one_batch(self, iterator)
        864                 return False
        865             else:
    --> 866                 self._dispatch(tasks)
        867                 return True
        868 


    ~/anaconda3/lib/python3.6/site-packages/joblib/parallel.py in _dispatch(self, batch)
        782         with self._lock:
        783             job_idx = len(self._jobs)
    --> 784             job = self._backend.apply_async(batch, callback=cb)
        785             # A job can complete so quickly than its callback is
        786             # called before we get here, causing self._jobs to


    ~/anaconda3/lib/python3.6/site-packages/joblib/_parallel_backends.py in apply_async(self, func, callback)
        529     def apply_async(self, func, callback=None):
        530         """Schedule a func to be run"""
    --> 531         future = self._workers.submit(SafeFunction(func))
        532         future.get = functools.partial(self.wrap_future_result, future)
        533         if callback is not None:


    ~/anaconda3/lib/python3.6/site-packages/joblib/externals/loky/reusable_executor.py in submit(self, fn, *args, **kwargs)
        176         with self._submit_resize_lock:
        177             return super(_ReusablePoolExecutor, self).submit(
    --> 178                 fn, *args, **kwargs)
        179 
        180     def _resize(self, max_workers):


    ~/anaconda3/lib/python3.6/site-packages/joblib/externals/loky/process_executor.py in submit(self, fn, *args, **kwargs)
       1100         with self._flags.shutdown_lock:
       1101             if self._flags.broken is not None:
    -> 1102                 raise self._flags.broken
       1103             if self._flags.shutdown:
       1104                 raise ShutdownExecutorError(


    BrokenProcessPool: A task has failed to un-serialize. Please ensure that the arguments of the function are all picklable.


BrokenProcessPool: A task has failed to un-serialize. Please ensure that the arguments of the function are all picklable.

This always happens when using multiprocessing in an iPython console in Spyder. A workaround is to run the script from the command line instead. 

(https://stackoverflow.com/questions/56154654/a-task-failed-to-un-serialize)

Write about the wierd parallel processing timing...



```python

from math import sqrt
test= []
for i in range(10):
    test.append(sqrt(i**2))

from math import sqrt
from joblib import Parallel, delayed
test2 = Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))

g = "g"
def get_val(x,g):
    return str(x)+str("_tetst")+str(g)


```


```python

# write about this timing thingy here... wierd...
start=time.time()
test3 = Parallel(n_jobs=1)(delayed(get_val)(i,g) for i in ["a","b","c","d","e","b","c","d","e","b","c","d","e"])
end=time.time()
print(end-start)

```

    0.0007114410400390625



```python

# write about this timing thingy here... wierd...
start=time.time()
test3 = Parallel(n_jobs=8)(delayed(get_val)(i,g) for i in ["a","b","c","d","e","b","c","d","e","b","c","d","e"])
end=time.time()
print(end-start)

```

    0.2426769733428955


I wonder why it is so much slower (joblid)... the computations for log2FC is also much slower, it never finished before 15min... so I just ran some samples while in gym. 


```python

def get_log2FC_matrix(df, sample1, sample2, specie):
    proteins = get_proteins(df, specie) 
    runs = ["R0"+str(i) for i in range(1,6)]
    log2FC_array = []
    start=time.time()
    i = 0
    for protein in proteins:
        if i%200 == 0:
            print(str(i) + "/" + str(len(proteins)))
        log2FC_array.append(parallel_get_protein(df, protein, sample1, sample2, specie))
        i+=1
    end=time.time()
    print(end-start)
    df_log2FC = pd.DataFrame(log2FC_array, index=proteins, columns=runs)
    return df_log2FC

    df_log2FC = pd.DataFrame(log2FC_array, index=proteins, columns=runs).to_csv("spec_log2FC_S02_S06_HUMAN.csv", sep = "\t", index=False)

```

Hardcoding since the joblib did not work... let it run when im at the gym


```python

print(1)
df_log2FC = get_log2FC_matrix(triq, "S02", "S06", "HUMAN")
df_log2FC.to_csv("triq_log2FC_S02_S06_HUMAN.csv", sep = "\t", index=False)
print(2)
df_log2FC = get_log2FC_matrix(triq, "S02", "S06", "CAEEL")
df_log2FC.to_csv("troq_log2FC_S02_S06_CAEEL.csv", sep = "\t", index=False)
print(3)
df_log2FC = get_log2FC_matrix(triq, "S02", "S06", "ARATH")
df_log2FC.to_csv("troq_log2FC_S02_S06_ARATH.csv", sep = "\t", index=False)
print(4)
df_log2FC = get_log2FC_matrix(spec, "S02", "S06", "CAEEL")
df_log2FC.to_csv("spec_log2FC_S02_S06_CAEEL.csv", sep = "\t", index=False)
print(5)
df_log2FC = get_log2FC_matrix(spec, "S02", "S06", "ARATH")
df_log2FC.to_csv("spec_log2FC_S02_S06_ARATH.csv", sep = "\t", index=False)

print(6)
df_log2FC = get_log2FC_matrix(triq, "S03", "S04", "HUMAN")
df_log2FC.to_csv("triq_log2FC_S03_S04_HUMAN.csv", sep = "\t", index=False)
print(7)
df_log2FC = get_log2FC_matrix(triq, "S03", "S04", "CAEEL")
df_log2FC.to_csv("triq_log2FC_S03_S04_CAEEL.csv", sep = "\t", index=False)
print(8)
df_log2FC = get_log2FC_matrix(triq, "S03", "S04", "ARATH")
df_log2FC.to_csv("triq_log2FC_S03_S04_ARATH.csv", sep = "\t", index=False)
print(9)
df_log2FC = get_log2FC_matrix(spec, "S03", "S04", "HUMAN")
df_log2FC.to_csv("spec_log2FC_S03_S04_HUMAN.csv", sep = "\t", index=False)
print(10)
df_log2FC = get_log2FC_matrix(spec, "S03", "S04", "CAEEL")
df_log2FC.to_csv("spec_log2FC_S03_S04_CAEEL.csv", sep = "\t", index=False)
print(11)
df_log2FC = get_log2FC_matrix(spec, "S03", "S04", "ARATH")
df_log2FC.to_csv("spec_log2FC_S03_S04_ARATH.csv", sep = "\t", index=False)

print(12)
df_log2FC = get_log2FC_matrix(triq, "S05", "S08", "HUMAN")
df_log2FC.to_csv("triq_log2FC_S05_S08_HUMAN.csv", sep = "\t", index=False)
print(13)
df_log2FC = get_log2FC_matrix(triq, "S05", "S08", "CAEEL")
df_log2FC.to_csv("triq_log2FC_S05_S08_CAEEL.csv", sep = "\t", index=False)
print(14)
df_log2FC = get_log2FC_matrix(triq, "S05", "S08", "ARATH")
df_log2FC.to_csv("triq_log2FC_S05_S08_ARATH.csv", sep = "\t", index=False)
print(15)
df_log2FC = get_log2FC_matrix(spec, "S05", "S08", "HUMAN")
df_log2FC.to_csv("spec_log2FC_S05_S08_HUMAN.csv", sep = "\t", index=False)
print(16)
df_log2FC = get_log2FC_matrix(spec, "S05", "S08", "CAEEL")
df_log2FC.to_csv("spec_log2FC_S05_S08_CAEEL.csv", sep = "\t", index=False)
print(17)
df_log2FC = get_log2FC_matrix(spec, "S05", "S08", "ARATH")
df_log2FC.to_csv("spec_log2FC_S05_S08_ARATH.csv", sep = "\t", index=False)
print(18)
df_log2FC = get_log2FC_matrix(triq, "S04", "S09", "HUMAN")
df_log2FC.to_csv("triq_log2FC_S04_S09_HUMAN.csv", sep = "\t", index=False)
print(19)
df_log2FC = get_log2FC_matrix(triq, "S04", "S09", "CAEEL")
df_log2FC.to_csv("triq_log2FC_S04_S09_CAEEL.csv", sep = "\t", index=False)
print(20)
df_log2FC = get_log2FC_matrix(triq, "S04", "S09", "ARATH")
df_log2FC.to_csv("triq_log2FC_S04_S09_ARATH.csv", sep = "\t", index=False)
print(21)
df_log2FC = get_log2FC_matrix(spec, "S04", "S09", "HUMAN")
df_log2FC.to_csv("spec_log2FC_S04_S09_HUMAN.csv", sep = "\t", index=False)
print(22)
df_log2FC = get_log2FC_matrix(spec, "S04", "S09", "CAEEL")
df_log2FC.to_csv("spec_log2FC_S04_S09_CAEEL.csv", sep = "\t", index=False)
print(23)
df_log2FC = get_log2FC_matrix(spec, "S04", "S09", "ARATH")
df_log2FC.to_csv("spec_log2FC_S04_S09_ARATH.csv", sep = "\t", index=False)
print("DONE!")

```

    1
    0/5593
    200/5593
    400/5593
    600/5593
    800/5593
    1000/5593
    1200/5593
    1400/5593
    1600/5593
    1800/5593
    2000/5593
    2200/5593
    2400/5593
    2600/5593
    2800/5593
    3000/5593
    3200/5593
    3400/5593
    3600/5593
    3800/5593
    4000/5593
    4200/5593
    4400/5593
    4600/5593
    4800/5593
    5000/5593
    5200/5593
    5400/5593
    422.6912865638733
    2
    0/1472
    200/1472
    400/1472
    600/1472
    800/1472
    1000/1472
    1200/1472
    1400/1472
    100.4037938117981
    3
    0/3796
    200/3796
    400/3796
    600/3796
    800/3796
    1000/3796
    1200/3796
    1400/3796
    1600/3796
    1800/3796
    2000/3796
    2200/3796
    2400/3796
    2600/3796
    2800/3796
    3000/3796
    3200/3796
    3400/3796
    3600/3796
    273.03745770454407
    4
    0/4211
    200/4211
    400/4211
    600/4211
    800/4211
    1000/4211
    1200/4211
    1400/4211
    1600/4211
    1800/4211
    2000/4211
    2200/4211
    2400/4211
    2600/4211
    2800/4211
    3000/4211
    3200/4211
    3400/4211
    3600/4211
    3800/4211
    4000/4211
    4200/4211
    360.48885440826416
    5
    0/4620
    200/4620
    400/4620
    600/4620
    800/4620
    1000/4620
    1200/4620
    1400/4620
    1600/4620
    1800/4620
    2000/4620
    2200/4620
    2400/4620
    2600/4620
    2800/4620
    3000/4620
    3200/4620
    3400/4620
    3600/4620
    3800/4620
    4000/4620
    4200/4620
    4400/4620
    4600/4620
    398.10421776771545
    6
    0/5593
    200/5593
    400/5593
    600/5593
    800/5593
    1000/5593
    1200/5593
    1400/5593
    1600/5593
    1800/5593
    2000/5593
    2200/5593
    2400/5593
    2600/5593
    2800/5593
    3000/5593
    3200/5593
    3400/5593
    3600/5593
    3800/5593
    4000/5593
    4200/5593
    4400/5593
    4600/5593
    4800/5593
    5000/5593
    5200/5593
    5400/5593
    421.7850704193115
    7
    0/1472
    200/1472
    400/1472
    600/1472
    800/1472
    1000/1472
    1200/1472
    1400/1472
    100.94081354141235
    8
    0/3796
    200/3796
    400/3796
    600/3796
    800/3796
    1000/3796
    1200/3796
    1400/3796
    1600/3796
    1800/3796
    2000/3796
    2200/3796
    2400/3796
    2600/3796
    2800/3796
    3000/3796
    3200/3796
    3400/3796
    3600/3796
    274.5622580051422
    9
    0/6183
    200/6183
    400/6183
    600/6183
    800/6183
    1000/6183
    1200/6183
    1400/6183
    1600/6183
    1800/6183
    2000/6183
    2200/6183
    2400/6183
    2600/6183
    2800/6183
    3000/6183
    3200/6183
    3400/6183
    3600/6183
    3800/6183
    4000/6183
    4200/6183
    4400/6183
    4600/6183
    4800/6183
    5000/6183
    5200/6183
    5400/6183
    5600/6183
    5800/6183
    6000/6183
    545.6345722675323
    10
    0/4211
    200/4211
    400/4211
    600/4211
    800/4211
    1000/4211
    1200/4211
    1400/4211
    1600/4211
    1800/4211
    2000/4211
    2200/4211
    2400/4211
    2600/4211
    2800/4211
    3000/4211
    3200/4211
    3400/4211
    3600/4211
    3800/4211
    4000/4211
    4200/4211
    362.08672857284546
    11
    0/4620
    200/4620
    400/4620
    600/4620
    800/4620
    1000/4620
    1200/4620
    1400/4620
    1600/4620
    1800/4620
    2000/4620
    2200/4620
    2400/4620
    2600/4620
    2800/4620
    3000/4620
    3200/4620
    3400/4620
    3600/4620
    3800/4620
    4000/4620
    4200/4620
    4400/4620
    4600/4620
    399.01437854766846
    12
    0/5593
    200/5593
    400/5593
    600/5593
    800/5593
    1000/5593
    1200/5593
    1400/5593
    1600/5593
    1800/5593
    2000/5593
    2200/5593
    2400/5593
    2600/5593
    2800/5593
    3000/5593
    3200/5593
    3400/5593
    3600/5593
    3800/5593
    4000/5593
    4200/5593
    4400/5593
    4600/5593
    4800/5593
    5000/5593
    5200/5593
    5400/5593
    419.50996351242065
    13
    0/1472
    200/1472
    400/1472
    600/1472
    800/1472
    1000/1472
    1200/1472
    1400/1472
    100.6195158958435
    14
    0/3796
    200/3796
    400/3796
    600/3796
    800/3796
    1000/3796
    1200/3796
    1400/3796
    1600/3796
    1800/3796
    2000/3796
    2200/3796
    2400/3796
    2600/3796
    2800/3796
    3000/3796
    3200/3796
    3400/3796
    3600/3796
    273.7214152812958
    15
    0/6183
    200/6183
    400/6183
    600/6183
    800/6183
    1000/6183
    1200/6183
    1400/6183
    1600/6183
    1800/6183
    2000/6183
    2200/6183
    2400/6183
    2600/6183
    2800/6183
    3000/6183
    3200/6183
    3400/6183
    3600/6183
    3800/6183
    4000/6183
    4200/6183
    4400/6183
    4600/6183
    4800/6183
    5000/6183
    5200/6183
    5400/6183
    5600/6183
    5800/6183
    6000/6183
    546.1721587181091
    16
    0/4211
    200/4211
    400/4211
    600/4211
    800/4211
    1000/4211
    1200/4211
    1400/4211
    1600/4211
    1800/4211
    2000/4211
    2200/4211
    2400/4211
    2600/4211
    2800/4211
    3000/4211
    3200/4211
    3400/4211
    3600/4211
    3800/4211
    4000/4211
    4200/4211
    360.6661376953125
    17
    0/4620
    200/4620
    400/4620
    600/4620
    800/4620
    1000/4620
    1200/4620
    1400/4620
    1600/4620
    1800/4620
    2000/4620
    2200/4620
    2400/4620
    2600/4620
    2800/4620
    3000/4620
    3200/4620
    3400/4620
    3600/4620
    3800/4620
    4000/4620
    4200/4620
    4400/4620
    4600/4620
    399.0610158443451
    18
    0/5593
    200/5593
    400/5593
    600/5593
    800/5593
    1000/5593
    1200/5593
    1400/5593
    1600/5593
    1800/5593
    2000/5593
    2200/5593
    2400/5593
    2600/5593
    2800/5593
    3000/5593
    3200/5593
    3400/5593
    3600/5593
    3800/5593
    4000/5593
    4200/5593
    4400/5593
    4600/5593
    4800/5593
    5000/5593
    5200/5593
    5400/5593
    421.1472773551941
    19
    0/1472
    200/1472
    400/1472
    600/1472
    800/1472
    1000/1472
    1200/1472
    1400/1472
    101.06039953231812
    20
    0/3796
    200/3796
    400/3796
    600/3796
    800/3796
    1000/3796
    1200/3796
    1400/3796
    1600/3796
    1800/3796
    2000/3796
    2200/3796
    2400/3796
    2600/3796
    2800/3796
    3000/3796
    3200/3796
    3400/3796
    3600/3796
    274.2331681251526
    21
    0/6183
    200/6183
    400/6183
    600/6183
    800/6183
    1000/6183
    1200/6183
    1400/6183
    1600/6183
    1800/6183
    2000/6183
    2200/6183
    2400/6183
    2600/6183
    2800/6183
    3000/6183
    3200/6183
    3400/6183
    3600/6183
    3800/6183
    4000/6183
    4200/6183
    4400/6183
    4600/6183
    4800/6183
    5000/6183
    5200/6183
    5400/6183
    5600/6183
    5800/6183
    6000/6183
    543.7764277458191
    22
    0/4211
    200/4211
    400/4211
    600/4211
    800/4211
    1000/4211
    1200/4211
    1400/4211
    1600/4211
    1800/4211
    2000/4211
    2200/4211
    2400/4211
    2600/4211
    2800/4211
    3000/4211
    3200/4211
    3400/4211
    3600/4211
    3800/4211
    4000/4211
    4200/4211
    360.48128175735474
    23
    0/4620
    200/4620
    400/4620
    600/4620
    800/4620
    1000/4620
    1200/4620
    1400/4620
    1600/4620
    1800/4620
    2000/4620
    2200/4620
    2400/4620
    2600/4620
    2800/4620
    3000/4620
    3200/4620
    3400/4620
    3600/4620
    3800/4620
    4000/4620
    4200/4620
    4400/4620
    4600/4620
    397.95293641090393
    DONE!


We see that some samples have less protein and take way less than 15min to run.  So it might be feasible to get the runs quite quickly after all. Lets do a code for this later, now I want to complete the analysis.


```python
df_log2FC

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R01</th>
      <th>R02</th>
      <th>R03</th>
      <th>R04</th>
      <th>R05</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A0A1P8AUY4</th>
      <td>0.190271</td>
      <td>-0.172924</td>
      <td>0.992776</td>
      <td>-0.710468</td>
      <td>0.295473</td>
    </tr>
    <tr>
      <th>A0MFS5</th>
      <td>0.314738</td>
      <td>-0.304560</td>
      <td>-0.046011</td>
      <td>-0.142394</td>
      <td>0.123230</td>
    </tr>
    <tr>
      <th>A1A6M1</th>
      <td>0.045143</td>
      <td>-0.039569</td>
      <td>-0.031675</td>
      <td>0.082436</td>
      <td>-0.056626</td>
    </tr>
    <tr>
      <th>A1L4X7</th>
      <td>0.279982</td>
      <td>-6.314680</td>
      <td>0.403772</td>
      <td>-0.886979</td>
      <td>0.037891</td>
    </tr>
    <tr>
      <th>A1L4Y2</th>
      <td>-0.573467</td>
      <td>-0.547050</td>
      <td>-0.521499</td>
      <td>-0.338061</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>Q9ZWJ3</th>
      <td>0.243150</td>
      <td>0.130662</td>
      <td>0.133022</td>
      <td>-0.244746</td>
      <td>0.116473</td>
    </tr>
    <tr>
      <th>Q9ZWT1</th>
      <td>NaN</td>
      <td>0.161794</td>
      <td>0.542331</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Q9ZWT2</th>
      <td>0.689017</td>
      <td>0.528014</td>
      <td>0.418026</td>
      <td>0.011134</td>
      <td>0.008915</td>
    </tr>
    <tr>
      <th>X5JA13</th>
      <td>0.592807</td>
      <td>-0.553747</td>
      <td>-0.015328</td>
      <td>0.040232</td>
      <td>0.044947</td>
    </tr>
    <tr>
      <th>X5JB51</th>
      <td>-0.161275</td>
      <td>-0.138268</td>
      <td>2.972913</td>
      <td>-0.063825</td>
      <td>-0.023935</td>
    </tr>
  </tbody>
</table>
<p>4620 rows × 5 columns</p>
</div>



### 2020-12-11 Cont. on diff expression


```python
# refresh imports 

import os 
import time

import pandas as pd
import numpy as np 


```


```python
os.chdir("/home/ptruong/git/bayesMS/bin")
from read_triqler_output import read_triqler_protein_output_to_df
from triqler_output_df_melter import melt_spectronaut_triqler_formatted, melt_triqler_output
from normalize_melted import normalize_within_sample, get_ratios_from_normalized_melted_df
from constants import get_sample_ratios, get_log2FC_ratio_matrix, get_log2FC_ratio_matrices
from extract_from_melt import get_protein_abundance, get_proteins
from log2fc_from_melt import get_log2FC_matrix
from log2fc_from_melt_computation import get_differentially_expressed_proteins_from_log2FC_df


```


```python
os.chdir("/home/ptruong/git/bayesMS/data/log2FC_2020-12-10")
```

Differentially expressed per sample all for the same ratio (=0.8) of the true FC are counted as differentially expressed.


```python
##########################################################################################
# WE DONT NEED TO LOOK AT THIS CODE IT IS JUST USED TO GENERATE SOME SAMPLE COMPARISONS. #
##########################################################################################
#S02 vs S06
triq_s02_s06_HUMAN_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S02", "S06", "HUMAN", 0.8)
spec_s02_s06_HUMAN_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S02", "S06", "HUMAN", 0.8)
triq_s02_s06_CAEEL_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S02", "S06", "CAEEL", 0.8)
spec_s02_s06_CAEEL_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S02", "S06", "CAEEL", 0.8)
triq_s02_s06_ARATH_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S02", "S06", "ARATH", 0.8)
spec_s02_s06_ARATH_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S02", "S06", "ARATH", 0.8)

triq_s02_s06_HUMAN_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S02", "S06", "HUMAN", 0.8))
spec_s02_s06_HUMAN_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S02", "S06", "HUMAN", 0.8))
triq_s02_s06_CAEEL_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S02", "S06", "CAEEL", 0.8))
spec_s02_s06_CAEEL_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S02", "S06", "CAEEL", 0.8))
triq_s02_s06_ARATH_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S02", "S06", "ARATH", 0.8))
spec_s02_s06_ARATH_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S02", "S06", "ARATH", 0.8))

#S03 vs S04
triq_s03_s04_HUMAN_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S03", "S04", "HUMAN", 0.8)
spec_s03_s04_HUMAN_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S03", "S04", "HUMAN", 0.8)
triq_s03_s04_CAEEL_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S03", "S04", "CAEEL", 0.8)
spec_s03_s04_CAEEL_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S03", "S04", "CAEEL", 0.8)
triq_s03_s04_ARATH_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S03", "S04", "ARATH", 0.8)
spec_s03_s04_ARATH_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S03", "S04", "ARATH", 0.8)

triq_s03_s04_HUMAN_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S03", "S04", "HUMAN", 0.8))
spec_s03_s04_HUMAN_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S03", "S04", "HUMAN", 0.8))
triq_s03_s04_CAEEL_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S03", "S04", "CAEEL", 0.8))
spec_s03_s04_CAEEL_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S03", "S04", "CAEEL", 0.8))
triq_s03_s04_ARATH_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S03", "S04", "ARATH", 0.8))
spec_s03_s04_ARATH_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S03", "S04", "ARATH", 0.8))

#S04 vs S09
triq_s04_s09_HUMAN_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S04", "S09", "HUMAN", 0.8)
spec_s04_s09_HUMAN_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S04", "S09", "HUMAN", 0.8)
triq_s04_s09_CAEEL_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S04", "S09", "CAEEL", 0.8)
spec_s04_s09_CAEEL_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S04", "S09", "CAEEL", 0.8)
triq_s04_s09_ARATH_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S04", "S09", "ARATH", 0.8)
spec_s04_s09_ARATH_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S04", "S09", "ARATH", 0.8)

triq_s04_s09_HUMAN_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S04", "S09", "HUMAN", 0.8))
spec_s04_s09_HUMAN_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S04", "S09", "HUMAN", 0.8))
triq_s04_s09_CAEEL_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S04", "S09", "CAEEL", 0.8))
spec_s04_s09_CAEEL_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S04", "S09", "CAEEL", 0.8))
triq_s04_s09_ARATH_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S04", "S09", "ARATH", 0.8))
spec_s04_s09_ARATH_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S04", "S09", "ARATH", 0.8))

#S05 vs S08
triq_s05_s08_HUMAN_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S05", "S08", "HUMAN", 0.8)
spec_s05_s08_HUMAN_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S05", "S08", "HUMAN", 0.8)
triq_s05_s08_CAEEL_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S05", "S08", "CAEEL", 0.8)
spec_s05_s08_CAEEL_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S05", "S08", "CAEEL", 0.8)
triq_s05_s08_ARATH_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("triq", "S05", "S08", "ARATH", 0.8)
spec_s05_s08_ARATH_diff_exp = get_differentially_expressed_proteins_from_log2FC_df("spec", "S05", "S08", "ARATH", 0.8)

triq_s05_s08_HUMAN_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S05", "S08", "HUMAN", 0.8))
spec_s05_s08_HUMAN_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S05", "S08", "HUMAN", 0.8))
triq_s05_s08_CAEEL_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S05", "S08", "CAEEL", 0.8))
spec_s05_s08_CAEEL_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S05", "S08", "CAEEL", 0.8))
triq_s05_s08_ARATH_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("triq", "S05", "S08", "ARATH", 0.8))
spec_s05_s08_ARATH_diff_exp_tot = np.sum(get_differentially_expressed_proteins_from_log2FC_df("spec", "S05", "S08", "ARATH", 0.8))

```


```python
print("S02 vs S06")
# S02 vs S06
print("Triqler S02 vs S06, HUMAN")
print(triq_s02_s06_HUMAN_diff_exp) 
print("Total different expression: " + str(triq_s02_s06_HUMAN_diff_exp_tot)) 
print("")
print("Spectronaut S02 vs S06, HUMAN")    
print(spec_s02_s06_HUMAN_diff_exp)
print("Total different expression: " + str(spec_s02_s06_HUMAN_diff_exp_tot)) 
print("")
print("Triqler S02 vs S06, CAEEL")
print(triq_s02_s06_CAEEL_diff_exp) 
print("Total different expression: " + str(triq_s02_s06_CAEEL_diff_exp_tot)) 
print("")
print("Spectronaut S02 vs S06, CAEEL")    
print(spec_s02_s06_CAEEL_diff_exp) 
print("Total different expression: " + str(spec_s02_s06_CAEEL_diff_exp_tot)) 
print("")
print("Triqler S02 vs S06, ARATH")
print(triq_s02_s06_ARATH_diff_exp) 
print("Total different expression: " + str(triq_s02_s06_ARATH_diff_exp_tot)) 
print("")
print("Spectronaut S02 vs S06, ARATH")    
print(spec_s02_s06_ARATH_diff_exp) 
print("Total different expression: " + str(spec_s02_s06_ARATH_diff_exp_tot)) 
print("")

print("S03 vs S04")
#S03 vs S04
print("Triqler S03 vs S04, HUMAN")
print(triq_s03_s04_HUMAN_diff_exp) 
print("Total different expression: " + str(triq_s03_s04_HUMAN_diff_exp_tot)) 
print("")
print("Spectronaut S03 vs S04, HUMAN")    
print(spec_s03_s04_HUMAN_diff_exp)
print("Total different expression: " + str(spec_s03_s04_HUMAN_diff_exp_tot)) 
print("")
print("Triqler S03 vs S04, CAEEL")
print(triq_s03_s04_CAEEL_diff_exp) 
print("Total different expression: " + str(triq_s03_s04_CAEEL_diff_exp_tot)) 
print("")
print("Spectronaut S03 vs S04, CAEEL")    
print(spec_s03_s04_CAEEL_diff_exp) 
print("Total different expression: " + str(spec_s03_s04_CAEEL_diff_exp_tot)) 
print("")
print("Triqler S03 vs S04, ARATH")
print(triq_s03_s04_ARATH_diff_exp) 
print("Total different expression: " + str(triq_s03_s04_ARATH_diff_exp_tot)) 
print("")
print("Spectronaut S03 vs S04, ARATH")    
print(spec_s03_s04_ARATH_diff_exp) 
print("Total different expression: " + str(spec_s03_s04_ARATH_diff_exp_tot)) 
print("")


#S04 vs S09
print("S04 vs S09")
print("Triqler S04 vs S09, HUMAN")
print(triq_s04_s09_HUMAN_diff_exp) 
print("Total different expression: " + str(triq_s04_s09_HUMAN_diff_exp_tot)) 
print("")
print("Spectronaut S04 vs S09, HUMAN")    
print(spec_s04_s09_HUMAN_diff_exp)
print("Total different expression: " + str(spec_s04_s09_HUMAN_diff_exp_tot)) 
print("")
print("Triqler S04 vs S09, CAEEL")
print(triq_s04_s09_CAEEL_diff_exp) 
print("Total different expression: " + str(triq_s04_s09_CAEEL_diff_exp_tot)) 
print("")
print("Spectronaut S04 vs S09, CAEEL")    
print(spec_s04_s09_CAEEL_diff_exp) 
print("Total different expression: " + str(spec_s04_s09_CAEEL_diff_exp_tot)) 
print("")
print("Triqler S04 vs S09, ARATH")
print(triq_s04_s09_ARATH_diff_exp) 
print("Total different expression: " + str(triq_s04_s09_ARATH_diff_exp_tot)) 
print("")
print("Spectronaut S04 vs S09, ARATH")    
print(spec_s04_s09_ARATH_diff_exp) 
print("Total different expression: " + str(spec_s04_s09_ARATH_diff_exp_tot)) 
print("")

#S05 vs S08
print("S05 vs S08")
print("Triqler S05 vs S08, HUMAN")
print(triq_s05_s08_HUMAN_diff_exp) 
print("Total different expression: " + str(triq_s05_s08_HUMAN_diff_exp_tot)) 
print("")
print("Spectronaut S05 vs S08, HUMAN")    
print(spec_s05_s08_HUMAN_diff_exp)
print("Total different expression: " + str(spec_s05_s08_HUMAN_diff_exp_tot)) 
print("")
print("Triqler S05 vs S08, CAEEL")
print(triq_s05_s08_CAEEL_diff_exp) 
print("Total different expression: " + str(triq_s05_s08_CAEEL_diff_exp_tot)) 
print("")
print("Spectronaut S05 vs S08, CAEEL")    
print(spec_s05_s08_CAEEL_diff_exp) 
print("Total different expression: " + str(spec_s05_s08_CAEEL_diff_exp_tot)) 
print("")
print("Triqler S05 vs S08, ARATH")
print(triq_s05_s08_ARATH_diff_exp) 
print("Total different expression: " + str(triq_s05_s08_ARATH_diff_exp_tot)) 
print("")
print("Spectronaut S05 vs S08, ARATH")    
print(spec_s05_s08_ARATH_diff_exp) 
print("Total different expression: " + str(spec_s05_s08_ARATH_diff_exp_tot)) 
print("")





```

    S02 vs S06
    Triqler S02 vs S06, HUMAN
    R01    4470
    R02    4637
    R03    4490
    R04    4507
    R05    4356
    dtype: int64
    Total different expression: 22460
    
    Spectronaut S02 vs S06, HUMAN
    R01    4195
    R02    4372
    R03    4232
    R04    4170
    R05    3996
    dtype: int64
    Total different expression: 20965
    
    Triqler S02 vs S06, CAEEL
    R01    0
    R02    0
    R03    0
    R04    0
    R05    0
    dtype: int64
    Total different expression: 0
    
    Spectronaut S02 vs S06, CAEEL
    R01    0
    R02    0
    R03    0
    R04    0
    R05    0
    dtype: int64
    Total different expression: 0
    
    Triqler S02 vs S06, ARATH
    R01    45
    R02    38
    R03    30
    R04    34
    R05    31
    dtype: int64
    Total different expression: 178
    
    Spectronaut S02 vs S06, ARATH
    R01    323
    R02    286
    R03    275
    R04    264
    R05    260
    dtype: int64
    Total different expression: 1408
    
    S03 vs S04
    Triqler S03 vs S04, HUMAN
    R01    1802
    R02    3201
    R03    1894
    R04    3556
    R05    2797
    dtype: int64
    Total different expression: 13250
    
    Spectronaut S03 vs S04, HUMAN
    R01    2656
    R02    3037
    R03    2499
    R04    3142
    R05    2450
    dtype: int64
    Total different expression: 13784
    
    Triqler S03 vs S04, CAEEL
    R01    0
    R02    0
    R03    0
    R04    0
    R05    0
    dtype: int64
    Total different expression: 0
    
    Spectronaut S03 vs S04, CAEEL
    R01    0
    R02    0
    R03    0
    R04    0
    R05    0
    dtype: int64
    Total different expression: 0
    
    Triqler S03 vs S04, ARATH
    R01     8
    R02    21
    R03    15
    R04    42
    R05    19
    dtype: int64
    Total different expression: 105
    
    Spectronaut S03 vs S04, ARATH
    R01    119
    R02    197
    R03    143
    R04    338
    R05    196
    dtype: int64
    Total different expression: 993
    
    S04 vs S09
    Triqler S04 vs S09, HUMAN
    R01    4086
    R02    2706
    R03    3451
    R04    2796
    R05    3109
    dtype: int64
    Total different expression: 16148
    
    Spectronaut S04 vs S09, HUMAN
    R01    3909
    R02    3175
    R03    4001
    R04    3352
    R05    3427
    dtype: int64
    Total different expression: 17864
    
    Triqler S04 vs S09, CAEEL
    R01    0
    R02    0
    R03    0
    R04    0
    R05    0
    dtype: int64
    Total different expression: 0
    
    Spectronaut S04 vs S09, CAEEL
    R01    0
    R02    0
    R03    0
    R04    0
    R05    0
    dtype: int64
    Total different expression: 0
    
    Triqler S04 vs S09, ARATH
    R01    14
    R02    13
    R03    23
    R04    12
    R05     5
    dtype: int64
    Total different expression: 67
    
    Spectronaut S04 vs S09, ARATH
    R01    197
    R02    208
    R03    246
    R04    168
    R05    138
    dtype: int64
    Total different expression: 957
    
    S05 vs S08
    Triqler S05 vs S08, HUMAN
    R01    3745
    R02    4341
    R03    4193
    R04    4592
    R05    4744
    dtype: int64
    Total different expression: 21615
    
    Spectronaut S05 vs S08, HUMAN
    R01    3809
    R02    4503
    R03    3808
    R04    4448
    R05    4666
    dtype: int64
    Total different expression: 21234
    
    Triqler S05 vs S08, CAEEL
    R01    0
    R02    0
    R03    0
    R04    0
    R05    0
    dtype: int64
    Total different expression: 0
    
    Spectronaut S05 vs S08, CAEEL
    R01    0
    R02    0
    R03    0
    R04    0
    R05    0
    dtype: int64
    Total different expression: 0
    
    Triqler S05 vs S08, ARATH
    R01    19
    R02    59
    R03    25
    R04    12
    R05     9
    dtype: int64
    Total different expression: 124
    
    Spectronaut S05 vs S08, ARATH
    R01    157
    R02    333
    R03    219
    R04    202
    R05    130
    dtype: int64
    Total different expression: 1041
    


We need to make treshold depending on specie.

For HUMAN we want sample to be larger.
For CAEEL we want sample to be smaller.
For ARATH we want sample to be close to 0. 

Triqler seems to get more or similar differentially expressed for HUMAN.
Triqler seems to get less or similar differenatially expressed for ARATH.

which is good... but I seem to be doing something wrong with the CAEEL computations.

I could visualize this as matrix for all samples, where coloring of the matrix indicated which has more differentially expressed.

Think about if we should remove proteins that have not been discovered in different runs from spec...


### 2020-12-18 Todo after friday meeting.

- Check Tenzer data set.
- Download ENSEMBL (Uniprot) data set.
- Download SWISS (Uniprot) data set.
- Check proteoform inference in Matthew's article about iPRG2016.
- Get EncyclopeDIA running on data sets.
- Get Triqler running on data sets.
- Think about what database Roland should use perform experiments for a fair comparison with triqler.
- Make project description more neutral. 
- Change project description from protein quantification to protein summarization (?)

Meeting notes

Project description is too loaded. It needs to be more neutral. 

Problems in benchmarking is not protein inference. We need to remove this part from any Triqler benchmarking. There are two approaches to how to treat proteoforms.

- If any proteoform is prevalent; the protein is assumed to exist (will id. too many proteins).
- If require more evidence for protein for it to be counted as identified (will be more conservative).

Triqler works on the conservative principle. Therefore, we need to have a database with less proteoforms for any comparison to be fair. 

Get encyclopeDIA working, get results and remove protein inference step from encyclopedia and run Triqler from this step.

I need to run the whole thing for my own to know the process. 

TIP on log-formatting: It will be much easier for everybody else to read if I chunk it up to experient scripts, run scripts and write about results and discuss the results in the log. Have the experiment scripts in experiment-folder.

On the FC diff. exp. comparison (2020-12-11 Cont. on diff expression). Still a good idea to do the matrix of which comparison are better for triqler and spectronaut for all cases and run, to get an overview of which methods perform better. But this is not priority at this moment.







### 2020-12-18 article for DIA data
https://www.nature.com/articles/s41467-019-13866-z#Sec16

Spectral library
https://www.ebi.ac.uk/pride/spectrumlibrary

Figure out how to run encyclopeDIA, what is background, library files etc...

File formats commonly used in proteomics. This is good to know.
https://pubmed.ncbi.nlm.nih.gov/22956731/


## 2020-01-06

https://bitbucket.org/searleb/encyclopedia/wiki/FAQs


Q. How can I use EncyclopeDIA in a non-English speaking environment?

Sorry, EncyclopeDIA is not currently internationalized for different languages. Aside from translation issues, EncyclopeDIA also assumes a decimal point separator (common to North America and most of Asia), rather than a decimal comma separator (common to mainland Europe). You can change the default settings for Java to force your computer to operate in this manner by specifying "user.language" and "user.region" to "US". For example, you can start EncyclopeDIA using the command:

java -Xmx12g -jar encyclopedia-0.9.0-executable.jar -Duser.language=en-US -Duser.region=US

Q. How do I run EncyclopeDIA or Walnut at the command line?

EncyclopeDIA can also be used at the command line. For example, to run EncyclopeDIA across all mzMLs in a directory, you can execute the shell command:

for i in directory/to/my/files/*.mzML; do 
    java -Xmx12g -jar encyclopedia-0.9.0-executable.jar -i $i -l library.dlib -f sequences.fasta; 
done

Here, Java is run with 12 GB of RAM with the flag "-Xmx12g". Additional flags are "-i" to specify the input mzML, "-l" to specify the library, and "-f" to specify the FASTA database. You can run the help function to get additional command line options:

java -Xmx12g -jar encyclopedia-0.9.0-executable.jar -h

The "-libexport" function can be used to generate global quantitative results.

java -Xmx12g -jar encyclopedia-0.9.0-executable.jar -libexport -a true -l library.dlib -f sequences.fasta -i directory/to/my/files/ -o output.elib

With the "-a true" flag, this command performs retention time alignment (match-between-runs) and global FDR estimation. After you run the -libexport function, all of the results are filtered to a 1% FDR with Percolator at the peptide (in the .peptides.txt table) and protein level (in the .proteins.txt table). With the "-a false" flag, the -libexport function can be used to generate a chromatogram library as "output.elib".

## 2020-01-10

https://www.biorxiv.org/content/10.1101/044552v2.full.pdf

This website contains good tutorial on how to perform openSWATH procedure. 




### Looking at the Tenzer dataset

Questions:
- What is .wiff.scan files
- What is htrms files

.wiff.scan file seems to be to raw-files that should be converted to .mzml files according to (this)[https://www.researchgate.net/post/What_are_free_tools_to_convert_a_wiff_file_into_an_mzXML_file_in_an_MS_experiment] it should be able to be converted to .mzml with msconvert. 

Some more questions:
- What is important to focus on?
- What data set should I start with?
- What about datasets without proteinId?
- How should we approach this problem?
- Should I use the .raw files?
- What is the library (spectral library)
- What is the background file (background of encyclopeDIA?)
- When should I use PECAN? (One benchmarking paper used normal peakpicking from msconvert, is PECAN not for peak detection?)


Looking into 
Spectronaut_onlyHumanPeptidesDetectedByDIAUmpire_Report_ProtHUMAN.tsv

## 2021-01-13
http://openswath.org/en/latest/docs/docker.html#running-openswath-in-docker

To run from docker: This is the command.

docker run --name osw_tutorial --rm -v ~/:/data -i -t openswath/openswath:latest

How to run pyprophet.

Install pyprophet on python 2 environment. 

anaconda3/envs/py27/bin/pyprophet --help

## 2021-01-14

Have gotten OpenSWATH to work on PASS00779 dataset.

Looking into BiblioSpec for spectral library build (How does this work?)
Looking into TPP Spectrast for spectra library build (Could not get TPP working correctly)
Looking into Mascot, SEQUEST for PSM (They seems to be proprietary)

Looking into the data set: I have choosen HYE124_TTOF6600_32fix data set because they seem to be the smallest data set with least dissimilar proportion between mixtures (65 % HUMAN, 20 % E.Coli, 15 % Yeast). 


Steps for building spectral library
.raw --> convert [MSConvert] to .mzML --> peptide spectral matching and protein identification (Crux-pipeline [Crux Bullseye --> Crux Comet/Tide search --> Crux Percolator]) --> BiblioSpec.

NOTE: files need to be renamed so that they do not have spaces before Crux can be run properly (I got stuck in this for a while).

I am currently running the Crux Bullseye on .mzML data. It seems to take about 2.5-3h for each .mzML file. 

Some Thoughts for meeting tomorrow:

- Tenzer data is big, Bruderer data is even bigger. Steps in pipeline take quite some time. How would be a smart way to work with the data, which data set to chose? Does it even matter?

Does it matter if TTOF6600, TTOF5600+ machine? 64 variable window size for SWATH vs 32 fixed window sized?

Does it matter which database search engine is used for peptide spectrum matches and protein identification (PSM)? 

Skyline can build spectral library (https://skyline.ms/_webdav/home/software/Skyline/%40files/tutorials/MethodEdit-20_1.pdf). But does not support tide-search format. So will use the comet formatting.

When this is done, everything else should work. 

How do i get BlibBuild working.

## 2021-01-15

Meeting with Lukas.

Looking into how to build spectra libraries again. 

How to build spectral library from SPECTRAL LIBRARY GENERATION segment in this tutorial (http://openswath.org/en/latest/docs/tpp.html#id4).

Looking into Trans-Proteomic Pipeline.

Building the Trans-Proteomic Pipeline by following this tutorial (http://tools.proteomecenter.org/wiki/index.php?title=TPP_5.2.0:_Installing_on_Ubuntu_18.04_LTS).

Everything worked until 
```
export PERL_MM_USE_DEFAULT=1
yes | sudo cpan install CGI
sudo cpan install XML::Parser
sudo cpan install FindBin::libs
yes | sudo cpan install JSON


cd /usr/local/tpp/bin
export PERL5LIB=/usr/local/tpp/lib/perl
./test_tpi.pl

(base) ptruong@planck:/usr/local/tpp/bin$ ./test_tpi.pl
Testing CGI.............................ok
Testing CGI::Carp.......................ok
Testing Cwd.............................ok
Testing Data::Dumper....................ok
Testing Digest::MD5.....................ok
Testing DirHandle.......................ok
Testing Fcntl...........................ok
Testing File::Basename..................ok
Testing File::Copy......................ok
Testing File::Path......................ok
Testing File::Spec......................ok
Testing File::Spec::Functions...........ok
Testing File::Spec::Win32...............ok
Testing File::Temp......................ok
Testing FindBin.........................ok
Testing FindBin::libs...................NOT FOUND!  Please check installation.
Testing Getopt::Long....................ok
Testing Getopt::Std.....................ok
Testing HTML::Entities..................ok
Testing IO::Compress::Zip...............ok
Testing JSON............................ok
Testing LWP::Simple.....................ok
Testing Pod::Usage......................ok
Testing POSIX...........................ok
Testing Test::More......................ok
Testing Tie::File.......................ok
Testing TPP.............................ok
Testing tpplib_perl.....................ok
Testing TPP::StatUtilities..............ok
Testing Win32...........................skipped
Testing Win32::GUI......................skipped
Testing Win32::GuiTest..................skipped
Testing Win32::Service..................skipped
Testing Win32::SysTray..................skipped
Testing XML::Parser.....................ok
29 modules installed, 5 skipped, 1 NOT installed


We don't have FindBin::libs. I will need to check how to install this tonight.

### 2020-01-18

sudo cpan install FindBin::libs

Installed FindBin::libs

Now installation of TPP should be done.

In http://openswath.org/en/latest/docs/tpp.html.

Following line:

Please follow the tutorial until the generation of SpectraST spectral libraries. If you are using DIA data, follow the DIA-Umpire tutorial to generate pseudo-spectra first, which can then be processed using the TPP.

Does this mean that we can generate spectral library from DIA data as well... I should check this.

According to [Yang et al. 2020](https://www.nature.com/articles/s41467-019-13866-z) spectral library can be generated from DIA-data. SHould check this laters.

... Some .md notes lost because forgot to save .md file and closed terminal.

### 2020-01-19.

... Some .md notes lost because forgot to save .md file and closed terminal.

Have been trying to get spectraST. I can't figure out which file to use from crux-output, so have tried to run comet from tpp.

The process for generating spectral library...

Comet works but on HeLa_007.mzML pep.xml output I get the following error:

(base) ptruong@planck:~/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007$ PeptideProphetParser Hela_007_Rep1.pep.xml 
 (Comet)
init with Comet Trypsin 
MS Instrument info: Manufacturer: UNKNOWN, Model: UNKNOWN, Ionization: UNKNOWN, Analyzer: UNKNOWN, Detector: UNKNOWN

INFO: Processing standard MixtureModel ... 
 PeptideProphet  (TPP v5.2.0 Flammagenitus, Build 201902051127-7887 (Linux-x86_64)) AKeller@ISB
 read in 8 1+, 26899 2+, 24801 3+, 0 4+, 0 5+, 0 6+, and 0 7+ spectra.
Initialising statistical models ...
Iterations: .........10.........20.........
WARNING: Mixture model quality test failed for charge (1+).
model complete after 30 iterations


(base) ptruong@planck:~/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007$ InterProphetParser Hela_007_Rep1.pep.xml iProphet.pep.xml
Running NSS NRS NSE NSI NSM NSP FPKM Model EM:
Computing NSS values ... 
. done
Computing NRS values ... 
.........10%.........20%.........30%.........40%.........50%.........60%.........70%.........80%.........90%.........100% done
Computing NSE values ... 
.........10%.........20%.........30%.........40%.........50%.........60%.........70%.........80%.........90%.........100% done
Computing NSI values ... 
.........10%.........20%.........30%.........40%.........50%.........60%.........70%.........80%.........90%.........100% done
Computing NSM values ... 
.........10%.........20%.........30%.........40%.........50%.........60%.........70%.........80%.........90%.........100% done
Computing NSP values ... 
Creating 1 threads 
Wait for threads to finish ...
0--------------------------------------------------50------------------------------------------------100%
.................................................................................................... done
FPKM values are unavailable ... 
Iterations: .........10.......done

iProphet processed .mzML for probability assignment performed as recommended.


(base) ptruong@planck:~/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007$ spectrast -cP iProphet.pep.xml 
SpectraST started at Wed Jan 20 01:40:54 2021.
Processing "iProphet.pep.xml"...500...1000...1500...2000...2500...3000...3500...4000...4500...5000...5500...6000...6500...7000...7500...8000...8500...9000...9500...10000...10500...11000...11500...12000...12500...13000...13500...14000...14500...15000...15500...16000...16500...17000...17500...18000...18500...19000...19500...20000...20500...21000...21500...22000...22500...23000...DONE!
Importing all spectra with P>=0 ...10%...20%...30%...40%...50%...60%...70%...80%...90%...DONE!

Library file (BINARY) "iProphet.splib" created.
Library file (TEXT) "iProphet.sptxt" created.
M/Z Index file "iProphet.spidx" created.
Peptide Index file "iProphet.pepidx" created.

Total number of spectra in library: 0
Total number of distinct peptide ions in library: 0
Total number of distinct stripped peptides in library: 0

CHARGE            +1: 0 ; +2: 0 ; +3: 0 ; +4: 0 ; +5: 0 ; >+5: 0 ; Unk: 0
TERMINI           Tryptic: 0 ; Semi-tryptic: 0 ; Non-tryptic: 0
PROBABILITY       >0.9999: 0 ; 0.999-0.9999: 0 ; 0.99-0.999: 0 ; 0.9-0.99: 0 ; <0.9: 0
NREPS             20+: 0 ; 10-19: 0 ; 4-9: 0 ; 2-3: 0 ; 1: 0
MODIFICATIONS     None

Total Run Time = 48 seconds.
SpectraST finished at Wed Jan 20 01:41:42 2021 with 23144 error(s):
...

spectrast performed on the iProphet output... however 0 spectra ssem to have been generated. The output file is empty.

What to do??

I have tried rerunning everything many times.. without results. 

I don't know how would be the smartest way to generate spectral lib from my current data set... I'm stuck this is not good. 

Just noticed this snippet...

...

PEPXML IMPORT: Cannot find MS2+ scan #71199 in file "/home/ptruong/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output/comet.mzXML". Scan not imported.
...

Perhaps the error occurs because I have not converted my .mzML to mzXML, so the spectrast cannot search?

Converting .mzML to .mzXML worked.


(base) ptruong@planck:~/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output$ spectrast -cP0.9 comet.target.pep.xml 
SpectraST started at Wed Jan 20 02:48:55 2021.
Processing "comet.target.pep.xml"...500...1000...1500...2000...2500...3000...3500...4000...4500...5000...5500...6000...6500...7000...7500...8000...8500...9000...9500...10000...10500...11000...11500...12000...12500...13000...13500...14000...14500...15000...15500...16000...16500...DONE!
Importing all spectra with P>=0.9 ...10%...20%...30%...40%...50%...60%...70%...80%...90%...DONE!

Library file (BINARY) "comet.target.splib" created.
Library file (TEXT) "comet.target.sptxt" created.
M/Z Index file "comet.target.spidx" created.
Peptide Index file "comet.target.pepidx" created.

Total number of spectra in library: 8141
Total number of distinct peptide ions in library: 7491
Total number of distinct stripped peptides in library: 7435

CHARGE            +1: 0 ; +2: 6122 ; +3: 2019 ; +4: 0 ; +5: 0 ; >+5: 0 ; Unk: 0
TERMINI           Tryptic: 8140 ; Semi-tryptic: 1 ; Non-tryptic: 0
PROBABILITY       >0.9999: 4670 ; 0.999-0.9999: 1068 ; 0.99-0.999: 1068 ; 0.9-0.99: 1333 ; <0.9: 2
NREPS             20+: 0 ; 10-19: 0 ; 4-9: 0 ; 2-3: 0 ; 1: 8141
MODIFICATIONS     C,Carbamidomethyl: 1026

Total Run Time = 380 seconds.
SpectraST finished at Wed Jan 20 02:55:15 2021 with 8551 error(s):
PEPXML IMPORT: Cannot find MS2+ scan #156 in file "/home/ptruong/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output/comet.mzXML". Scan not imported.
PEPXML IMPORT: Cannot find MS2+ scan #185 in file "/home/ptruong/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output/comet.mzXML". Scan not imported.
PEPXML IMPORT: Cannot find MS2+ scan #263 in file "/home/ptruong/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output/comet.mzXML". Scan not imported.
...

The missed PEPXML IMPORT: are mslevel=1 scans in the .mzXML file.

### 2021-01-20 A lot of time spent tryin to get spectral lib file conversion.

Fixed all steps for the other two mzML steps.

How do we convert .splib to TraML, tsv, pqp format?

Spent a couple of hours (~3hrs) on trying to looking into ConvertTSVToTraML to convert .splib to .TraML as specified in http://openswath.org/en/latest/docs/ipf_legacy.html. It turns out that ConvertTSVToTraML has deprecated and is removed since openms2.2 (https://www.openms.de/openms220/). The current version is openms2.6. 

TargetFileConverter should be used instead to convert.

The process is following..

# This will generate the file db_assays.mrm
spectrast -cNdb_assays -cICID-QTOF -cM db_consensus.splib

TargetedFileConverter -in db_assays.mrm -out db_assays.TraML

OpenSwathWorkflow -in comet.target.mzML -tr db_assays.TraML -sort_swath_maps -batchSize 1000 -out_tsv osw_output.tsv

The above command worked; two thoughts - 1) iRT normalization is this needed (I should read the Tenzer paper to determine this and old notes from what is discussed with Lukas), 2) I am not using swath_windows_file at this moment. Is this needed?

### 2021-01-21 

Trying to get the whole pipeline working. The followning is the output.

root@f2d0dc8baf00:/data/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output# OpenSwathWorkflow -in comet.target.mzML -tr db_assays.TraML -sort_swath_maps -batchSize 1000 -out_tsv osw_output.tsv
Since neither rt_norm nor tr_irt is set, OpenSWATH will not use RT-transformation (rather a null transformation will be applied)
Progress of 'Load TraML file':
-- done [took 1.99 s (CPU), 2.05 s (Wall)] -- 
Loaded 259 proteins, 318 compounds with 36807 transitions.
Loading mzML file comet.target.mzML using readoptions normal
Progress of 'Loading metadata file comet.target.mzML':
Will analyze the metadata first to determine the number of SWATH windows and the window sizes.
Determined there to be 34525 SWATH windows and in total 2212 MS1 spectra
Determined there to be 34525 SWATH windows and in total 2212 MS1 spectra
-- done [took 22.85 s (CPU), 41.60 s (Wall)] -- 
Progress of 'Loading data file comet.target.mzML':
Killed

root@f2d0dc8baf00:/data/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.ukroot@f2d0dc8baf00:/data/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output# OpenSwathWorkflow -in comet.target.mzML -tr db_assays.TraML -sort_swath_maps -batchSize 1000 -out_tsv osw_output.tsv
Since neither rt_norm nor tr_irt is set, OpenSWATH will not use RT-transformation (rather a null transformation will be applied)
Progress of 'Load TraML file':
-- done [took 1.90 s (CPU), 1.94 s (Wall)] -- 
Loaded 259 proteins, 318 compounds with 36807 transitions.
Loading mzML file comet.target.mzML using readoptions normal
Progress of 'Loading metadata file comet.target.mzML':
Will analyze the metadata first to determine the number of SWATH windows and the window sizes.
Determined there to be 34525 SWATH windows and in total 2212 MS1 spectra
Determined there to be 34525 SWATH windows and in total 2212 MS1 spectra
-- done [took 24.89 s (CPU), 41.30 s (Wall)] -- 
Progress of 'Loading data file comet.target.mzML':
Read chromatogram while reading SWATH files, did not expect that!

  -- done [took 03:48 m (CPU), 03:48 m (Wall)] -- 
Extraction will overlap between 360.521 and 359.522
This will lead to multiple extraction of the transitions in the overlapping regionwhich will lead to duplicated output. It is very unlikely that you want this.
Please fix this by providing an appropriate extraction file with -swath_windows_file
Extraction windows overlap. Will abort (override with -force)
OpenSwathWorkflow took 04:33 m (wall), 04:16 m (CPU), 10.95 s (system), 04:05 m (user).
root@f2d0dc8baf00:/data/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output# 

It seems that I should be using swath_windows_file. 

I will try the -force arg as well.


root@f2d0dc8baf00:/data/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output# OpenSwathWorkflow -in comet.target.mzML -tr db_assays.TraML -sort_swath_maps -batchSize 1000 -force -out_tsv osw_output.tsv

### 2021-01-22

Another link about running spectrast 
https://www.biorxiv.org/content/10.1101/2020.01.21.914788v2.full.pdf

How does spectral searching work?


How does OpenSWATH work for peptide concentrations?

Today was spent writing about the pipeline in thesis section.

Reading [Griss J. 2015 - Spectral library searching in Proteomics](https://onlinelibrary.wiley.com/doi/full/10.1002/pmic.201500296)

### 2021-01-25

Trying to run .splib --> .mrm --> .TraML file again. I suspect -cI command messed up last spectral library build.

Going through Tenzer paper PXD002952 to check details.

iRT normalization is not needed because same buffer (lösningmedel) is used for all samples and same gradient. I think.. this is found under sample preparation section of the paper.



(base) ptruong@planck:~/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output$ spectrast -cNpercolator.db -cM percolator.target.splib 
SpectraST started at Mon Jan 25 15:15:40 2021.
Creating library from "/home/ptruong/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output/percolator.target.splib" 
Importing ions...500...1000...1500...2000...2500...3000...3500...4000...4500...5000...5500...6000...DONE!

Library file (BINARY) "percolator.db.splib" created.
Library file (TEXT) "percolator.db.sptxt" created.
M/Z Index file "percolator.db.spidx" created.
Peptide Index file "percolator.db.pepidx" created.
MRM Table file "percolator.db.mrm" created.

Total number of spectra in library: 6811
Total number of distinct peptide ions in library: 6375
Total number of distinct stripped peptides in library: 6342

CHARGE            +1: 0 ; +2: 5055 ; +3: 1756 ; +4: 0 ; +5: 0 ; >+5: 0 ; Unk: 0
TERMINI           Tryptic: 6811 ; Semi-tryptic: 0 ; Non-tryptic: 0
PROBABILITY       >0.9999: 109 ; 0.999-0.9999: 789 ; 0.99-0.999: 2448 ; 0.9-0.99: 3464 ; <0.9: 1
NREPS             20+: 0 ; 10-19: 0 ; 4-9: 0 ; 2-3: 0 ; 1: 6811
MODIFICATIONS     C,Carbamidomethyl: 938

Total Run Time = 457 seconds.
SpectraST finished at Mon Jan 25 15:23:17 2021 without error.

(base) ptruong@planck:~/git/bayesMS/data/datasets/PXD002952/ftp.pride.ebi.ac.uk/pride/data/archive/2016/09/PXD002952/convert/dda/mzml/HeLa_007/crux-output$ TargetedFileConverter -in percolator.db.mrm -out percolator.db.TraML
´Warning: SpectraST was not run in RT normalization mode but the converted list was interpreted to have iRT units. Check whether you need to adapt the parameter -algorithm:retentionTimeInterpretation. You can ignore this warning if you used a legacy SpectraST 4.0 file.
Progress of 'conversion to internal data representation':
-- done [took 2.00 s (CPU), 2.01 s (Wall)] -- 
TargetedFileConverter took 06:28 m (wall), 06:28 m (CPU), 3.04 s (system), 06:25 m (user); Peak Memory Usage: 1485 MB.

Converted file to .TraML and .tsv to check the formating.

To find out which input row is used, we check the values of the .tsv from the converted .splib and compare it to the pep.xml used as input to generate the .splib. Since spectrast spectral library creation should just be a tresholding of the pep.xml file.

#### EXPERIMENT ID. IF PEPTIDE-LEVEL(FDR) or PSM-LEVEL(PEP) probababilities are used for spectrast.

We run the following commands:

spectrast -cP<prob> percolator.target.pep.xml
spectrast -cNpercolator.db -cM percolator.target.splib
TargetedFileConverter -in percolator.db.mrm -out percolator.db.tsv

First we run the commands using -cP0.95.

We look at the .tsv file and find a peptide "AAAAAAALQAK". It has the parameters.

percolator_qvalue = 0.00071234
percolator_PEP = 0.00011322
peptideprophet_prob = 0.99988678

1-percolator_qvalue = 0.99928766
1-percolator_PEP = 0.9998867

We run the commands again with treshold 0.9995 and look for "AAAAAAALQAK". If it is there then PSM-level probabilities are used, otherwise peptide-level probabilities are used.

We check the .tsv and find "AAAAAAALQAK", which means PSM-level probabilities are used. Now to double check we find a peptide "AAAEVNQDYGLDPK" which has percolator_PEP = 0.00032544, and therefore 1-percolator_PEP = 0.99967456. 

If we treshold at -cP0.9998, "AAAEVNQDYGLDPK" should be gone from the library .tsv. 

We run the same commands with -cP0.9998 and the .tsv file does not contain the "AAAEVNQDYGLDPK" peptide.

Hence we are using the PEP-probabilities.

#### Generating data to run openSWATH

We run same command as above with -cP0.99.

spectrast -cP0.99 percolator.target.pep.xml
spectrast -cNpercolator.db -cM percolator.target.splib
TargetedFileConverter -in percolator.db.mrm -out percolator.db.tsv
TargetedFileConverter -in percolator.db.mrm -out percolator.db.TraML

### 2021-01-26

Ran openSWATHWorkFlow yesterday... I choose the wrong input (DDA input). I should use the DIA. I will try again and remake.

Also, there should be a file for irt_normalization hroest_DIA_iRT.TraML. I can't find the file in the ProteomeExchange. 


OpenSwathWorkflow -in ../test_HYE124_TTOF6600_32fix_lgillet_I150211_004_test_sample.mzML -tr ecolihumanyeast_concat_mayu_IRR_cons_openswath_32w_fixed_curated_decoy.TraML -out_tsv osw_output.tsv -readOptions cacheWorkingInMemory -batchSize 1000 -min_upper_edge_dist 1 -extra_rt_extraction_window 100 -min_rsq 0.95 -min_coverage 0.6 -rt_extraction_window 600 -mz_extraction_window 30 -threads 6 -ppm

Running this command gives the following error. 

Error: Unable to read file (- due to that error of type Parse Error in: /code/OpenMS/src/openms/source/FORMAT/HANDLERS/XMLHandler.cpp@105-void OpenMS::Internal::XMLHandler::fatalError(OpenMS::Internal::XMLHandler::ActionMode, const OpenMS::String&, OpenMS::UInt, OpenMS::UInt) const)

According to https://github.com/nf-core/mhcquant/issues/91

This is some c++ internal error. And It could be fixed by peak_ms_level 1 or other centroiding algorithm.

I try to use msconvert to filter on "msLevel 1" with the following command:

msconvert test_HYE124_TTOF6600_32fix_lgillet_I150211_004_test_sample.mzML --filter "msLevel 1"

### 2021-01-27

Installed new harddrive at lab computer, using GParted to create partition.

https://askubuntu.com/questions/662229/what-partition-table-does-ubuntu-create-by-default

This guide suggests using gpt partition.

Tutorial for gparted:

https://linuxhint.com/gparted_ubuntu/

ToDo before bedtime:
- convert all .wiff files to .mzml in hdd_14T.
- perform a spectral library run of openMS.
- check the osw_tsv.csv output data.
- check TRIC

Added shared folder for virtualBox and started process for converting all .wiff files for .mzml.




```python

```
