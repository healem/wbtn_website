#!../bin/python
import logging
from flask import render_template
from app.admin import admin
from app.admin.decorators import require_admin, require_token

logger = logging.getLogger(__name__)

@admin.route('/whiskey/whiskies/')
@require_token
@require_admin
def whiskies():
    ''' Front landing page '''
    return render_template("whiskies.html")

@admin.route('/whiskey/getAllWhiskies')
@require_token
@require_admin
def get_all_whiskies():
    #logger.debug("Dump of args for get_all_whiskies: %s", request.args)
    currentPage = request.args.get('page', 1, type=int)
    itemsPerPage = request.args.get('rows', 10, type=int)
    sortField = request.args.get('sort', None, type=str)
    #logger.info("Getting whiskey page %d with %d items per page", currentPage, itemsPerPage)
    if itemsPerPage > 100:
        logger.warn("%d Items per page exceed max of 100, forcing to 100", itemsPerPage)
        itemsPerPage = 100
    return getAllWhiskies(currentPage, itemsPerPage, sortField)

@admin.route('/whiskey/college_rating/')
@require_token
@require_admin
def college_rating():
    ''' Front landing page '''
    return render_template("college_rating.html")

@admin.route('/whiskey/user_rating/')
@require_token
@require_admin
def user_rating():
    ''' Front landing page '''
    return render_template("user_rating.html")