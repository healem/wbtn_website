#!../../bin/python

import logging
from utils import loginit
from . import facebook
from social_types import SocialType

class SocialFactory(object):
    
    logger = logging.getLogger("SocialFactory")
    
    @classmethod
    def get_provider(cls, providerType):
        cls.logger.debug("Getting provider for type: %d ", providerType)
        if providerType == SocialType.facebook:
            return facebook.Facebook()
        else:
            cls.logger.error("Invalid provider type: %d", providerType)
            return None
