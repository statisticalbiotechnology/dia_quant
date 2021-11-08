library(SWATH2stats)
library(MSnbase)
library(msqrobsum)

#setwd("/hdd_14T/data/PXD002952/20210614_dataset/diaumpire/msfragger/diann")
setwd("/hdd_14T/data/PXD002952/20210614_dataset/diaumpire_spectral_lib_20210706/MSFragger_20210707/diann_20210811")

expr_path <- "expr_0.01.csv"
fd_path <- "fd_0.01.csv"
pd_path <- "pd_0.01.csv"

exprs_col = grepEcols(expr_path, '00',split = '\t')

set = readMSnSet2(expr_path ,ecol = exprs_col,fnames = 'peptide'
                  , sep = '\t',stringsAsFactors = FALSE)

suppressPackageStartupMessages(library(tidyverse))

expr <- read.csv2("expr_0.01.csv", sep = "\t", row.names = 1)
fd <- read.csv("fd_0.01.csv", sep = "\t", row.names = 1)
pd <- read.csv("pd_0.01.csv", sep = "\t", row.names = 1)
fData(set) = fd
pData(set) = pd
exprs(set) 

exprs(set)[0 == (exprs(set))] <- NA
set <- set[!fData(set)$decoy]
set_log = log(set, base = 2)
set = normalize(set, 'vsn') #vsn normalized values are on log-scale



formulas =  c(expression ~ (1|condition) + (1|sample) + (1|feature)
              , expression ~ (1|condition))

msqrob_result <- msqrobsum(data = set, formulas, contrasts = 'condition', mode = 'msqrobsum'
                           ## group by folowing variables,
                           ## they will also be retained in output
                           , group_vars = c('protein','human','yeas8','ecoli'))


contrasts = msqrob_result %>% select(proteins,human,ecoli,yeas8,contrasts) %>% unnest
protein_sums = msqrob_result %>% select(proteins, human, ecoli, yeas8, data_summarized) %>% unnest

write.table(contrasts, "msqrobsum_result_20211105_filtered_before.csv", sep = "\t", row.names = FALSE)
write.table(protein_sums, "msqrobsum_protein_sum_20211105_filtered_before.csv", sep = "\t", row.names=FALSE)

