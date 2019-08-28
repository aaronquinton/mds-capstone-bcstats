Linking Qualitative to Quantitative Detailed Methodology
================
Aaron Quinton, Ayla Pearson, Fan Nie
June 2019

Usage
=====

This report gives more detail to the methodology for linking the qualitative to quantitative data sets due to the length restriction of the final report. This document also serves as a single output of the MakefileLinking.

Introduction
============

Quantitative studies generate data in numerical form that can be analyzed and expressed by statistics while qualitative studies often generate non-numerical data that is more descriptive. Generally, these forms of data are analyzed separately due to their different forms. We plan to use mixed method research which finds value in integrating qualitative and quantitative data sets to help identify specific areas in the qualitative data set that are not as well represented in the quantitative data set.

Method
======

### Creating link between sub-theme labels

The first task was to create a link between the sub-theme labels used to code the comments and the multiple-choice questions. To do this each team member independently and separately matched the 80 multiple-choice questions to the sub-theme labels. For each potential match it was allowed to have no match, single match or multiple matches. The team members did not agree in every scenario so to determine the correct matching it was chosen that the majority would rule, so if two raters had the same match it would be chosen. For matches that all three team members disagreed upon they were discussed as a group and all team members had to agree on the match before moving forward. It was chosen that any matches that were hard to agree upon they would be left blank because this meant the relationship between the multiple-choice questions and sub-theme label was not as clear.

### Cleaning and Wrangling the Data

For the qualitative data the comments relating to positive comments were removed because they do not correspond to a specific topic but are generally positive. This means it was not possible to match the comments with positive sub-theme labels to specific multiple-choice questions. Once all positive comments were removed it was assumed that all remaining comments had a negative sentiment.

The quantitative data had to be binned into positive, neutral and negative sentiment.

![](../reports/figures/img_mc_numeric_to_sentiment_150.png)

### Determining the Agreement Level Linking

Once both data set were cleaned and in a similar format they were joined and the level of agreement between the qualitative and quantitative sentiment was calculated.

| Qualitative Sentiment | Quantitative Sentiment | Level of Agreement |
|-----------------------|------------------------|--------------------|
| Negative              | Negative               | Strong             |
| Negative              | Neutral                | Weak               |
| Negative              | Positive               | None               |

To obtain the counts for the level of agreement for each sub-theme the scoring function was chosen to be more liberal by only counting the highest agreement level for the sub-theme per person. This was done because sub-theme label and multiple-choice questions could have multiple matches. To find the agreement levels for the theme, the sub-theme agreement levels were generalized to the theme level.

![](../reports/figures/img_scoring_fn.png)

Results
=======

The key findings are discussed in the final report.

![](../reports/figures/linking_subtheme_mc.png)

<br>

<table>
<thead>
<tr>
<th style="text-align:left;">
Raters
</th>
<th style="text-align:right;">
Percent Agreement
</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left;">
Person 1 and Person 2
</td>
<td style="text-align:right;">
0.80
</td>
</tr>
<tr>
<td style="text-align:left;">
Person 1 and Person 3
</td>
<td style="text-align:right;">
0.58
</td>
</tr>
<tr>
<td style="text-align:left;">
Person 2 and Person 3
</td>
<td style="text-align:right;">
0.62
</td>
</tr>
<tr>
<td style="text-align:left;">
All
</td>
<td style="text-align:right;">
0.48
</td>
</tr>
</tbody>
</table>
<br><br><br>

#### Sub-theme Results

![](../reports/figures/linking_agreement_subtheme.png)

<br>

<table>
<thead>
<tr>
<th style="text-align:left;">
Theme
</th>
<th style="text-align:right;">
Sub-theme
</th>
<th style="text-align:right;">
Total Number
</th>
<th style="text-align:right;">
Strong Agreement (%)
</th>
<th style="text-align:right;">
Weak Agreement (%)
</th>
<th style="text-align:right;">
No Agreement (%)
</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left;">
Compensation & Benefits
</td>
<td style="text-align:right;">
24
</td>
<td style="text-align:right;">
1554
</td>
<td style="text-align:right;">
87.45
</td>
<td style="text-align:right;">
7.98
</td>
<td style="text-align:right;">
4.57
</td>
</tr>
<tr>
<td style="text-align:left;">
Compensation & Benefits
</td>
<td style="text-align:right;">
21
</td>
<td style="text-align:right;">
146
</td>
<td style="text-align:right;">
86.99
</td>
<td style="text-align:right;">
9.59
</td>
<td style="text-align:right;">
3.42
</td>
</tr>
<tr>
<td style="text-align:left;">
Compensation & Benefits
</td>
<td style="text-align:right;">
23
</td>
<td style="text-align:right;">
541
</td>
<td style="text-align:right;">
76.71
</td>
<td style="text-align:right;">
13.12
</td>
<td style="text-align:right;">
10.17
</td>
</tr>
<tr>
<td style="text-align:left;">
Stress & Workload
</td>
<td style="text-align:right;">
93
</td>
<td style="text-align:right;">
929
</td>
<td style="text-align:right;">
69.32
</td>
<td style="text-align:right;">
18.08
</td>
<td style="text-align:right;">
12.59
</td>
</tr>
<tr>
<td style="text-align:left;">
Executives
</td>
<td style="text-align:right;">
43
</td>
<td style="text-align:right;">
586
</td>
<td style="text-align:right;">
67.75
</td>
<td style="text-align:right;">
18.09
</td>
<td style="text-align:right;">
14.16
</td>
</tr>
<tr>
<td style="text-align:left;">
Staffing Practices
</td>
<td style="text-align:right;">
61
</td>
<td style="text-align:right;">
769
</td>
<td style="text-align:right;">
66.32
</td>
<td style="text-align:right;">
16.25
</td>
<td style="text-align:right;">
17.43
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
101
</td>
<td style="text-align:right;">
406
</td>
<td style="text-align:right;">
64.53
</td>
<td style="text-align:right;">
16.26
</td>
<td style="text-align:right;">
19.21
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
105
</td>
<td style="text-align:right;">
611
</td>
<td style="text-align:right;">
63.83
</td>
<td style="text-align:right;">
22.59
</td>
<td style="text-align:right;">
13.58
</td>
</tr>
<tr>
<td style="text-align:left;">
Engagement & Workplace Culture
</td>
<td style="text-align:right;">
32
</td>
<td style="text-align:right;">
295
</td>
<td style="text-align:right;">
63.73
</td>
<td style="text-align:right;">
10.85
</td>
<td style="text-align:right;">
25.42
</td>
</tr>
<tr>
<td style="text-align:left;">
Executives
</td>
<td style="text-align:right;">
41
</td>
<td style="text-align:right;">
785
</td>
<td style="text-align:right;">
63.69
</td>
<td style="text-align:right;">
21.02
</td>
<td style="text-align:right;">
15.29
</td>
</tr>
<tr>
<td style="text-align:left;">
Supervisors
</td>
<td style="text-align:right;">
82
</td>
<td style="text-align:right;">
407
</td>
<td style="text-align:right;">
63.39
</td>
<td style="text-align:right;">
17.44
</td>
<td style="text-align:right;">
19.16
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
102
</td>
<td style="text-align:right;">
1348
</td>
<td style="text-align:right;">
60.61
</td>
<td style="text-align:right;">
21.07
</td>
<td style="text-align:right;">
18.32
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
106
</td>
<td style="text-align:right;">
641
</td>
<td style="text-align:right;">
57.88
</td>
<td style="text-align:right;">
22.31
</td>
<td style="text-align:right;">
19.81
</td>
</tr>
<tr>
<td style="text-align:left;">
Recognition & Empowerment
</td>
<td style="text-align:right;">
72
</td>
<td style="text-align:right;">
434
</td>
<td style="text-align:right;">
57.60
</td>
<td style="text-align:right;">
22.81
</td>
<td style="text-align:right;">
19.59
</td>
</tr>
<tr>
<td style="text-align:left;">
Recognition & Empowerment
</td>
<td style="text-align:right;">
74
</td>
<td style="text-align:right;">
476
</td>
<td style="text-align:right;">
56.09
</td>
<td style="text-align:right;">
18.70
</td>
<td style="text-align:right;">
25.21
</td>
</tr>
<tr>
<td style="text-align:left;">
Engagement & Workplace Culture
</td>
<td style="text-align:right;">
34
</td>
<td style="text-align:right;">
459
</td>
<td style="text-align:right;">
55.12
</td>
<td style="text-align:right;">
20.04
</td>
<td style="text-align:right;">
24.84
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
104
</td>
<td style="text-align:right;">
674
</td>
<td style="text-align:right;">
55.04
</td>
<td style="text-align:right;">
24.78
</td>
<td style="text-align:right;">
20.18
</td>
</tr>
<tr>
<td style="text-align:left;">
Supervisors
</td>
<td style="text-align:right;">
83
</td>
<td style="text-align:right;">
1051
</td>
<td style="text-align:right;">
52.90
</td>
<td style="text-align:right;">
16.46
</td>
<td style="text-align:right;">
30.64
</td>
</tr>
<tr>
<td style="text-align:left;">
Stress & Workload
</td>
<td style="text-align:right;">
94
</td>
<td style="text-align:right;">
281
</td>
<td style="text-align:right;">
52.67
</td>
<td style="text-align:right;">
30.25
</td>
<td style="text-align:right;">
17.08
</td>
</tr>
<tr>
<td style="text-align:left;">
Executives
</td>
<td style="text-align:right;">
42
</td>
<td style="text-align:right;">
268
</td>
<td style="text-align:right;">
51.87
</td>
<td style="text-align:right;">
19.03
</td>
<td style="text-align:right;">
29.10
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
103
</td>
<td style="text-align:right;">
382
</td>
<td style="text-align:right;">
51.31
</td>
<td style="text-align:right;">
30.89
</td>
<td style="text-align:right;">
17.80
</td>
</tr>
<tr>
<td style="text-align:left;">
Career & Personal Development
</td>
<td style="text-align:right;">
12
</td>
<td style="text-align:right;">
103
</td>
<td style="text-align:right;">
50.49
</td>
<td style="text-align:right;">
12.62
</td>
<td style="text-align:right;">
36.89
</td>
</tr>
<tr>
<td style="text-align:left;">
Career & Personal Development
</td>
<td style="text-align:right;">
13
</td>
<td style="text-align:right;">
1202
</td>
<td style="text-align:right;">
47.92
</td>
<td style="text-align:right;">
25.37
</td>
<td style="text-align:right;">
26.71
</td>
</tr>
<tr>
<td style="text-align:left;">
Career & Personal Development
</td>
<td style="text-align:right;">
14
</td>
<td style="text-align:right;">
502
</td>
<td style="text-align:right;">
47.21
</td>
<td style="text-align:right;">
22.31
</td>
<td style="text-align:right;">
30.48
</td>
</tr>
<tr>
<td style="text-align:left;">
Stress & Workload
</td>
<td style="text-align:right;">
92
</td>
<td style="text-align:right;">
510
</td>
<td style="text-align:right;">
43.53
</td>
<td style="text-align:right;">
25.69
</td>
<td style="text-align:right;">
30.78
</td>
</tr>
<tr>
<td style="text-align:left;">
Vision, Mission & Goals
</td>
<td style="text-align:right;">
111
</td>
<td style="text-align:right;">
587
</td>
<td style="text-align:right;">
42.93
</td>
<td style="text-align:right;">
29.13
</td>
<td style="text-align:right;">
27.94
</td>
</tr>
<tr>
<td style="text-align:left;">
Supervisors
</td>
<td style="text-align:right;">
84
</td>
<td style="text-align:right;">
491
</td>
<td style="text-align:right;">
39.71
</td>
<td style="text-align:right;">
21.79
</td>
<td style="text-align:right;">
38.49
</td>
</tr>
<tr>
<td style="text-align:left;">
Recognition & Empowerment
</td>
<td style="text-align:right;">
71
</td>
<td style="text-align:right;">
292
</td>
<td style="text-align:right;">
34.93
</td>
<td style="text-align:right;">
20.55
</td>
<td style="text-align:right;">
44.52
</td>
</tr>
<tr>
<td style="text-align:left;">
Engagement & Workplace Culture
</td>
<td style="text-align:right;">
35
</td>
<td style="text-align:right;">
123
</td>
<td style="text-align:right;">
31.71
</td>
<td style="text-align:right;">
24.39
</td>
<td style="text-align:right;">
43.90
</td>
</tr>
<tr>
<td style="text-align:left;">
Supervisors
</td>
<td style="text-align:right;">
81
</td>
<td style="text-align:right;">
294
</td>
<td style="text-align:right;">
23.13
</td>
<td style="text-align:right;">
21.43
</td>
<td style="text-align:right;">
55.44
</td>
</tr>
<tr>
<td style="text-align:left;">
Recognition & Empowerment
</td>
<td style="text-align:right;">
73
</td>
<td style="text-align:right;">
149
</td>
<td style="text-align:right;">
16.11
</td>
<td style="text-align:right;">
20.81
</td>
<td style="text-align:right;">
63.09
</td>
</tr>
<tr>
<td style="text-align:left;">
Engagement & Workplace Culture
</td>
<td style="text-align:right;">
33
</td>
<td style="text-align:right;">
357
</td>
<td style="text-align:right;">
8.12
</td>
<td style="text-align:right;">
14.29
</td>
<td style="text-align:right;">
77.59
</td>
</tr>
</tbody>
</table>
<br><br><br>

#### Theme Results

![](../reports/figures/linking_agreement_theme.png)

<br>

<table>
<thead>
<tr>
<th style="text-align:left;">
Theme
</th>
<th style="text-align:right;">
Sub-theme
</th>
<th style="text-align:right;">
Total Number
</th>
<th style="text-align:right;">
Strong Agreement (%)
</th>
<th style="text-align:right;">
Weak Agreement (%)
</th>
<th style="text-align:right;">
No Agreement (%)
</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left;">
Compensation & Benefits
</td>
<td style="text-align:right;">
24
</td>
<td style="text-align:right;">
1554
</td>
<td style="text-align:right;">
87.45
</td>
<td style="text-align:right;">
7.98
</td>
<td style="text-align:right;">
4.57
</td>
</tr>
<tr>
<td style="text-align:left;">
Compensation & Benefits
</td>
<td style="text-align:right;">
21
</td>
<td style="text-align:right;">
146
</td>
<td style="text-align:right;">
86.99
</td>
<td style="text-align:right;">
9.59
</td>
<td style="text-align:right;">
3.42
</td>
</tr>
<tr>
<td style="text-align:left;">
Compensation & Benefits
</td>
<td style="text-align:right;">
23
</td>
<td style="text-align:right;">
541
</td>
<td style="text-align:right;">
76.71
</td>
<td style="text-align:right;">
13.12
</td>
<td style="text-align:right;">
10.17
</td>
</tr>
<tr>
<td style="text-align:left;">
Stress & Workload
</td>
<td style="text-align:right;">
93
</td>
<td style="text-align:right;">
929
</td>
<td style="text-align:right;">
69.32
</td>
<td style="text-align:right;">
18.08
</td>
<td style="text-align:right;">
12.59
</td>
</tr>
<tr>
<td style="text-align:left;">
Executives
</td>
<td style="text-align:right;">
43
</td>
<td style="text-align:right;">
586
</td>
<td style="text-align:right;">
67.75
</td>
<td style="text-align:right;">
18.09
</td>
<td style="text-align:right;">
14.16
</td>
</tr>
<tr>
<td style="text-align:left;">
Staffing Practices
</td>
<td style="text-align:right;">
61
</td>
<td style="text-align:right;">
769
</td>
<td style="text-align:right;">
66.32
</td>
<td style="text-align:right;">
16.25
</td>
<td style="text-align:right;">
17.43
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
101
</td>
<td style="text-align:right;">
406
</td>
<td style="text-align:right;">
64.53
</td>
<td style="text-align:right;">
16.26
</td>
<td style="text-align:right;">
19.21
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
105
</td>
<td style="text-align:right;">
611
</td>
<td style="text-align:right;">
63.83
</td>
<td style="text-align:right;">
22.59
</td>
<td style="text-align:right;">
13.58
</td>
</tr>
<tr>
<td style="text-align:left;">
Engagement & Workplace Culture
</td>
<td style="text-align:right;">
32
</td>
<td style="text-align:right;">
295
</td>
<td style="text-align:right;">
63.73
</td>
<td style="text-align:right;">
10.85
</td>
<td style="text-align:right;">
25.42
</td>
</tr>
<tr>
<td style="text-align:left;">
Executives
</td>
<td style="text-align:right;">
41
</td>
<td style="text-align:right;">
785
</td>
<td style="text-align:right;">
63.69
</td>
<td style="text-align:right;">
21.02
</td>
<td style="text-align:right;">
15.29
</td>
</tr>
<tr>
<td style="text-align:left;">
Supervisors
</td>
<td style="text-align:right;">
82
</td>
<td style="text-align:right;">
407
</td>
<td style="text-align:right;">
63.39
</td>
<td style="text-align:right;">
17.44
</td>
<td style="text-align:right;">
19.16
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
102
</td>
<td style="text-align:right;">
1348
</td>
<td style="text-align:right;">
60.61
</td>
<td style="text-align:right;">
21.07
</td>
<td style="text-align:right;">
18.32
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
106
</td>
<td style="text-align:right;">
641
</td>
<td style="text-align:right;">
57.88
</td>
<td style="text-align:right;">
22.31
</td>
<td style="text-align:right;">
19.81
</td>
</tr>
<tr>
<td style="text-align:left;">
Recognition & Empowerment
</td>
<td style="text-align:right;">
72
</td>
<td style="text-align:right;">
434
</td>
<td style="text-align:right;">
57.60
</td>
<td style="text-align:right;">
22.81
</td>
<td style="text-align:right;">
19.59
</td>
</tr>
<tr>
<td style="text-align:left;">
Recognition & Empowerment
</td>
<td style="text-align:right;">
74
</td>
<td style="text-align:right;">
476
</td>
<td style="text-align:right;">
56.09
</td>
<td style="text-align:right;">
18.70
</td>
<td style="text-align:right;">
25.21
</td>
</tr>
<tr>
<td style="text-align:left;">
Engagement & Workplace Culture
</td>
<td style="text-align:right;">
34
</td>
<td style="text-align:right;">
459
</td>
<td style="text-align:right;">
55.12
</td>
<td style="text-align:right;">
20.04
</td>
<td style="text-align:right;">
24.84
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
104
</td>
<td style="text-align:right;">
674
</td>
<td style="text-align:right;">
55.04
</td>
<td style="text-align:right;">
24.78
</td>
<td style="text-align:right;">
20.18
</td>
</tr>
<tr>
<td style="text-align:left;">
Supervisors
</td>
<td style="text-align:right;">
83
</td>
<td style="text-align:right;">
1051
</td>
<td style="text-align:right;">
52.90
</td>
<td style="text-align:right;">
16.46
</td>
<td style="text-align:right;">
30.64
</td>
</tr>
<tr>
<td style="text-align:left;">
Stress & Workload
</td>
<td style="text-align:right;">
94
</td>
<td style="text-align:right;">
281
</td>
<td style="text-align:right;">
52.67
</td>
<td style="text-align:right;">
30.25
</td>
<td style="text-align:right;">
17.08
</td>
</tr>
<tr>
<td style="text-align:left;">
Executives
</td>
<td style="text-align:right;">
42
</td>
<td style="text-align:right;">
268
</td>
<td style="text-align:right;">
51.87
</td>
<td style="text-align:right;">
19.03
</td>
<td style="text-align:right;">
29.10
</td>
</tr>
<tr>
<td style="text-align:left;">
Tools, Equipment & Physical Environment
</td>
<td style="text-align:right;">
103
</td>
<td style="text-align:right;">
382
</td>
<td style="text-align:right;">
51.31
</td>
<td style="text-align:right;">
30.89
</td>
<td style="text-align:right;">
17.80
</td>
</tr>
<tr>
<td style="text-align:left;">
Career & Personal Development
</td>
<td style="text-align:right;">
12
</td>
<td style="text-align:right;">
103
</td>
<td style="text-align:right;">
50.49
</td>
<td style="text-align:right;">
12.62
</td>
<td style="text-align:right;">
36.89
</td>
</tr>
<tr>
<td style="text-align:left;">
Career & Personal Development
</td>
<td style="text-align:right;">
13
</td>
<td style="text-align:right;">
1202
</td>
<td style="text-align:right;">
47.92
</td>
<td style="text-align:right;">
25.37
</td>
<td style="text-align:right;">
26.71
</td>
</tr>
<tr>
<td style="text-align:left;">
Career & Personal Development
</td>
<td style="text-align:right;">
14
</td>
<td style="text-align:right;">
502
</td>
<td style="text-align:right;">
47.21
</td>
<td style="text-align:right;">
22.31
</td>
<td style="text-align:right;">
30.48
</td>
</tr>
<tr>
<td style="text-align:left;">
Stress & Workload
</td>
<td style="text-align:right;">
92
</td>
<td style="text-align:right;">
510
</td>
<td style="text-align:right;">
43.53
</td>
<td style="text-align:right;">
25.69
</td>
<td style="text-align:right;">
30.78
</td>
</tr>
<tr>
<td style="text-align:left;">
Vision, Mission & Goals
</td>
<td style="text-align:right;">
111
</td>
<td style="text-align:right;">
587
</td>
<td style="text-align:right;">
42.93
</td>
<td style="text-align:right;">
29.13
</td>
<td style="text-align:right;">
27.94
</td>
</tr>
<tr>
<td style="text-align:left;">
Supervisors
</td>
<td style="text-align:right;">
84
</td>
<td style="text-align:right;">
491
</td>
<td style="text-align:right;">
39.71
</td>
<td style="text-align:right;">
21.79
</td>
<td style="text-align:right;">
38.49
</td>
</tr>
<tr>
<td style="text-align:left;">
Recognition & Empowerment
</td>
<td style="text-align:right;">
71
</td>
<td style="text-align:right;">
292
</td>
<td style="text-align:right;">
34.93
</td>
<td style="text-align:right;">
20.55
</td>
<td style="text-align:right;">
44.52
</td>
</tr>
<tr>
<td style="text-align:left;">
Engagement & Workplace Culture
</td>
<td style="text-align:right;">
35
</td>
<td style="text-align:right;">
123
</td>
<td style="text-align:right;">
31.71
</td>
<td style="text-align:right;">
24.39
</td>
<td style="text-align:right;">
43.90
</td>
</tr>
<tr>
<td style="text-align:left;">
Supervisors
</td>
<td style="text-align:right;">
81
</td>
<td style="text-align:right;">
294
</td>
<td style="text-align:right;">
23.13
</td>
<td style="text-align:right;">
21.43
</td>
<td style="text-align:right;">
55.44
</td>
</tr>
<tr>
<td style="text-align:left;">
Recognition & Empowerment
</td>
<td style="text-align:right;">
73
</td>
<td style="text-align:right;">
149
</td>
<td style="text-align:right;">
16.11
</td>
<td style="text-align:right;">
20.81
</td>
<td style="text-align:right;">
63.09
</td>
</tr>
<tr>
<td style="text-align:left;">
Engagement & Workplace Culture
</td>
<td style="text-align:right;">
33
</td>
<td style="text-align:right;">
357
</td>
<td style="text-align:right;">
8.12
</td>
<td style="text-align:right;">
14.29
</td>
<td style="text-align:right;">
77.59
</td>
</tr>
</tbody>
</table>
