#!/bin/bash

coverage run --omit=/home/teamgoge/public_html/whiskey/api/lib/* -m test.testdb
coverage report -m

echo ""
echo ""

coverage run -m --omit=/home/teamgoge/public_html/whiskey/api/lib/* test.testfb
coverage report -m

