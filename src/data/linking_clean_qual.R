#! /usr/bin/env Rscript
# linking_clean_qual.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script reads in the desensitized qualitative data and outputs
#           the data ready to be related to the quantitative data
#
# Inputs:
#   This script takes 1 arguments
#     - desensitized qualitative data
#
# Outputs:
#   This script has 1 output
#     - csv of clean and wrangled qualitative data
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/data/linking_clean_qual.R input_file output_file
#
# Real example:
# Rscript src/data/linking_clean_qual.R "./data/interim/desensitized_qualitative
#-data2018.csv" "./data/interim/linking_cleaned_qual.csv"
#


# load packages
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
# Version 1.2.1
suppressPackageStartupMessages(library(testthat))
# Version 2.0.0

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]


# define main function
main <- function(){
  # load qualitative data
  options(readr.num_columns = 0)
  data_qual <- read_csv(input_file)

  # subset required columns, rename and filter out people who only had positive
  #comments
  qual <- data_qual %>%
    select(`_telkey`, `Code 1`, `Code 2`, `Code 3`, `Code 4`, `Code 5`) %>%
    rename(USERID = `_telkey`,
           code1 = `Code 1`,
           code2 = `Code 2`,
           code3 = `Code 3`,
           code4 = `Code 4`,
           code5 = `Code 5`)

  # re-organize data into tidy form
  qual <- gather(qual, key= "code_num", value="code", code1, code2, code3,
                    code4, code5)

  # remove other theme and unrelated comments, create negative rating, and
  # add main themes label from sub-theme code
  qual_cleaned <- qual %>%
    drop_na(code) %>%
    filter(code != 99) %>%
    filter(code != 121) %>%
    filter(code != 123) %>%
    filter(code != 122) %>%
    mutate(qual_value = -1) %>%
    select(USERID, code, qual_value)

  # Unit Test to confirm filtering is working correctly
  person1 = "172541-914038"  # 4 separate codes, all should appear = 4
  person2 = "173108-219388"  # only has code 122, should NOT appear = 0
  person3 = "173924-784228"  # has code 122 and 93, only code 93 should appear=1
  person4 = "190199-111388"  # only has comment 99, should NOT appear =0
  person5 = "180129-727518"  # has 4 codes, one being 123, should count of = 3

  test1 <- qual_cleaned %>%
    filter(USERID %in% c(person1, person2, person3, person4, person5)) %>%
    arrange(USERID)

  test_that("qualitative has been properly filtered", {
    expect_equal(nrow(test1), 8)
  })
  # if all tests pass, write cleaned data to file
  write_csv(qual_cleaned, output_file)

}

# call main function
main()
