#! /usr/bin/env Rscript
# linking_subtheme_mc_matching.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This scrip creates a visualization showing the relationship
#           between the subtheme labels and multiple-choice questions
#
# Inputs:
#   This script takes 2 arguments
#     - desensitized qualitative data
#     - survey legend that contains sub-theme codes and
#          multiple-choice questions
#
# Outputs:
#   This script has 1 output
#     - png of subtheme mc relationship
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/visualization/linking_subtheme_mc_matching.R input_qual
# input_data_legend output_file
#
# Real example:
# Rscript src/visualization/linking_subtheme_mc_matching.R
#"./data/interim/desensitized_qualitative-data2018.csv"
#"./references/data-dictionaries/survey_mc_legend.csv"
#"./reports/figures/linking_subtheme_mc.png"


# load packages
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
# Version 1.2.1
suppressPackageStartupMessages(library(testthat))
# Version 2.0.0

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_qual <- args[1]
input_data_legend <- args[2]
output_file <- args[3]


# define main function
main <- function(){


  options(readr.num_columns = 0)
  # load qualitative data
  data_qual <- read_csv(input_qual)

  # load sub-theme codes to question matching
  data_label <- read_csv(input_data_legend)

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

  # Unit tests to ensure labels are correctly parsed in
  test1 <- labels %>%
    filter(question == "Q39")

  test_that("Ensure labels have been parsed in correctly", {
    expect_equal(test1$theme, c("102",  "104"))
    expect_equal(nrow(labels), 53)
  })

  # create grid for plot
  x_axis <- rep(1:16, times=6)[1:62]
  y_axis <- rep(1:16, each=16)[1:62]

  # create table with a grid for plotting
  total_subtheme <- data_qual %>%
    select(contains("Code")) %>%
    filter(`Code 1` != 10) %>%
    gather(key="code", value="subtheme") %>%
    drop_na() %>%
    group_by(subtheme) %>%
    summarize(total_comments=n()) %>%
    mutate(x_pos = x_axis) %>%
    mutate(y_pos = y_axis) %>%
    mutate(subtheme = as.character(subtheme)) %>%
    left_join(labels, by=c("subtheme" = "theme")) %>%
    mutate(question = if_else(is.na(question), "no", "at least one"))

  # create plot
  mc_subtheme <- ggplot(data=total_subtheme) +
    geom_point(aes(x=x_pos, y=y_pos, size=total_comments, color=question)) +
    geom_text(aes(x=x_pos, y=y_pos, label=subtheme),hjust=0,
                  vjust=1.6, size=4.2) +
    theme_bw() +
    labs(x="", y="") +
    theme(axis.text.x = element_blank(),
          axis.text.y = element_blank(),
          axis.ticks = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.background = element_blank(),
          axis.line = element_blank(),
          panel.border = element_blank(),
          legend.justification = c("right", "top"),
          legend.title=element_text(size=13),
          legend.text=element_text(size=12))+
    guides(size=guide_legend(override.aes=list(colour="grey"))) +
    scale_colour_manual("Does the subtheme match to \n a multiple-choice question?",
                        values = c("at least one"="#12aab5", "no"="#7C2F5B")) +
    scale_size_continuous("Number of Comments") +
    guides(colour = guide_legend(override.aes = list(size=3.5)))
  mc_subtheme

  # save plot created as an image
  ggsave(output_file,
         plot=mc_subtheme,
         width=14, dpi=500)

}

# call main function
main()
