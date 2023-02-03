#!python

import sys

import yaml
from jmon.runner import Runner


with open(sys.argv[1], "r") as fh:
    config = yaml.load(fh, yaml.FullLoader)

check_runner = Runner()
print(config)
check_runner.perform_check(config)
