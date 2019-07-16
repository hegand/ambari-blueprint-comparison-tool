#!/usr/bin/env bash

PROJECT_HOME="${PROJECT_HOME:=$(pwd)}"

python $PROJECT_HOME/src/process_blueprints.py -r right.json -l left.json | diff2html -i stdin -s side -F $PROJECT_HOME/out/out.html