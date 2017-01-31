#!../../bin/python
import logging
from flask import Blueprint
from flask_restplus import Api

apiBlueprint = Blueprint('api', __name__)

api = Api( apiBlueprint,
    title='WBTN REST',
    version='1.0',
    description='HTTP REST interface to WBTN backend',
    doc=False,
)
