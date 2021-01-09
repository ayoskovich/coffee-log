#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib

get_ipython().run_line_magic('run', './helpers.ipynb')

df = pd.read_csv('data/coffee.csv')
df.head()


# In[ ]:


get_ipython().run_line_magic('run', './helpers.ipynb')

df = pd.read_csv('data/coffee.csv')

df.replace('na', np.NaN, inplace=True)

df['date'] = df['date'].apply(pd.to_datetime)

df['cTime'] = df['cTime'].apply(timeToSec)
df['gTime'] = df['gTime'].apply(timeToSec)
df['bTime'] = df['bTime'].apply(timeToSec)

df['startTime'] = df['startTime'].apply(getTime)
df['endTime'] = df['endTime'].apply(getTime)

df['count'] = df['count'].apply(toFloat)
df['over'] = df['over'].apply(toFloat)


# In[ ]:


df.head()


# In[ ]:


df['cTime'].hist()


# In[ ]:


df.dtypes


# In[ ]:


nat = np.datetime64('NaT')


# In[ ]:


nat


# In[ ]:


pd.Timestamp(nat)


# In[ ]:


dt = df.startTime.tail(1).values[0]


# In[ ]:


dt


# In[ ]:


pd.Timestamp(dt).time()


# In[ ]:




