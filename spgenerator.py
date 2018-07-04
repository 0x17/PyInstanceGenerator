import json
import os
import random
from math import floor
import sys
from utils import spit, args_to_obj, parse_or_default, rand_pair_incl, val_or_else, enforce_directory, twice

random.seed(42)


def generate_client_normal_demands(j, num_classes, capacity, revenue_cost_ratios):
    stochastic_consumptions = False
    consumption_per_req = random.randint(1, floor(capacity / num_classes))
    exp_D = floor(capacity / consumption_per_req) * random.uniform(0.5, 1.0) * ((j+1) / 3)
    var_coeff = random.uniform(0.1, 0.5)

    consumption_per_req_mean = consumption_per_req * 0.8
    var_coeff_consumption = 0.1 if bool(random.getrandbits(1)) else 0.3

    base_obj = {'description': 'Description for class ' + str(j + 1),
                'name': 'Class ' + str(j + 1),
                'revenuePerReq': revenue_cost_ratios[j] * consumption_per_req,
                'expD': exp_D,
                'devD': exp_D * var_coeff,
                }
    stoch_obj = {'consumptionPerReqMean': consumption_per_req_mean,
                 'consumptionPerReqStdDev': consumption_per_req_mean * var_coeff_consumption}
    return {**base_obj, **(stoch_obj if stochastic_consumptions else {'consumptionPerReq': consumption_per_req})}


def generate_client_binomial_demands(j, num_classes, capacity, revenue_cost_ratios):
    consumption_per_req = random.randint(1, floor(capacity / num_classes))
    exp_D = floor(capacity / (num_classes * consumption_per_req)) * random.uniform(0.5, 2.0)
    n = int(floor(exp_D * random.uniform(1.0, 2.0)))
    return {'description': 'Description for class ' + str(j + 1),
            'name': 'Class ' + str(j + 1),
            'revenuePerReq': 1,
            'consumptionPerReq': consumption_per_req,
            'n': n,
            'p': exp_D / n}


def generate_instance(config, client_generator_func):
    capacity = rand_pair_incl(config['capacity'])
    num_classes = rand_pair_incl(config['numClasses'])
    revenue_cost_ratios = sorted([random.uniform(0.0, 10.0) for j in range(num_classes)], reverse=True)
    clients = [client_generator_func(j, num_classes, capacity, revenue_cost_ratios) for j in range(num_classes)]
    return {'capacity': capacity, 'clients': clients}


def generate_instances(config, num_instances, client_generator_func):
    return [generate_instance(config, client_generator_func) for instance_ix in range(num_instances)]


def persist_instances(instances, out_path, prefix, suffix):
    for ctr in range(len(instances)):
        out_fn = out_path + os.sep + prefix + str(ctr + 1) + suffix
        spit(out_fn, json.dumps(instances[ctr], indent=4, sort_keys=True))


def show_usage():
    print('Missing arguments, expected [with optionals]:')
    print('python spgenerator.py out_path=SomeDir prefix=instance suffix=.json [config=config.json] [num_instances=3] [dist=normal|binomial]')


def main(args):
    arg_obj = args_to_obj(args)
    client_gen_func = generate_client_binomial_demands if 'dist' in arg_obj and arg_obj['dist'] == 'binomial' else generate_client_normal_demands
    if all(k in arg_obj for k in ['out_path', 'prefix', 'suffix']):
        enforce_directory(arg_obj['out_path'])
        config = parse_or_default(val_or_else(arg_obj, 'config', 'config.json'), {'numClasses': twice(10), 'capacity': twice(60)})
        instances = generate_instances(config, int(val_or_else(arg_obj, 'num_instances', 10)), client_gen_func)
        persist_instances(instances, arg_obj['out_path'], arg_obj['prefix'], arg_obj['suffix'])
    else:
        show_usage()


if __name__ == '__main__':
    main(sys.argv)
