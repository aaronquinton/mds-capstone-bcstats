#! /usr/bin/env Rscript
# linking_agreement_figure_subtheme.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script takes in the joined data and outputs a grid of
#            32 histogram showing the agreement levels for each subtheme
#
# Inputs:
#   This script takes 1 arguments
#     - joined qualitative and quantitative data
#
# Outputs:
#   This script has 1 output
#     - png of subtheme agreement levels
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/visualization/linking_agreement_figure_subtheme.R input_file
# output_file
#
# Real example:
# Rscript src/visualization/linking_agreement_figure_subtheme.R
#"./data/interim/linking_joined_qual_qaunt.csv"
#"./reports/figures/linking_agreement_subtheme.png"


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

  # add main theme labels to grouped data
  group2 <- grouped_data %>%
    mutate(main_theme = str_sub(`code`, start = 1, end = str_length(`code`)-1),
           Theme = theme_qual$theme[match(`main_theme`, theme_qual$num)])

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

  # shows distribution of agreement for each subtheme
  sub_theme <- ggplot(data=group2) +
    geom_col(aes(x=factor(diff), y=n, fill=Theme)) +
    facet_wrap(~code) +
    labs(x="", y="count", fill="") +
    theme_bw()+
    scale_fill_brewer(type="qual", palette = "Paired") +
    theme(legend.position="bottom",
          axis.text.x = element_text(angle=70, hjust = 1)) +
    guides(fill=guide_legend(nrow=4)) +
    scale_x_discrete(labels=c("0" = "Strong", "1" = "Weak",
                              "2" = "None"))

  # save plot
  ggsave(output_file,
         plot=sub_theme,
         width=10,
         dpi=500)

}

# call main function
main()
