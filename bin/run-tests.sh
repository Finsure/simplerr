cd $(git rev-parse --show-toplevel)

fswatch --exclude 4913 . | while read f; do echo $f; clear; tests/run.py; done
