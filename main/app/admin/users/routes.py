#!../bin/python
import logging
from flask import render_template, request
from .helpers import getAllUsers
from app.admin import admin
from app.admin.decorators import require_admin, require_token

logger = logging.getLogger(__name__)
    
@admin.route('/users/', strict_slashes=False)
@require_token
@require_admin
def users_view():
    ''' Users view page '''
    return render_template("users.html")

@admin.route('/users/getAllUsers')
@require_token
@require_admin
def get_all_users():
    currentPage = request.args.get('currentPage', 1, type=int)
    itemsPerPage = request.args.get('itemsPerPage', 10, type=int)
    if itemsPerPage > 100:
        logger.warn("%d Items per page exceed max of 100, forcing to 100", itemsPerPage)
        itemsPerPage = 100
    return getAllUsers(currentPage, itemsPerPage)
    
    