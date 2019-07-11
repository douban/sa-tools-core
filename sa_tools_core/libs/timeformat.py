# coding: utf-8

import time
from datetime import datetime


# TODO: more flexiable time format
def timeformat(time_string):
    now_ts = int(time.time())
    dt = None
    try:
        time_int = int(time_string)
        if time_int < 0:
            ts = now_ts + time_int * 60
            dt = datetime.fromtimestamp(ts)
            return dt
        else:
            # timestamp ? time range limit ?
            return None
    except:
        pass
    for p in ('%Y-%m-%d %H:%M',
              '%Y-%m-%d %H:%M:%S',
              '%Y-%m-%dT%H:%M:%S',
              ):
        try:
            dt = datetime.strptime(time_string, p)
            return dt
        except:
            pass
    return dt
