#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

df = pd.read_csv('data/coffee.csv')
df


# In[ ]:


[print(x) for x in df.columns]


# In[ ]:


df.head()


# In[ ]:


df['coffee'].unique()

