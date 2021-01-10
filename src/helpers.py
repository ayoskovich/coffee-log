#!/usr/bin/env python
# coding: utf-8

# In[ ]:


left = 0.125  # the left side of the subplots of the figure
right = 0.9   # the right side of the subplots of the figure
bottom = 0.1  # the bottom of the subplots of the figure
top = 0.9     # the top of the subplots of the figure
wspace = 0.5  # the amount of width reserved for space between subplots,
              # expressed as a fraction of the average axis width
hspace = 0.5  # the amount of height reserved for space between subplots,
              # expressed as a fraction of the average axis height

SAMP_WARNING = '(Groups with < 10 observations omitted)'
    
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
    

def computeUptime(c, g, b):
    """Compute uptime for brewing. """
    return c + g + b


def save_fig(f, name):
    f.savefig(f'graphs/{name}')
    f.savefig(f'/home/anthony/personalSite/content/project/coffee/{name}')

