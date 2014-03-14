#!/usr/bin/env python

import os
import re
import sys
import codecs
import json
import yaml

from urllib import urlopen

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def projects():
    url = 'http://digital2.library.unt.edu/nomination/'
    html = urlopen(url).read()
    for match in re.finditer('<a href="/nomination/(.+?)/">', html):
        yield match.group(1)


def write_dump(project):
    dump_url = 'http://digital2.library.unt.edu/nomination/' + project + '/reports/projectdump/'
    r = urlopen(dump_url)
    if r.code == 200:
        json_file = '%s.json' % project
        j = json.loads(urlopen(dump_url).read())
        open(json_file, 'w').write(json.dumps(j, indent=2))
        print 'got %s' % json_file


def write_yaml(project, data):
    seeds = []
    yaml_file = '%s.yaml' % project
    for url, seed_info in data.items():
        seed = {
            'url': url,
            'nominators': []
        }
        for nominator in seed_info['nominators']:
            person, institution = nominator.split(' - ', 1)
            seed['nominators'].append({
                'name': person,
                'institution': institution
            })
        for key, vals in seed_info['attributes'].items():
            key = key.replace('_', ' ').lower()
            if len(vals) == 1:
                seed[key] = vals[0]
            else:
                seed[key] = vals
        seeds.append(seed)
    yaml.safe_dump(seeds, open(yaml_file, 'w'), default_flow_style=False)
    print yaml_file

def main():
    #for project in projects():
    #    write_dump(project)
    for f in os.listdir("."):
        parts = f.split(".")
        if len(parts) != 2:
            continue
        if parts[1] == "json":
            j = json.loads(open(f).read())
            write_yaml(parts[0], j)


if __name__ == "__main__":
    main()

