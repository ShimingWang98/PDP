from attack.dpsniper import DPSniper
from classifiers.classifier_factory import LogisticRegressionFactory, MultiLayerPerceptronFactory
from classifiers.torch_optimizer_factory import SGDOptimizerFactory
from search.ddconfig import DDConfig
from search.ddsearch import DDSearch
from input.input_domain import InputDomain, InputBaseType
from input.pattern_generator import PatternGenerator
from mechanisms.laplace import LaplaceMechanism
from mechanisms.gaussian import GaussianMechanism
from utils.initialization import initialize_dpsniper

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--original_laplace', default=0, type=bool)
parser.add_argument('--eps', default=2.8, type=float)
parser.add_argument('--r', default=2.52, type=float)
# c of the attacker
parser.add_argument('--c_prime', default=0.1, type=float)
# whether the attacker uses given number of samples(N!=0) or follows the guideline 1(N==0)
parser.add_argument('--N', default=0, type=int)
# whether to compare practical laplace mechanism and gaussian mechanism with the same utility(variance)
parser.add_argument('--compare_gaussian', default=0, type=bool)
args = parser.parse_args()

if __name__ == "__main__":

    # create mechanism
    laplace_mechanism = LaplaceMechanism(original=args.original_laplace, eps=args.eps, r=args.r)
    utility = laplace_mechanism.test_utility()
    # configuration
    # use Logistic regression with stochastic gradient descent optimization as the underlying machine-learning algorithm
    classifier_factory = LogisticRegressionFactory(in_dimensions=1, optimizer_factory=SGDOptimizerFactory())
    # classifier_factory = MultiLayerPerceptronFactory(in_dimensions=1, optimizer_factory=SGDOptimizerFactory())
    # consider 1-dimensional floating point input pairs from the range [-10, 10] with maximum distance of 1
    input_generator = PatternGenerator(InputDomain(3, InputBaseType.FLOAT, [-10, 10]), False)
    # adapt the number of processes to fit your machine
    config = DDConfig(c=args.c_prime, N=args.N, n_processes=2)

    # use dp-sniper to attack Laplace mechanism
    print("Using dp-sniper to attack Laplace mechanism")
    with initialize_dpsniper(config, out_dir="example_outputs"):
        # run DD-Search to find the witness
        witness1 = DDSearch(laplace_mechanism, DPSniper(laplace_mechanism, classifier_factory, config), input_generator, config).run()
        # re-compute the power of the witness using high precision for a tighter lower confidence bound
        witness1.compute_eps_high_precision(laplace_mechanism, config)

    print("laplace_eps_lcb = {}".format(witness1.lower_bound))
    print("witness = ({}, {}, {})".format(witness1.a1, witness1.a2, witness1.attack))


    if args.compare_gaussian:
        # the gaussian mechanism has the same variance of the practical laplace mechanism
        gaussian_mechanism = GaussianMechanism(var=utility)

        # use dp-sniper to attack Gaussian mechanism
        print("Using dp-sniper to attack Gaussian mechanism")
        with initialize_dpsniper(config, out_dir="example_outputs"):
            # run DD-Search to find the witness
            witness2 = DDSearch(gaussian_mechanism, DPSniper(gaussian_mechanism, classifier_factory, config), input_generator, config).run()
            # re-compute the power of the witness using high precision for a tighter lower confidence bound
            witness2.compute_eps_high_precision(gaussian_mechanism, config)

        print("laplace_eps_lcb = {}".format(witness2.lower_bound))
        print("witness = ({}, {}, {})".format(witness2.a1, witness2.a2, witness2.attack))


