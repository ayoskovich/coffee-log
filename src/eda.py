#!/usr/bin/env python
# coding: utf-8

# ## Questions
# 
# - Do the times vary by coffee?
# - Did I get faster at grinding?
# - Did I get better at eyeballing the pours?
# - Total time vs. unaccounted for time

# In[ ]:


import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import calplot

get_ipython().run_line_magic('run', './helpers.ipynb')

df = (
    pd.read_csv('data/coffee.csv')
    .drop(labels=['Unnamed: 10', 'Unnamed: 11'], axis=1)
)

df.replace('na', np.NaN, inplace=True)

df['date'] = df['date'].apply(pd.to_datetime)

df['cTime'] = df['cTime'].apply(timeToSec)
df['gTime'] = df['gTime'].apply(timeToSec)
df['bTime'] = df['bTime'].apply(timeToSec)

df['startTime'] = df['startTime'].apply(getTime)
df['endTime'] = df['endTime'].apply(getTime)

df['count'] = df['count'].apply(toFloat)
df['over'] = df['over'].apply(toFloat)

df['duration'] = tryTime((df.endTime - df.startTime).values)
df['duration'] = df['duration'].dt.components.minutes

plt.rcParams.update({'font.size': 18})


# In[ ]:


calplot.calplot(df['date'].value_counts());


# In[ ]:


from matplotlib.ticker import MaxNLocator
fig, ax = plt.subplots(1,1, figsize=(15,5))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
df['coffee'].value_counts().plot(kind='barh');
ax.set(xlabel='Amount of Observations', title='Amounts of different coffees');
plt.tight_layout()
save_fig(plt.gcf(), 'coffee_bar.png')


# In[ ]:


(
    df
    #.loc[~df.duration.isna()]
    .loc[df.coffee != 'mix']
    ['coffee']
    .value_counts()
)


# In[ ]:


# Coffees that have more than 10 observations
overTen = (
    df
    .loc[df.coffee != 'mix']
    ['coffee']
    .value_counts()
    .loc[lambda x: x > 10]
    .index
)


# In[ ]:


fig, ax = plt.subplots(1,1, figsize=(15,5))
(
    df
    .loc[~df.duration.isna()]
    .loc[df.coffee != 'mix']
    .pipe(lambda x: sns.scatterplot(x='date', y='duration', data=x, ax=ax))
    .set(
        title='Total Time Spent Making Coffee Each Day', xlabel='Date', ylabel='Total Time (minutes)'
    )
);
plt.tight_layout()
save_fig(fig, 'total.png')


# In[ ]:


fig, ax = plt.subplots(1,1, figsize=(15,5))
plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
(
    df
    .loc[~df.duration.isna()]
    .loc[df.coffee.isin(overTen)]
    .pipe(lambda x: sns.boxplot(x='duration', y='coffee', orient='h', data=x, ax=ax))
    .set(
        title=f'Variation of Total Brew Times Across Coffees\n{SAMP_WARNING}',
        xlabel='Total brew time (minutes)',
        ylabel='Type of Coffee'
    )
);
plt.tight_layout()
save_fig(fig, 'total_brew.png')


# In[ ]:


fig, ax = plt.subplots(1,1, figsize=(15,5))
plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
(
    df
    .loc[df.coffee.isin(overTen)]
    .pipe(lambda x: sns.boxplot(x='gTime', y='coffee', orient='h', data=x, ax=ax))
    .set(
        title=f'Amount of time it takes to grind\n{SAMP_WARNING}',
        xlabel='Grind time (seconds)',
        ylabel='Type of Coffee'
    )
);
plt.tight_layout()
save_fig(fig, 'grind_time.png')


# In[ ]:


fig, ax = plt.subplots(1,1, figsize=(15,5))
plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
(
    df
    .loc[df.coffee.isin(overTen)]
    .pipe(lambda x: sns.boxplot(x='bTime', y='coffee', orient='h', data=x, ax=ax))
    .set(
        title=f'Drawdown Time Varies By Coffee\n{SAMP_WARNING}',
        xlabel='Drawdown (seconds)',
        ylabel='Type of Coffee'
    )
);
plt.tight_layout()
save_fig(fig, 'draw_down.png')


# In[ ]:


fig, ax = plt.subplots(1,1, figsize=(15,5))

(
    df
    .pipe(lambda x: x.assign(cTime = x.cTime / 60))
    .pipe(lambda x: sns.scatterplot(x='date', y='cTime', data=x, ax=ax))
    .set(xticklabels=[], title='Minutes To Count Beans', xlabel='Time', ylabel='Time (minutes)')
);
plt.tight_layout()
save_fig(fig, 'c_over_time.png')


# In[ ]:


fig, ax = plt.subplots(1,1, figsize=(15,5))
(
    sns.scatterplot(x='date', y='over', data=df, ax=ax)
    .set(xticklabels=[], title='Overages over time', xlabel='Time', ylabel='Amount overpoured (number of beans)')
)
plt.tight_layout()
ax.axhline(color='red');
save_fig(fig, 'overages.png')


# In[ ]:


fig, ax = plt.subplots(1,1, figsize=(15,5))
plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
(
    df
    .loc[df.coffee.isin(overTen)]
    .pipe(lambda x: sns.boxplot(x='over', y='coffee', orient='h', data=x, ax=ax))
    .set(
        title=f'Eyeballing\n{SAMP_WARNING}',
        xlabel='Overage (# of beans)',
        ylabel='Type of Coffee'
    )
);
plt.tight_layout()
ax.axvline(color='red');
save_fig(fig, 'overages_by_cof.png')


# In[ ]:


fig, ax = plt.subplots(1,1, figsize=(15,5))
(
    df
    .loc[~df.duration.isna()]
    .loc[df.coffee != 'mix']
    .pipe(lambda x: x.assign(uptime = computeUptime(x.cTime, x.gTime, x.bTime) / 60 ))
    .pipe(lambda x: x.assign(unac = x.duration - x.uptime))
    
    .pipe(lambda x: sns.scatterplot(x='date', y='unac', data=x, ax=ax)
         .set(title='Random time over time', xlabel='Time', ylabel='Unaccounted for', xticklabels=[]))
);
plt.tight_layout()

