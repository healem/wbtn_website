from flask_restplus import Api

from .auth import api as auth_api

api = Api(
    title='WBTN REST',
    version='1.0',
    description='HTTP REST interface to WBTN backend',
)

api.add_namespace(auth_api)