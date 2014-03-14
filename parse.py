#!/usr/bin/env python

import sys
import yaml
import json

x = yaml.load(open(sys.argv[1]))
print json.dumps(x, indent=2)

