#!/bin/sh
python3 -m pylint --rcfile=.pylintrc *.py > report_code_quality.txt
