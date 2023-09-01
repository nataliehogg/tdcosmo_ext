import os
import pickle
from cobaya.likelihood import Likelihood
from hierarc.Likelihood.lens_sample_likelihood import LensSampleLikelihood


class TDCOSMO(Likelihood):

    def initialize(self, datasets='TDCOSMO7', num_distribution_draws=200):
        """
         In this function we load the TDCOSMO and SLACS data and get the likelihood from hierArc.

        """
        dir_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')

        self.datasets = datasets 
        self.num_distribution_draws = num_distribution_draws

        print(datasets)

        # 7 TDCOSMO lenses
        tdcosmo_file = open(os.path.join(dir_path, 'tdcosmo7_likelihood_processed.pkl'), 'rb')
        tdcosmo7_likelihood_processed = pickle.load(tdcosmo_file)

        # 33 SLACS lenses with SDSS spectroscopy
        slacs_sdss_file =  open(os.path.join(dir_path, 'slacs_sdss_likelihood_processed.pkl'), 'rb')
        slacs_sdss_likelihood_processed = pickle.load(slacs_sdss_file)

        # 5 SLACS lenses with IFU
        slacs_ifu_file = open(os.path.join(dir_path, 'slacs_ifu_likelihood_processed.pkl'), 'rb')
        slacs_ifu_likelihood_processed = pickle.load(slacs_ifu_file)

        # here we update each individual lens likelihood configuration 
        # with the setting of the Monte-Carlo marginalisation over hyper-parameter distributions
        for lens in tdcosmo7_likelihood_processed:
            lens['num_distribution_draws'] = self.num_distribution_draws
        for lens in slacs_sdss_likelihood_processed:
            lens['num_distribution_draws'] = self.num_distribution_draws
        for lens in slacs_ifu_likelihood_processed:
            lens['num_distribution_draws'] = self.num_distribution_draws

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

        In our case, since we need to define an external Cosmo class, we have to use the full CAMBdata object.
        This is non-ideal, as it ties the likelihood to CAMB as the theory code. A more general implementation would use
        self.provider.get_angular_diameter_distance(), but the hierarc likelihood requires the cosmo object.

        :return: requirements_dictionary
        :rtype: dict

        """

        requirements_dictionary = {'CAMBdata': None}

        return requirements_dictionary

    def logp(self, **param_values):
        """
        Take a dictionary of (sampled) nuisance parameter values param_values
        and return a log-likelihood.

        """

        # get the camb results
        camb_results = self.provider.get_CAMBdata()

        # get an instance of the Cosmo class (defined below) using the camb results
        cosmo = Cosmo(camb_results)

        # get the likelihood from hierarc
        self._likelihood = LensSampleLikelihood(self.lens_list)

        print(param_values)

        # nuisance parameters required to evaluate the likelihood in accordance with TDCOSMO IV Table 3
        lambda_mst = param_values['lambda_mst']              # mean in the internal MST distribution
        lambda_mst_sigma = param_values['lambda_mst_sigma']  # Gaussian sigma of the distribution of lambda_mst
        alpha_lambda = param_values['alpha_lambda']          # slope of lambda_mst with r_eff/theta_E
        a_ani = param_values['a_ani']                        # mean a_ani anisotropy parameter in the OM model
        a_ani_sigma = param_values['a_ani_sigma']            # sigma(a_ani)⟨a_ani⟩ is the 1-sigma Gaussian scatter in a_ani

        kwargs_lens_test = {'lambda_mst': lambda_mst, 'lambda_mst_sigma': lambda_mst_sigma, 'alpha_lambda': alpha_lambda}

        kwargs_kin_test = {'a_ani': a_ani,'a_ani_sigma': a_ani_sigma}

        # kwargs_lens_test = {'lambda_mst': 1.0, 'lambda_mst_sigma': 0.1, 'alpha_lambda': 0.0}

        # kwargs_kin_test = {'a_ani': 1.0,'a_ani_sigma': 0.1}

        print(kwargs_lens_test)

        # get the log-likelihood from hierarc
        loglike = self._likelihood.log_likelihood(cosmo=cosmo, kwargs_lens=kwargs_lens_test, kwargs_kin=kwargs_kin_test)

        return loglike


class Cosmo:
    """
    Basic cosmology class which uses CAMB instead of astropy to get angular diameter distances.

    Note: hierarc expects angular diameter distance functions with the attribute .value, 
    whereas CAMB provides the float value directly without units. Hierarc has been modified to account for this.

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
    
    def angular_diameter_distance_z1z2(self, z1, z2):
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
