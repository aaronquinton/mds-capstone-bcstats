#! /usr/bin/env Rscript
# linking_agreement_results_subtheme.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script takes in the joined qualitative and quantitative data
#           and outputs the subtheme agreement results
#
# Inputs:
#   This script takes 1 arguments
#     - joined qualitative and quantitative data
#
# Outputs:
#   This script has 1 output
#     - csv of the subtheme agreement results
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/analysis/linking_agreement_results_subtheme.R input_file
# output_file
#
# Real example:
# Rscript src/analysis/linking_agreement_results_subtheme.R
#"./data/interim/linking_joined_qual_quant.csv"
#"./data/processed/linking_agreement_subtheme.csv"


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

  # group data by subtheme
  # changed the "loss penalty" it now takes the minimum value
  grouped_data <- joined_data %>%
    group_by(USERID, code) %>%
    summarize(diff = min(diff)) %>%
    group_by(code, diff) %>%
    summarize(n=n())

  # create overall counts for each group
  counts <- joined_data %>%
    group_by(USERID, code) %>%
    summarize(diff = min(diff)) %>%
    group_by(code) %>%
    summarize(n = n())

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

  # create summary table for display
  table_results_subtheme <- grouped_data %>%
    mutate(perc = round(n/sum(n)*100,2)) %>%
    select(code, diff, perc) %>%
    spread(diff, perc) %>%
    ungroup() %>%
    mutate(counts = counts$n[match(`code`, counts$code)],
           main_theme = str_sub(`code`, start = 1, end = str_length(`code`)-1),
           Theme = theme_qual$theme[match(`main_theme`, theme_qual$num)],
           code = as.character(`code`)) %>%
    select(Theme,
           "Sub-theme" = code,
           "Total Number" = counts,
           "Strong Agreement (%)" = "0",
           "Weak Agreement (%)" = "1",
           "No Agreement (%)" = "2")

  # Unit tests to ensure filtering is occurring correctly
  # Code will not write output file if tests don't pass
  person1 = "172541-914038"
  person2 = "173108-219388"
  person3 = "173924-784228"
  person4 = "190199-111388"
  person5 = "180129-727518"

  test1 <- joined_data %>%
    filter(USERID %in% c(person1, person2, person3, person4, person5)) %>%
    group_by(USERID, code) %>%
    summarize(diff = min(diff)) %>%
    group_by(code, diff) %>%
    summarize(n=n())

  test_that("Check loss function is taking min for each subtheme per person", {
    expect_equal(nrow(test1), 4)
    expect_equal(sum(test1$n), 4)
  })

  test2 <- joined_data %>%
    filter(USERID %in% c(person1, person2, person3, person4, person5)) %>%
    group_by(USERID, code) %>%
    summarize(diff = min(diff)) %>%
    group_by(code) %>%
    summarize(n = n())

  test_that("Check loss function is taking minimum for counts", {
    expect_equal(nrow(test2), 3)
    expect_equal(sum(test2$n), 4)
  })

  test3 <- table_results_subtheme %>%
    filter(`Sub-theme` == 12)

  test_that("Check proportions are correct", {
    expect_equal(test3$`Total Number`, 103)
    expect_equal(test3$`Strong Agreement (%)`, 50.49)
    expect_equal(test3$`Weak Agreement (%)`, 12.62)
    expect_equal(test3$`No Agreement (%)`, 36.89)
  })

  # write results files if all tests pass
  write_csv(table_results_subtheme, output_file)

}

# call main function
main()
