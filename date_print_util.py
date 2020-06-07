import time
import datetime

def unix2date(x):
        return datetime.datetime.utcfromtimestamp(x)
    
def sec2dirname(t):
    return(unix2date(t).strftime("%Y-%m-%d"))

def unix2datestr(x):
        return(unix2date(x).strftime('%Y-%m-%dT%H:%M:%S'))


def unix2datestr(x):
        return(unix2date(x).strftime('%Y-%m-%dT%H:%M:%S'))
