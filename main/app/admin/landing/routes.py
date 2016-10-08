#!../bin/python
import logging
from flask import render_template
from app.admin import admin
from app.admin.decorators import require_admin, require_token

logger = logging.getLogger(__name__)

@admin.route('/')
@require_token
@require_admin
def frontend():
    ''' Front landing page '''
    return render_template("frontend.html")

@admin.route('/minor/')
@require_token
@require_admin
def minor():
    ''' Minor '''
    return render_template("minor.html")