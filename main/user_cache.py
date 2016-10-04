#!bin/python
from expiringdict import ExpiringDict

# Cache entries expire in 1 hour, effectively expiring the session
userCache = ExpiringDict(max_len=500, max_age_seconds=3600)
