#!../bin/python
import logging
from flask import render_template
from app.admin import admin
from app.admin.decorators import require_admin, require_token
from .helpers import getAllWhiskies, deleteWhiskey, addWhiskey

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

@admin.route('/whiskey/addWhiskey')
@require_token
@require_admin
def add_whiskey():
    logger.debug("Dump of args for add_whiskey: %s", request.args)
    name = request.args.get('name')
    logger.debug("Adding whiskey", name)

    return addWhiskey(name)

@admin.route('/whiskey/updateWhiskey')
@require_token
@require_admin
def update_whiskey():
    logger.debug("Dump of args for update_whiskey: %s", request.args)
    name = request.args.get('name')
    logger.debug("updating whiskey", name)

    return updateWhiskey(name)

@admin.route('/whiskey/deleteWhiskey')
@require_token
@require_admin
def delete_whiskey():
    logger.debug("Dump of args for delete_whiskey: %s", request.args)
    name = request.args.get('name')
    logger.debug("Deleting whiskey", name)

    return deleteWhiskey(name)

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