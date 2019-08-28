#! /usr/bin/env Rscript
# theme_subtheme_names.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script reads in the codebook and creates a
#           clean mapping of themes to sub-themes descriptions
#
# Inputs:
#   This script takes 1 arguments
#     - excel qualitative data codebook
#
# Outputs:
#   This script has 1 output
#     - csv with theme, sub-theme description and code
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/data/theme_subtheme_names.R input_file output_file
#
# Real example:
# Rscript src/data/theme_subtheme_names.R
#"data/raw/2018 WES Qual Coded - Final Comments and Codes.xlsx"
#"./references/data-dictionaries/theme_subtheme_names.csv"
#


# load packages
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
# Version 1.2.1
library(readxl)
# Version 1.1.0

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]


# define main function
main <- function(){
  # load codebook
  options(readr.num_columns = 0)
  qual_subtheme_labels <- read_excel(input_file, sheet = "Codebook",
                                     range = "B2:C75",
                                     col_names = c("Code", "Description"))


  # create matching between theme number and name
  theme_qual <- tribble(
    ~num, ~theme,                     ~short_name,
    1, "Career & Personal Development", "CPD",
    2, "Compensation & Benefits",       "CB",
    3, "Engagement & Workplace Culture","EWC",
    4, "Executives",                   "Exec",
    5, "Flexible Work Environment",    "FWE",
    6, "Staffing Practices",           "SP",
    7, "Recognition & Empowerment",    "RE",
    8, "Supervisors",                  "Sup",
    9, "Stress & Workload",            "SW",
    10,"Tools, Equipment & Physical Environment", "TEPE",
    11, "Vision, Mission & Goals",     "VMG",
    12, "Other",                        "OTH"
  )

  # create table with theme names, sub-theme names and codes
  data_dict <- qual_subtheme_labels %>%
    filter(`Code` != 99) %>%
    filter(!Description %in% (theme_qual$theme)) %>%
    mutate(theme_num = str_sub(`Code`, start = 1, end = str_length(`Code`)-1),
          Theme = theme_qual$theme[match(`theme_num`, theme_qual$num)],
          Theme = if_else(Code == 99, "", Theme) ,
          Code = as.integer(Code),
          Description = str_replace_all(Description, "_", " ")
    ) %>%
    select(theme = Theme,
           theme_num,
           code = Code,
           subtheme_description = Description)

  # write to file
  write_csv(data_dict, output_file)

}

# call main function
main()
