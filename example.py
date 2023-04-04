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
import time

if __name__ == "__main__":

    # create mechanism
    # mechanism = GaussianMechanism(var=)
    mechanism = LaplaceMechanism(original=False, eps=2.8, r=2.52, c=0.05)
    # configuration
    # use Logistic regression with stochastic gradient descent optimization as the underlying machine-learning algorithm
    classifier_factory = LogisticRegressionFactory(in_dimensions=1, optimizer_factory=SGDOptimizerFactory())
    # classifier_factory = MultiLayerPerceptronFactory(in_dimensions=1, optimizer_factory=SGDOptimizerFactory())
    # consider 1-dimensional floating point input pairs from the range [-10, 10] with maximum distance of 1
    input_generator = PatternGenerator(InputDomain(3, InputBaseType.FLOAT, [-10, 10]), False)
    # adapt the number of processes to fit your machine
    config = DDConfig(n_processes=2)

    s = time.time()

    with initialize_dpsniper(config, out_dir="example_outputs"):
        # run DD-Search to find the witness
        witness = DDSearch(mechanism, DPSniper(mechanism, classifier_factory, config), input_generator, config).run()
        # re-compute the power of the witness using high precision for a tighter lower confidence bound
        witness.compute_eps_high_precision(mechanism, config)

    print("eps_lcb = {}".format(witness.lower_bound))
    print("witness = ({}, {}, {})".format(witness.a1, witness.a2, witness.attack))

    e = time.time()
    print("time: ", e - s)

