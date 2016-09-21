#!../../bin/python
from expiringdict import ExpiringDict

userCache = ExpiringDict(max_len=500, max_age_seconds=3600)
