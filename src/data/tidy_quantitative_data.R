#! /usr/bin/env Rscript
# tidy_quantitative_data.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: Tidy's the raw quanititative data into two csv files, one with the
#            scores on the multiple choice questions and engagement model, the
#            second details the demographic and other employee info
#
# Inputs:
#   This script takes 2 arguments
#     - raw quantitative data
#     - survey multiple choice legend
#
# Outputs:
#   This script has 1 output
#     - csv of tidy quantitative data
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/data/tidy_quantitative_data.R  input_quant input_legend
# output_questions
#
# Real example:
# Rscript src/data/tidy_quantitative_data.R
#"./data/raw/WES 2007-2018 LONGITUDINAL DATA_short.sav"
#"./references/data-dictionaries/survey_mc_legend.csv"
#"./data/interim/tidy_quant_questions.csv"


# load packages
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
# Version 1.2.1
suppressWarnings(suppressPackageStartupMessages(library(zoo)))# Version 1.8.4


# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_quant <- args[1]
input_labels <- args[2]
output_questions <- args[3]
#output_demos <- args[4]

# define main function
main <- function(){

###############################################################################
# Read quantitative data from SPSS file and read in legend to help select and #
# rename columns                                                              #
###############################################################################

  # Removes labels from spss file for the multiple choice question data
  df_spss <- foreign::read.spss(file = input_quant,
                                to.data.frame = TRUE,
                                use.value.labels = FALSE) %>%
             sjlabelled::remove_all_labels()



  # the csv used has been manually built to help make sense of all the columns
  # in the spss file
  options(readr.num_columns = 0)
  df_legend <- read_csv(input_labels)


###############################################################################
# Build tidy dataframe with m.c. questions and engagement model: df_questions #
###############################################################################

  # specify columns to select
  col_questions <- df_legend %>%
    filter(category == "Raw Survey Question" |
           sub_category == "Engagement Model" |
           original_column_name == "USERID") %>%
    pull(original_column_name)

  # Rename columns, fix data types, and reorganize data frame. Rows used to be
  # unqiuely identified by USERID, it is now by USERID and survey_year
  df_questions <- df_spss %>%
    select(col_questions) %>%
    gather(-USERID, key = "original_column_name", value = "temp_val") %>%
    left_join(df_legend, by = "original_column_name") %>%
    select(USERID, new_column_name, survey_year, temp_val) %>%
    spread(key = new_column_name, value = temp_val) %>%
    mutate_at(vars(-USERID), as.double)%>%
    select(-contains("Q"), Q01:Q80)


###############################################################################
# Write quantitative data files to csv                                        #
###############################################################################

  write_csv(df_questions, output_questions)

}

# call main function
main()
