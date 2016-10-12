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
    #logger.debug("Dump of args for get_all_users: %s", request.args)
    currentPage = request.args.get('page', 1, type=int)
    itemsPerPage = request.args.get('rows', 10, type=int)
    logger.info("Getting user page %d with %d items per page", currentPage, itemsPerPage)
    if itemsPerPage > 100:
        logger.warn("%d Items per page exceed max of 100, forcing to 100", itemsPerPage)
        itemsPerPage = 100
    return getAllUsers(currentPage, itemsPerPage)
    
    