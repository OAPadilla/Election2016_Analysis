#!/usr/bin/env python
"""political_election_analysis.py: Visualizes polling data from HuffPost's aggregator."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('darkgrid')

# Source of poll dataset is provided by the Huffington Post
source = 'http://elections.huffingtonpost.com/pollster/2016-general-election-trump-vs-clinton.csv'
poll_df = pd.read_csv(source)
# print(poll_df.head())

# Count of affiliated polls (None, Dem, Rep, Other)
poll_affil = sns.factorplot('Affiliation', data=poll_df, aspect=1.25, kind='count')
poll_affil.fig.suptitle("Poll Affiliations")

# Count of population (Likely Voters, Registered Voters, Adults) for each affiliation polled
lvrv_affil = sns.factorplot('Affiliation', data=poll_df, hue='Population', aspect=1.75, kind='count')
lvrv_affil.fig.suptitle("LV and RV Poll Affiliations")

# Types or 'Mode's of polling done
poll_types = sns.factorplot('Mode', data=poll_df, aspect=1.75, kind='count')
poll_types.fig.suptitle("Polling Methods")

# Keep polling data of Likely Voters and Registered Voters only, no party specific polls
poll_df = poll_df[(poll_df.Population == 'Likely Voters') | (poll_df.Population == 'Registered Voters')]
# print(poll_df.head())

# Average of all polls
avg = pd.DataFrame(poll_df.mean(), columns=['AVG'])
avg.drop(['Number of Observations', 'Question Iteration'], axis=0, inplace=True)

# Standard deviation of all polls
std = pd.DataFrame(poll_df.std(), columns=['STDEV'])
std.drop(['Number of Observations', 'Question Iteration'], axis=0, inplace=True)

# Bar graph plot of AVG and STDEV
avg.plot(yerr=std, kind='bar', legend=False).set_title("Average of All Polls")

# AVG and STDEV of polls concatenated, and outputted
poll_avg = pd.concat([avg, std], axis=1)
poll_avg.columns = ['ALL: AVG', 'ALL: STDEV']
print('\n')
print(poll_avg)

# Adds 'Difference' column to dframe for the percentage margin between Clinton(+)/Trump(-)
pd.options.mode.chained_assignment = None  # default='warn'
poll_df['Difference'] = (poll_df.Clinton - poll_df.Trump) / 100

# Compares average 'Difference' in polls between different 'Modes' of polling
avg_mode_diff = sns.factorplot('Mode', 'Difference', aspect=2, data=poll_df)
avg_mode_diff.fig.suptitle("Comparing Averages between Types of Polling: Clinton(+)/Trump(-)")

# DataFrames for Registered Voters (RV) and Likely Voters (LV) polled
rv_df = poll_df[poll_df.Population == 'Registered Voters']
lv_df = poll_df[poll_df.Population == 'Likely Voters']

# Average of Registered Voter polls
rv_avg = pd.DataFrame(rv_df.mean())
rv_avg.drop(['Number of Observations','Question Iteration', 'Difference'], axis=0, inplace=True)

# Standard deviation of Registered Voter polls
rv_std = pd.DataFrame(rv_df.std())
rv_std.drop(['Number of Observations','Question Iteration', 'Difference'], axis=0, inplace=True)

# Average of Likely Voter polls
lv_avg = pd.DataFrame(lv_df.mean())
lv_avg.drop(['Number of Observations','Question Iteration', 'Difference'], axis=0, inplace=True)

# Standard deviation of Likely Voter polls
lv_std = pd.DataFrame(lv_df.std())
lv_std.drop(['Number of Observations','Question Iteration', 'Difference'], axis=0, inplace=True)

# Bar graph plot of RV and LV to compare
rv_avg.plot(yerr=std, kind='bar', legend=False, color='lightgreen').set_title("Poll Average: Registered Voters")
lv_avg.plot(yerr=std, kind='bar', legend=False, color='green').set_title("Poll Average: Likely Voters")

# AVG and STDEV of RV polls concatenated and outputted
rv_avg = pd.concat([rv_avg, rv_std], axis=1)
rv_avg.columns = ['RV: AVG', 'RV: STDEV']
print('\n')
print(rv_avg)

# AVG and STDEV of LV polls concatenated and outputted
lv_avg = pd.concat([lv_avg, lv_std], axis=1)
lv_avg.columns = ['LV: AVG', 'LV: STDEV']
print('\n')
print(lv_avg)

# Groups dataframe by Start Date
poll_df = poll_df.groupby(['Start Date'], as_index=False).mean()
# Plots the mean of each Start Date group
date_means = poll_df.plot('Start Date', 'Difference', figsize=(12, 4), marker='o', linestyle='-', color='purple')
date_means.set_title("Daily Polling Means: Differences Clinton(+)/Trump(-)")

# Gathers rows of polls done from Sept to election day
row_in = 0
date_dict = {}  # { date : row# }
for date in poll_df['Start Date']:
    if date[0:7] == '2016-09' or date[0:7] == '2016-10' or date[0:7] == '2016-11':  # Poll dates Sept-End
        date_dict[date] = row_in
    row_in += 1

x_max = max(date_dict.values())     # Row of last poll done
x_min = min(date_dict.values())     # Row of first polls done

# Plots polling figures from Sept, through the debates, until election day Nov 4
poll_df.plot('Start Date', 'Difference', figsize=(12, 4), marker='o', linestyle='-', color='purple',
             xlim=(x_min, x_max)).set_title("Daily Polling Means with Debates and Comey Letter Event Marked")

# Markers for debate days and comey letter release, to observe effects in the polls
debate_dates = ['2016-09-26', '2016-10-09', '2016-10-19']
comey_letter = '2016-10-28'
for point in date_dict.keys():
    if point in debate_dates:
        plt.axvline(x=date_dict[point], linewidth=4, color='grey')
    elif point == comey_letter:
        plt.axvline(x=date_dict[point], linewidth=4, color='red')

# Displays Visualizations
plt.show()
