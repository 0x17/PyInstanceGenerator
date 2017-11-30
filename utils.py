import os
import json
import random


def val_or_else(dict, key, otherwise):
    return otherwise if key not in dict else dict[key]


def parse_or_default(fn, def_obj):
    if os.path.isfile(fn):
        with open(fn, 'r') as fp:
            return json.load(fp)
    return def_obj


def args_to_obj(args):
    return {arg.split('=')[0]: arg.split('=')[1] for arg in args if '=' in arg}


def spit(fn, s):
    with open(fn, 'w') as fp:
        fp.write(s)


def rand_pair_incl(pair):
    lb, ub = pair
    return random.randint(lb, ub)


def enforce_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)
