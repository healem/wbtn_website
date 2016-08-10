#!/bin/bash

coverage run -m test.testdb
coverage report -m

echo ""
echo ""

coverage run -m test.testfb
coverage report -m

