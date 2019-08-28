#! /usr/bin/env Rscript
# linking_inter_rater_agreement.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script takes each of the raters matching and
#           calculates the percent agreement between each rater
#           and outputs a table with the results
#
# Inputs:
#   This script takes 1 arguments
#     - file containing all 3 raters matches
#
# Outputs:
#   This script has 1 output
#     - csv containing percent agreement values for each pair
#        and all together
#
# Usage:
# Run from the project root
#
# General example:
# Rscript src/analysis/linking_inter_rater_agreement.R input_file output_file
#
# Real example:
# Rscript src/analysis/linking_inter_rater_agreement.R
#"./references/data-dictionaries/survey_mc_legend_inter-rater.csv"
#"./data/processed/linking_inter_rater_agreement.csv"


# load packages
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
# Version 1.2.1

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]

# define main function
main <- function(){
  options(readr.num_columns = 0)
  # load raters sub-theme choices for inter-rater comparison
  data_legend <- read_csv(input_file)

  # percent agreement for person 1 vs person 2
  person_1_2 <- data_legend[,4:5] %>%
    mutate(new = person2 == person1) %>%
    drop_na(new) %>%
    summarize(value =sum(new)/length(new))

  # percent agreement for person 3 vs person 2
  person_2_3 <- data_legend[,3:4] %>%
    mutate(new = person2 == person3) %>%
    drop_na(new) %>%
    summarize(value =sum(new)/length(new))

  # percent agreement for person 1 and person 3
  df <- tibble("person3"=data_legend$person3, "person1"=data_legend$person1)
  person_1_3 <- df %>%
    mutate(new = person1 == person3) %>%
    drop_na(new) %>%
    summarize(value =sum(new)/length(new))

  # percent agreement between all 3 raters
  all <- data_legend[, 3:5] %>%
    mutate(p23 = person3 == person2) %>%
    mutate(p13 = person3 == person1) %>%
    mutate(all_agree = (p23 == TRUE & p13 == TRUE)) %>%
    drop_na(all_agree) %>%
    summarise(value = sum(all_agree)/length(all_agree))

  # create df for results
  table_inter_rater <- tibble("Raters" = c("Person 1 and Person 2",
                                           "Person 1 and Person 3",
                                           "Person 2 and Person 3",
                                           "All"),
                              "Percent Agreement" = c(person_1_2$value,
                                                      person_1_3$value,
                                                      person_2_3$value,
                                                      all$value)) %>%
    mutate(`Percent Agreement` = round(`Percent Agreement`, 2))

  # write results to csv
  write_csv(table_inter_rater, output_file)

}

# call main function
main()
