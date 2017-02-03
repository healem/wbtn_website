#!../bin/python
import logging
import json
from flask import render_template, request
from app.admin import admin
from app.admin.decorators import require_admin, require_token
from .helpers import getAllWhiskies, deleteWhiskey, addWhiskey, updateWhiskey, getAllRatings, deleteRating, addRating, updateRating

logger = logging.getLogger(__name__)

@admin.route('/whiskey/whiskies/')
@require_token
@require_admin
def whiskies():
    ''' Front landing page '''
    return render_template("whiskies.html")

@admin.route('/whiskey/whiskey', methods=['GET', 'POST'])
@require_token
@require_admin
def whiskey():
    ''' Handle all edit commands '''
    logger.debug("Dump of form for whiskey: %s", request.form)
    oper = request.form.get('oper', type=str)
    logger.debug("Requested operation: {}".format(oper))
    if oper == 'add':
        name = request.form.get('name', type=str)
        price = request.form.get('price', type=float)
        proof = request.form.get('proof', type=float)
        style = request.form.get('style', type=str)
        age = request.form.get('age', type=int)
        url = request.form.get('url', None, type=str)
        logger.debug("adding whiskey {}".format(name))
        return addWhiskey(name, price, proof, style, age, url)
    elif oper == 'edit':
        name = request.form.get('name', type=str)
        price = request.form.get('price', type=float)
        proof = request.form.get('proof', type=float)
        style = request.form.get('style', type=str)
        age = request.form.get('age', type=int)
        icon = request.form.get('icon', None, type=str)
        url = request.form.get('url', None, type=str)
        logger.debug("updating whiskey {}".format(name))
        return updateWhiskey(name, price, proof, style, age, icon, url)
    elif oper == 'del':
        # The "name" of the whiskey comes in as "id"
        name = request.form.get('id', type=str)
        logger.debug("deleting whiskey {}".format(name))
        return deleteWhiskey(name)
    else:
        logger.warn("Unsupported operation:{}".format(oper))
        return "Unsupported operation: {}".format(oper)

@admin.route('/whiskey/getAllWhiskies')
@require_token
@require_admin
def get_all_whiskies():
    #logger.debug("Dump of args for get_all_whiskies: %s", request.args)
    currentPage = request.args.get('page', 1, type=int)
    itemsPerPage = request.args.get('rows', 10, type=int)
    sortField = request.args.get('sort', None, type=str)
    namesOnly = request.args.get('namesOnly', False, type=bool)
    logger.info("Getting whiskey page %d with %d items per page and namesOnly %s", currentPage, itemsPerPage, namesOnly)
    if itemsPerPage > 100:
        logger.warn("%d Items per page exceed max of 100, forcing to 100", itemsPerPage)
        itemsPerPage = 100
        
    return getAllWhiskies(currentPage, itemsPerPage, sortField, namesOnly)

@admin.route('/whiskey/ratings/')
@require_token
@require_admin
def ratings():
    ''' Front landing page '''
    return render_template("ratings.html")

@admin.route('/whiskey/rating', methods=['GET', 'POST'])
@require_token
@require_admin
def rating():
    ''' Handle all edit commands '''
    logger.debug("Dump of form for rating: %s", request.form)
    oper = request.form.get('oper', type=str)
    logger.debug("Requested operation: {}".format(oper))
    if oper == 'add':
        whiskeyId = request.form.get('whiskeyId', type=int)
        userId = request.form.get('userId', type=int)
        rating = request.form.get('rating', type=float)
        notes = request.form.get('notes', type=str)
        sweet = request.form.get('sweet', type=float)
        sour = request.form.get('sour', type=float)
        heat = request.form.get('heat', type=float)
        smooth = request.form.get('smooth', type=float)
        finish = request.form.get('finish', type=float)
        crisp = request.form.get('crisp', type=float)
        leather = request.form.get('leather', type=float)
        wood = request.form.get('wood', type=float)
        smoke = request.form.get('smoke', type=float)
        citrus = request.form.get('citrus', type=float)
        floral = request.form.get('floral', type=float)
        fruit = request.form.get('fruit', type=float)
        logger.debug("adding rating of whiskey {} for user {}".format(whiskeyId, userId))
        return addRating(whiskeyId, userId, rating, notes, sweet, sour, heat, smooth, finish, crisp, leather, wood, smoke, citrus, floral, fruit)
    elif oper == 'edit':
        whiskeyId = request.form.get('whiskeyId', type=int)
        userId = request.form.get('userId', type=int)
        rating = request.form.get('rating', type=float)
        notes = request.form.get('notes', type=str)
        sweet = request.form.get('sweet', type=float)
        sour = request.form.get('sour', type=float)
        heat = request.form.get('heat', type=float)
        smooth = request.form.get('smooth', type=float)
        finish = request.form.get('finish', type=float)
        crisp = request.form.get('crisp', type=float)
        leather = request.form.get('leather', type=float)
        wood = request.form.get('wood', type=float)
        smoke = request.form.get('smoke', type=float)
        citrus = request.form.get('citrus', type=float)
        floral = request.form.get('floral', type=float)
        fruit = request.form.get('fruit', type=float)
        logger.debug("updating rating of whiskey {} for user {}".format(whiskeyId, userId))
        return updateRating(whiskeyId, userId, rating, notes, sweet, sour, heat, smooth, finish, crisp, leather, wood, smoke, citrus, floral, fruit)
    elif oper == 'del':
        whiskeyId = request.form.get('whiskeyId', type=int)
        userId = request.form.get('userId', type=int)
        logger.debug("deleting rating of whiskey {} for user {}".format(whiskeyId, userId))
        return deleteRating(whiskeyId, userId)
    else:
        logger.warn("Unsupported operation:{}".format(oper))
        return "Unsupported operation: {}".format(oper)

@admin.route('/whiskey/getAllRatings')
@require_token
@require_admin
def get_all_ratings():
    #logger.debug("Dump of args for get_all_ratings: %s", request.args)
    currentPage = request.args.get('page', 1, type=int)
    itemsPerPage = request.args.get('rows', 10, type=int)
    sortField = request.args.get('sort', None, type=str)
    #logger.info("Getting ratings page %d with %d items per page", currentPage, itemsPerPage)
    if itemsPerPage > 100:
        logger.warn("%d Items per page exceed max of 100, forcing to 100", itemsPerPage)
        itemsPerPage = 100
    return getAllRatings(currentPage, itemsPerPage, sortField)