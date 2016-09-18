#!../../bin/python
import logging
from flask_restplus import Api
from . import decorators

api = Api( blueprint,
    title='WBTN REST',
    version='1.0',
    description='HTTP REST interface to WBTN backend',
    doc=False,
    decorators=[require_token, require_admin, require_blog, require_college]
)
