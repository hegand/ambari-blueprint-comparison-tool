# -*- coding: utf-8 -*-

import json
import os
import copy
import difflib
import argparse


def flat_traverse(path, d, res):
    # Ignores list location and order!!!
    # DO NOT USE with host_groups key!!!
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict) or isinstance(v, list):
                flat_traverse("{0}/{1}".format(path, k), v, res)
            else:
                res["{0}/{1}".format(path, k)] = "{0}".format(v)
    if isinstance(d, list):
        for item in d:
            if isinstance(item, dict) or isinstance(item, list):
                flat_traverse("{0}".format(path), item, res)
            else:
                res["{0}".format(path)] = "{0}".format(item)


def compare(left, right, ignore=False):
    keys=set().union(left['config'].keys(),right['config'].keys())
    d={}
    for k in keys:
        leftname = "{0}/{1}".format(k,left['name'])
        rightname = "{0}/{1}".format(k,right['name'])
        l = left['config'].setdefault(k,'')
        r = right['config'].setdefault(k,'')
        r1 = r.lower().replace(right['realm'].lower(),left['realm'].lower()).replace(right['name'].lower(), left['name'].lower()) if ignore else r
        l1 = l.lower() if ignore else l
        diff = '\n'.join(difflib.unified_diff(l1.splitlines(), r1.splitlines(), fromfile=leftname, tofile=rightname, lineterm=''))
        if diff:
            d0={}
            d0[left['name']]=left['config'][k]
            d0[right['name']]=right['config'][k]
            d0['diff']='\n'.join(difflib.unified_diff(l.splitlines(), r.splitlines(), fromfile=leftname, tofile=rightname, lineterm='')) if ignore else diff
            d[k]=d0
    return d


def get_realm(d):
    res = ''
    try:
        if d['/Blueprints/security/type'].lower()=='kerberos':
            res = d['/configurations/cluster-env/properties/ambari_principal_name'].split("@")[1]
    finally:
        return res


def get_name(d):
    res = ''
    try:
        if d['/Blueprints/security/type'].lower()=='kerberos':
            res = d['/configurations/cluster-env/properties/ambari_principal_name'].split("@")[0].split('-')[-1]
    finally:
        return res


def main():
    parser = argparse.ArgumentParser(description='Create diff from blueprint')
    parser.add_argument('-l', '--left', metavar='left.json', dest='left', help='left side blueprint', required=True)
    parser.add_argument('-r', '--right', metavar='right.json', dest='right', help='right side blueprint', required=True)

    options = parser.parse_args()

    d1 = json.loads(open(options.left, 'r').read())
    d2 = json.loads(open(options.right, 'r').read())

    del d1['host_groups']
    del d2['host_groups']

    r1={}
    r2={}

    flat_traverse('', d1, r1)
    flat_traverse('', d2, r2)

    left = {}
    left['name'] = get_name(r1) if get_name(r1) else os.path.basename(i1).split('.')[0]
    left['realm'] = get_realm(r1)
    left['config'] = r1

    right = {}
    right['name'] = get_name(r2) if get_name(r2) else os.path.basename(i2).split('.')[0]
    right['realm'] = get_realm(r2)
    right['config'] = r2

    res = compare(copy.deepcopy(left), copy.deepcopy(right), right['name'] and right['realm'] and left['name'] and left['realm'])
    #print(json.dumps(res, sort_keys=True, indent=4))

    for k in sorted(res.keys()):
        print(res[k]['diff'])


if __name__ == "__main__":
    main()