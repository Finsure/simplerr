#!/bin/sh

echo "change working directory to project root"
cd $(git rev-parse --show-toplevel)

echo "activiating env - you need to have this already"
source env/bin/activate

echo "runnings server - you should also have run pip install -r req..."
python manage.py runserver --site examples/01.kitchen_sink
