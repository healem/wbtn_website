#!/home/bythenum/public_html/whiskey/main/bin/python
from flask import Blueprint

admin = Blueprint('admin',
                  __name__,
                  template_folder='templates',
                  static_folder='static')

from app.admin.auth import routes
from app.admin.landing import routes
from app.admin.users import routes
from app.admin.decorators import require_admin, require_token
