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


# In[ ]:


df.shape


# In[ ]:


calplot.calplot(df['date'].value_counts());


# In[ ]:


df.head()


# In[ ]:


from matplotlib.ticker import MaxNLocator
ax = plt.figure().gca()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
df['coffee'].value_counts().plot(kind='barh');
ax.set(xlabel='Amount of Observations', title='Amounts of different coffees');


# In[ ]:


(
    df
    #.loc[~df.duration.isna()]
    .loc[df.coffee != 'mix']
    ['coffee']
    .value_counts()
)


# In[ ]:


df.head()


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
fig.savefig('totaltime.png')


# In[ ]:


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 15))

    
plt.subplots_adjust(left, bottom, right, top, wspace, hspace)

(
    df
    .loc[~df.duration.isna()]
    .loc[df.coffee != 'mix']
    .pipe(lambda x: sns.boxplot(x='duration', y='coffee', orient='h', data=x, ax=ax1))
    .set(
        title='Variation of Total Brew Times Across Coffees',
        xlabel='Total brew time (minutes)',
        ylabel='Type of Coffee'
    )
);

(
    df
    #.loc[~df.duration.isna()]
    .loc[df.coffee != 'mix']
    .pipe(lambda x: sns.boxplot(x='gTime', y='coffee', orient='h', data=x, ax=ax2))
    .set(
        title='Amount of time it takes to grind',
        xlabel='Grind time (seconds)',
        ylabel='Type of Coffee'
    )
);

(
    df
    #.loc[~df.duration.isna()]
    .loc[df.coffee != 'mix']
    .pipe(lambda x: sns.boxplot(x='bTime', y='coffee', orient='h', data=x, ax=ax3))
    .set(
        title='Drawdown time',
        xlabel='Drawdown (seconds)',
        ylabel='Type of Coffee'
    )
);


# In[ ]:


fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15,5))

(
    sns.scatterplot(x='date', y='cTime', data=df, ax=ax1)
    .set(xticklabels=[], title='Count time over time', xlabel='Time')
);

(
    sns.scatterplot(x='date', y='over', data=df, ax=ax2)
    .set(xticklabels=[], title='Overages over time', xlabel='Time')
);
ax2.axhline(color='red');


# In[ ]:


get_ipython().run_line_magic('run', './helpers.ipynb')

(
    df
    .loc[~df.duration.isna()]
    .loc[df.coffee != 'mix']
    .pipe(lambda x: x.assign(uptime = computeUptime(x.cTime, x.gTime, x.bTime) / 60 ))
    .pipe(lambda x: x.assign(unac = x.duration - x.uptime))
    
    .pipe(lambda x: sns.scatterplot(x='date', y='unac', data=x)
         .set(title='Random time over time', xlabel='Time', ylabel='Unaccounted for', xticklabels=[]))
);

