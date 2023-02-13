#!python

import sys

import yaml
from jmon.runner import Runner


with open(sys.argv[1], "r") as fh:
    config = yaml.safe_load(fh)

check_runner = Runner()
print(config)
check_runner.perform_check(config)
