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
import matplotlib

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


df.plot.scatter(x='date', y='cTime');


# In[ ]:


df['coffee'].value_counts().plot(kind='barh');


# In[ ]:


df.plot.scatter(x='date', y='duration');


# In[ ]:


df['duration'].hist();


# In[ ]:


df['cTime'].hist();


# In[ ]:


df['gTime'].hist();


# In[ ]:


df['bTime'].hist();


# In[ ]:


df.dtypes


# In[ ]:




