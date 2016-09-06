#!../../bin/python
from utils import loginit
import social.interface
import social.social_types

##################
## Authorization
##################
def getUser(token):
        ## Verify the user is authenticated by social provider
        ## Force facebook for now
        provider = 1
        auth = Social.get_provider(SocialType.provider)
        if auth.verify(token):
            ## Great!  Now lets see if they are registered with us
            ## First get email from social provider
            user = None
            userInfo = auth.getUserInfo(token)
            if 'email' in userInfo:
                user = dbm.getUserByEmail(email)
                if user is None:
                    ## We don't have a local user - let's make one
                    createLocalUser(userInfo)
                    user = dbm.getUserByEmail(email)
            else:
                # facebook authentication successful, but no local account (ie- email)
                pass
            
            return user
        else:
            raise NameError("User failed authentication")

def createLocalUser(userInfo):
        socialId, firstName, lastName = None
        if 'id' in userInfo:
            socialId = userInfo['id']
        if 'first_name' in  userInfo:
            firstName = userInfo['first_name']
        if 'last_name' in userInfo:
            lastName = userInfo['last_name']
        dbm.addNormalUser(email=email, firstName=firstName, lastName=lastName, facebookId=socialId)