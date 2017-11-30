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
    return [generate_instance(config) for i in range(num_instances)]


def persist_instances(instances, out_path, prefix, suffix):
    ctr = 1
    for instance in instances:
        out_fn = out_path + os.sep + prefix + str(ctr) + suffix
        spit(out_fn, json.dumps(instance, indent=4, sort_keys=True))
        ctr += 1


def main(args):
    config = {'numClasses': (4, 4), 'capacity': (20, 20)}
    instances = generate_instances(config, 3)
    print(json.dumps(instances, indent=4, sort_keys=True))
    # persist_instances(instances, 'output', 'pinstance', '.json')


if __name__ == '__main__':
    main(sys.argv)
