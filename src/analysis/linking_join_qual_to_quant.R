#! /usr/bin/env Rscript
# linking_join_qual_to_quant.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script takes in the cleaned qualitative data and
#           cleaned quantitative data and joins them and outputs
#           the joined data and then takes in the desensitized comments
#           and adds the comments, theme and subtheme names to the data
#
# Inputs:
#   This script takes 4 arguments
#     - cleaned qualitative data
#     - cleaned quantitative data
#     - desensitized qualitative data
#     - theme sub-theme names
#
# Outputs:
#   This script has 1 output
#     - csv of joined qualitative and quantitative data
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/analysis/linking_join_qual_to_quant.R input_qual input_quant
# output_joined
#
# Real example:
# Rscript src/analysis/linking_join_qual_to_quant.R
#"./data/interim/linking_cleaned_qual.csv"
#"./data/interim/linking_cleaned_quant.csv"
#"./data/interim/desensitized_qualitative-data2018.csv"
#"./references/data-dictionaries/theme_subtheme_names.csv"
#"./data/interim/linking_joined_qual_quant.csv"
#

# load packages
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
# Version 1.2.1
suppressPackageStartupMessages(library(testthat))
 # Version 2.0.0

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_qual <- args[1]
input_quant <- args[2]
input_comments <- args[3]
input_legend <- args[4]
output_file <- args[5]


# define main function
main <- function(){
  # read in cleaned data
  options(readr.num_columns = 0)
  qual <- read_csv(input_qual)
  quant <- read_csv(input_quant)

  # combine qualitative and quantitative dfs
  joined_data <- left_join(qual, quant, by=c("USERID", "code"="theme")) %>%
    drop_na(quan_value) %>%
    mutate(diff = quan_value - qual_value)

  # load theme and subtheme names
  legend <- read_csv(input_legend)

  # load comments to add to joined data
  input_comments <- "./data/interim/desensitized_qualitative-data2018.csv"
  comments <- read_csv(input_comments) %>%
    select(USERID = `_telkey`, `2018 Comment`)

  # add theme names and comments to joined data
  joined_data <- joined_data %>%
    mutate(main_theme = str_sub(`code`, start = 1, end = str_length(`code`)-1),
           theme = legend$theme[match(`main_theme`, legend$theme_num)],
           subtheme_description = legend$subtheme_description[match(`code`,
                                                              legend$code)]
           ) %>%
    left_join(comments, by="USERID") %>%
    select(USERID, code, qual_value, quan_value, question,
           diff, text=`2018 Comment`, theme, subtheme_description)

  # Unit Test to confirm filtering is working correctly
  person1 = "172541-914038"  # code 92 = 1
  person3 = "173924-784228"  # code 93 appear twice = 2
  person5 = "180129-727518"  # code 105 & 93 (but only once) = 2

  test1 <- joined_data %>%
    filter(USERID %in% c(person1, person3, person5)) %>%
    arrange(USERID)

  test_that("qual ad quant data have been properly joined", {
    expect_equal(nrow(test1), 5)
  })
  # if all tests pass, write cleaned data to file
  write_csv(joined_data, output_file)

}

# call main function
main()
