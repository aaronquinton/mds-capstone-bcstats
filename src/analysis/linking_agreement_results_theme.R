#! /usr/bin/env Rscript
# linking_agreement_results_theme.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script takes in the joined qualitative and quantitative data
#           and outputs the theme agreement results
#
# Inputs:
#   This script takes 1 arguments
#     - joined qualitative and quantitative data
#
# Outputs:
#   This script has 1 output
#     - csv of the theme agreement results
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/analysis/linking_agreement_results_theme.R input_file output_file
#
# Real example:
# Rscript src/analysis/linking_agreement_results_theme.R
#"./data/interim/linking_joined_qual_quant.csv"
#"./data/processed/linking_agreement_theme.csv"


# load packages
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
# Version 1.2.1
suppressPackageStartupMessages(library(testthat)) # Version 2.0.0

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]


# define main function
main <- function(){

  options(readr.num_columns = 0)
  # loaded joined data
  joined_data <- read_csv(input_file)

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

  grouped_data <- joined_data %>%
    group_by(USERID, code) %>%
    summarize(diff = min(diff)) %>%
    group_by(code, diff) %>%
    summarize(n=n()) %>%
    mutate(main_theme = str_sub(`code`, start = 1, end = str_length(`code`)-1),
           Theme = theme_qual$theme[match(`main_theme`, theme_qual$num)])

  counts_theme <- grouped_data %>%
    ungroup() %>%
    select(Theme, diff, n) %>%
    group_by(Theme) %>%
    summarize(n = sum(n))

  table_results_theme <- grouped_data %>%
    ungroup() %>%
    select(Theme, diff, n) %>%
    group_by(Theme, diff) %>%
    summarize(n = sum(n)) %>%
    mutate(perc = round(n/sum(n)*100,2)) %>%
    select(Theme, diff, perc) %>%
    spread(diff, perc) %>%
    ungroup() %>%
    mutate(counts = counts_theme$n[match(`Theme`, counts_theme$Theme)]) %>%
    select(Theme,
           "Total Number" = counts,
           "Strong Agreement (%)" = "0",
           "Weak Agreement (%)" = "1",
           "No Agreement (%)" = "2")


  test1 <- table_results_theme %>%
    filter(`Theme` == "Career & Personal Development")

  test_that("Check proportions are correct", {
    expect_equal(test1$`Total Number`, 1807)
    expect_equal(test1$`Strong Agreement (%)`, 47.87)
    expect_equal(test1$`Weak Agreement (%)`, 23.80)
    expect_equal(test1$`No Agreement (%)`, 28.33)
  })

  # write results files if all tests pass
  write_csv(table_results_theme, output_file)

}

# call main function
main()
