#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def timeToSec(time):
    """Returns number of seconds in time. """
    try:
        mins, secs = time.split(':')
    except ValueError:
        return np.nan
    
    return int(mins)*60 + int(secs)


def getTime(time):
    """Get the time. """
    return pd.to_datetime(time, errors='coerce')


def getTime2(time):
    try:
        return pd.Timestamp(time).time()
    except:
        return pd.Timestamp(np.datetime64('NaT'))
    
    
def toFloat(x):
    """ Nicely convert to float. """
    try:
        return np.float(x)
    except:
        return np.nan
    
    
def tryTime(x):
    """ Convert a timediff"""
    try:
        return x.astype('timedelta64[m]')
    except:
        return np.datetime64('NaT')

