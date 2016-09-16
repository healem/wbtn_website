#!/bin/bash

#coverage run --omit=/home/bythenum/public_html/whiskey/api/lib/* -m test.testdb
#coverage report -m

#echo ""
#echo ""

#coverage run -m --omit=/home/bythenum/public_html/whiskey/api/lib/* test.testfb
#coverage report -m

coverage run -m --omit=/home/bythenum/public_html/whiskey/api/lib/* test.testauth
coverage report -m
