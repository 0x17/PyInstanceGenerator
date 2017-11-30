import json
import os
import random
from math import floor
import sys


def spit(fn, s):
    with open(fn, 'w') as fp:
        fp.write(s)


def rand_pair_incl(pair):
    lb, ub = pair
    return random.randint(lb, ub)


def generate_client(j, num_classes, capacity, revenue_cost_ratio):
    consumption_per_req = random.randint(1, floor(capacity / num_classes))
    x = random.uniform(0.5, 2.0)
    exp_D = (capacity / num_classes) / consumption_per_req * x
    var_coeff = 0.1 if bool(random.getrandbits(1)) else 0.3
    consumption_per_req_mean = consumption_per_req * 0.8
    var_coeff_consumption = 0.1 if bool(random.getrandbits(1)) else 0.3
    return {'description': 'Description for class ' + str(j + 1),
            'name': 'Class ' + str(j + 1),
            'revenuePerReq': revenue_cost_ratio * consumption_per_req,
            'expD': exp_D,
            'devD': exp_D * var_coeff,
            'consumptionPerReqMean': consumption_per_req_mean,
            'consumptionPerReqStdDev': consumption_per_req_mean * var_coeff_consumption}


def generate_instance(config):
    capacity = rand_pair_incl(config['capacity'])
    num_classes = rand_pair_incl(config['numClasses'])
    revenue_cost_ratios = sorted([random.uniform(0.0, 10.0) for j in range(num_classes)], reverse=True)
    clients = [generate_client(j, num_classes, capacity, revenue_cost_ratios[j]) for j in range(num_classes)]
    return {'capacity': capacity, 'clients': clients}


def generate_instances(config, num_instances):
    return [generate_instance(config) for _ in range(num_instances)]


def persist_instances(instances, out_path, prefix, suffix):
    for ctr in range(len(instances)):
        out_fn = out_path + os.sep + prefix + str(ctr + 1) + suffix
        spit(out_fn, json.dumps(instances[ctr], indent=4, sort_keys=True))


def args_to_obj(args):
    return {arg.split('=')[0]: arg.split('=')[1] for arg in args if '=' in arg}


def show_usage():
    print('Missing arguments, expected:')
    print('python spgenerator.py out_path=SomeDir prefix=instance suffix=.json')


def parse_or_default(fn, def_obj):
    if os.path.isfile(fn):
        with open(fn, 'r') as fp:
            return json.load(fp)
    return def_obj


def main(args):
    config = parse_or_default('config.json', {'numClasses': (4, 4), 'capacity': (20, 20)})
    instances = generate_instances(config, 3)
    print(json.dumps(instances, indent=4, sort_keys=True))
    arg_obj = args_to_obj(args)
    if all(k in arg_obj for k in ['out_path', 'prefix', 'suffix']):
        persist_instances(instances, arg_obj['out_path'], arg_obj['prefix'], arg_obj['suffix'])
    else:
        show_usage()


if __name__ == '__main__':
    main(sys.argv)
