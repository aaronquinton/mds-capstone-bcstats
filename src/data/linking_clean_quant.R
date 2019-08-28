
#! /usr/bin/env Rscript
# linking_clean_quant.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script reads in the raw quantitative data and outputs
#           the data ready to be related to the qualitative data
#
# Inputs:
#   This script takes 2 arguments
#     - raw quantitative data
#     - survey legend that contains sub-theme codes and
#          multiple-choice questions
#
# Outputs:
#   This script has 1 output
#     - csv of clean and wrangled quantitative data
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/data/linking_clean_quant.R input_quant_data input_data_legend
# output_file
#
# Real example:
# Rscript src/data/linking_clean_quant.R
#"./data/processed/tidy_quant_questions.csv"
#"./references/data-dictionaries/survey_mc_legend.csv"
#"./data/interim/linking_cleaned_quant.csv"


# load packages
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
# Version 1.2.1
suppressPackageStartupMessages(library(testthat))
# Version 2.0.0

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file_quant <- args[1]
input_file_labels <- args[2]
output_file <- args[3]


# define main function
main <- function(){
  # load quantitative data
  options(readr.num_columns = 0)
  data_quant <- read_csv(input_file_quant)

  # select the 2018 questions
  quant <- data_quant %>%
    filter(survey_year == 2018) %>%
    select(USERID, dplyr::matches("Q.."))  %>%
    gather(key = "question", value="score", dplyr::matches("Q..")) %>%
    drop_na() %>%
    mutate(
      question = factor(question),
      quan_value = case_when(
        score < 50     ~ -1,
        score == 50    ~  0,
        score > 50     ~  1,
        TRUE           ~ 99
      )
    ) %>%
    select(USERID, question, quan_value)  %>%
    mutate(question = as.character(question))

  # load sub-theme labels matched to multiple-choice questions
  data_label <- read_csv(input_file_labels)

  # create df with sub-theme label and mc question
  labels <- data_label %>%
    filter(survey_year == "2018") %>%
    filter(category == "Raw Survey Question") %>%
    select(new_column_name, subtheme_code) %>%
    mutate(sub_theme = (na_if(subtheme_code, 0))) %>%
    separate(sub_theme,
             sep=", ",
             into = c("theme1", "theme2"),
             fill="right") %>%
    gather(key="theme_name", value="theme", theme1, theme2) %>%
    select(theme, question = new_column_name) %>%
    drop_na(theme) %>%
    arrange(question)

  # join the labels with the quantitative data
  quant_cleaned <- left_join(labels, quant, by=c("question")) %>%
    select(USERID, theme,  quan_value, question) %>%
    mutate(theme = as.numeric(theme))

  # Unit tests to ensure filtering is occurring correctly
  # Code will not write output file if tests don't pass
  person1 = "172541-914038"
  person2 = "173108-219388"
  person3 = "173924-784228"
  person4 = "190199-111388"
  person5 = "180129-727518"

  test1 <- quant %>%
    filter(USERID %in% c(person1, person2, person3, person4, person5))

  test_that("quantitative gather and filtering correctly", {
    expect_equal(nrow(test1), 393)
  })

  test2 <- labels %>%
    filter(question == "Q39")

  test_that("Ensure labels have been parsed in correctly", {
    expect_equal(test2$theme, c("102",  "104"))
    expect_equal(nrow(labels), 53)
  })

  test3 <- quant_cleaned %>%
    filter(USERID %in% c(person1, person2, person3, person4, person5)) %>%
    arrange(USERID)

  test4 <- quant_cleaned %>%
    filter(USERID == person1 & question == "Q01")

  test5 <- quant_cleaned %>%
    filter(USERID == person1 & question == "Q17")

  test6 <- quant_cleaned %>%
    filter(USERID == person1 & question == "Q41")

  test_that("Ensure correct joining of subtheme codes to quant data", {
    expect_equal(nrow(test3), 258)
    expect_equal(test4$theme, 34)
    expect_equal(nrow(test5), 0)
    expect_equal(test6$theme, c(105, 106))
  })
  # if all tests pass, write cleaned data to file
  write_csv(quant_cleaned, output_file)

}

# call main function
main()
