#! /usr/bin/env Rscript
# linking_agreement_figure_theme.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script takes in the joined data and outputs a bar plot
#            showing the agreement levels for each theme
#
# Inputs:
#   This script takes 1 arguments
#     - joined qualitative and quantitative data
#
# Outputs:
#   This script has 1 output
#     - png of theme agreement levels
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/visualization/linking_agreement_figure_theme.R input_file
# output_file
#
# Real example:
# Rscript src/visualization/linking_agreement_figure_theme.R
#"./data/interim/linking_joined_qual_quant.csv"
#"reports/figures/linking_agreement_theme.png"


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

  options(readr.num_columns = 0)
  # loaded joined data
  joined_data <- read_csv(input_file)


  # group data for plotting and tables
  # changed the "loss penalty" it now takes the minimum value
  grouped_data <- joined_data %>%
    group_by(USERID, code) %>%
    summarize(diff = min(diff)) %>%
    group_by(code, diff) %>%
    summarize(n=n())

  # dictionary for theme names
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

  # group data by main themes
  general_theme <- grouped_data %>%
    mutate(main_theme = str_sub(`code`, start = 1, end = str_length(`code`)-1),
           Theme = theme_qual$theme[match(`main_theme`, theme_qual$num)]) %>%
    ungroup() %>%
    select(Theme, diff, n) %>%
    group_by(Theme, diff) %>%
    summarize(counter = sum(n)) %>%
    mutate(short_name = theme_qual$short_name[match(`Theme`,
                                              theme_qual$theme)])

  # plot of proportions of agreement by theme
  theme <- ggplot(data=general_theme) +
    geom_bar(aes(x=factor(short_name,
                          levels = c("CB", "SP", "Exec", "TEPE", "SW",
                                     "CPD", "Sup", "RE", "VMG", "EWC")),
                 y=counter,
                 fill=factor(diff)),
             stat = "identity",
             position = "fill") +
    labs(fill="Level of Agreement", x="", y="") +
    theme_bw() +
    theme(plot.title = element_text(hjust = 0.5),
          axis.text=element_text(size=13),
          legend.title=element_text(size=14),
          legend.text=element_text(size=13)) +
    scale_fill_manual(values = c("#12aab5", "#7C2F5B", "#2F5B7C"),
                      labels=c("0" = "Strong",
                               "1" = "Weak",
                               "2" = "None"))

  # Unit tests to ensure filtering is occurring correctly
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
  # save figure if tests pass
  ggsave(output_file, plot=theme, dpi=550, width=14, height=4.5)

}

# call main function
main()
