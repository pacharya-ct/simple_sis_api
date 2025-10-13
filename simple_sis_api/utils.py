'''
utils.py
Author: Prabha Acharya
Create date: 20240402
Version: 0.1
'''
import datetime as dt

def parsedate(val):
    if not val:
        return val
    return dt.datetime.fromisoformat(val)

FUTURE_OFF_DATE = dt.datetime(3000, 1, 1, tzinfo=dt.UTC)

# define the non string attribute types 
# key is attribute name and the value is the function used to cast it to the expected datatype
ATTR_DATATYPE_MAPPING = dict(latitude=float,
    longitude=float, 
    elevation=float,
    xcoord=float,
    ycoord=float,
    zcoord=float,
    ondate=parsedate,
    offdate=parsedate,
)

