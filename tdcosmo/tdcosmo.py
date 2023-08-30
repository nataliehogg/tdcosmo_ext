from cobaya.likelihood import Likelihood
from hierarc.Likelihood.lens_sample_likelihood import LensSampleLikelihood
import os
import pickle

class TDCOSMO(Likelihood):

    def initialize(self, datasets='TDCOSMO7', num_distribution_draws=200):
        """
         In this function we load the TDCOSMO and SLACS data and get the likelihood from hierArc.

        """

        # NH: todo: add some checks
        self.datasets = datasets 
        self._num_distribution_draws = num_distribution_draws

        # 7 TDCOSMO lenses
        tdcosmo7_likelihood_processed = pickle.load(self.tdcosmo_file)

        # 33 SLACS lenses with SDSS spectroscopy
        slacs_sdss_likelihood_processed = pickle.load(self.slacs_sdss_file)

        # 5 SLACS lenses with IFU
        slacs_ifu_likelihood_processed = pickle.load(self.slacs_ifu_file)

        # here we update each individual lens likelihood configuration 
        # with the setting of the Monte-Carlo marginalisation over hyper-parameter distributions
        for lens in tdcosmo7_likelihood_processed:
            lens['num_distribution_draws'] = self._num_distribution_draws
        for lens in slacs_sdss_likelihood_processed:
            lens['num_distribution_draws'] = self._num_distribution_draws
        for lens in slacs_ifu_likelihood_processed:
            lens['num_distribution_draws'] = self._num_distribution_draws

        self.lens_list = []
        if 'TDCOSMO7' in self.datasets:
            self.lens_list += tdcosmo7_likelihood_processed
        if 'SLACS_SDSS' in self.datasets:
            self.lens_list += slacs_sdss_likelihood_processed
        if 'SLACS_IFU' in self.datasets:
            self.lens_list += slacs_ifu_likelihood_processed


    def get_requirements(self):
        """
        This function specifies the quantities we need to be calculated by the theory code.

        :return: requirements_dictionary
        :rtype: dict
        """

        requirements_dictionary = {}

        requirements_dictionary['CAMBdata'] = None # get the CAMB results (?)

        return requirements_dictionary

    def logp(self, **param_values):
        """
        Take a dictionary of (sampled) nuisance parameter values params_values
        and return a log-likelihood.
        """

        # get the camb results
        camb_results = self.provider.get_CAMBdata()

        # get an instance of the Cosmo class (defined below) using the camb results
        cosmo = Cosmo(camb_results)

        # get the likelihood from hierarc
        self._likelihood = LensSampleLikelihood(self.lens_list)

        # nuisance parameters required to evaluate the likelihood in accordance with TDCOSMO IV Table 3
        lambda_mst = param_values['lambda_mst']             # mean in the internal MST distribution
        lambda_mst_sigma = param_values['lambda_mst_sigma'] # Gaussian sigma of the distribution of lambda_mst
        alpha_lambda = param_values['alpha_lambda']         # slope of lambda_mst with r_eff/theta_E
        a_ani = param_values['a_ani']                       # mean a_ani anisotropy parameter in the OM model
        a_ani_sigma = param_value['a_ani_sigma']            # sigma(a_ani)⟨a_ani⟩ is the 1-sigma Gaussian scatter in a_ani

        kwargs_lens_test = {'lambda_mst': lambda_mst, 'lambda_mst_sigma': lambda_mst_sigma, 'alpha_lambda': alpha_lambda}

        kwargs_kin_test = {'a_ani': a_ani,'a_ani_sigma': a_ani_sigma}

        # get the log-likelihood from hierarc
        loglike = self._likelihood.log_likelihood(cosmo=cosmo, kwargs_lens=kwargs_lens_test, kwargs_kin=kwargs_kin_test)

        return loglike


class Cosmo:
    """
    Basic cosmology class which uses CAMB results instead of astropy to get angular diameter distances.
    """

    def __init__(self, camb_results):

        self.camb_results = camb_results

    def angular_diameter_distance(self, z):
        """
        This function returns the angular diameter distance to a redshift.

        :param camb_results: CAMB results object
        :param z: the redshift
        :returns: the angular diameter distance in Mpc
        :rtype: float 
        """

        DA = self.camb_results.angular_diameter_distance(z)

        return DA
    
    def angular_diameter_distance2(self, z1, z2):
        """
        This function returns the angular diameter distance between two redshifts.

        :param camb_results: CAMB results object
        :param z1: first redshift
        :param z2: second redshift
        :returns: the angular diameter distance in Mpc
        :rtype: float 
        """

        DA = self.camb_results.angular_diameter_distance2(z1, z2)

        return DA