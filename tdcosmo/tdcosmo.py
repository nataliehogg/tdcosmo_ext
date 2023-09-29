import os
import pickle
import numpy as np
from cobaya.likelihood import Likelihood
from hierarc.Likelihood.lens_sample_likelihood import LensSampleLikelihood
from lenstronomy.Cosmo.cosmo_interp import CosmoInterp


class TDCOSMO(Likelihood):

    def initialize(self):
        """
         In this function we load the TDCOSMO and SLACS data.

        """

        dir_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')

        self.lens_list = []

        # 7 TDCOSMO lenses
        if self.tdcosmo_lenses is not None:
            print('Using TDCOSMO lenses')
            tdcosmo_data = open(os.path.join(dir_path, 'tdcosmo7_likelihood_processed.pkl'), 'rb')
            tdcosmo7_likelihood_processed = pickle.load(tdcosmo_data)
            for lens in tdcosmo7_likelihood_processed:
                lens['num_distribution_draws'] = self.num_distribution_draws
            self.lens_list += tdcosmo7_likelihood_processed
        else:
            print('TDCOSMO lenses not being used')

        # 33 SLACS lenses with SDSS spectroscopy
        if self.slacs_sdss_lenses is not None:
            print('Using SLACS SDSS lenses')
            slacs_sdss_data =  open(os.path.join(dir_path, 'slacs_sdss_likelihood_processed.pkl'), 'rb')
            slacs_sdss_likelihood_processed = pickle.load(slacs_sdss_data)
            for lens in slacs_sdss_likelihood_processed:
                lens['num_distribution_draws'] = self.num_distribution_draws
            self.lens_list += slacs_sdss_likelihood_processed
        else:
            print('SLACS SDSS lenses not being used')
        
        # 5 SLACS lenses with IFU
        if self.slacs_ifu_lenses is not None:
            print('Using SDSS IFU lenses')
            slacs_ifu_data = open(os.path.join(dir_path, 'slacs_ifu_likelihood_processed.pkl'), 'rb')
            slacs_ifu_likelihood_processed = pickle.load(slacs_ifu_data)
            for lens in slacs_ifu_likelihood_processed:
                lens['num_distribution_draws'] = self.num_distribution_draws
            self.lens_list += slacs_ifu_likelihood_processed
        else:
            print('SLACS IFU lenses not being used')
        
        if len(self.lens_list) == 0:
            raise ValueError('You haven\'t loaded any data!')
        else:
            pass
        
    def get_requirements(self):
        """
        This function specifies the quantities we need to be calculated by the theory code.

        We need a set of angular diameter distances which will be interpolated by CosmoInterp(),
        Omega_k and H0.

        :return: requirements_dictionary
        :rtype: dict

        """

        self.zlist = np.linspace(0, 5, 100) # list of redshifts for which angular diameter distances will be computed

        requirements_dictionary = {'angular_diameter_distance': {'z': self.zlist}, 
                                   'omk': None,
                                   'H0': None}

        return requirements_dictionary

    def logp(self, **params_values):
        """
        This function takes a dictionary of (sampled) nuisance parameter values and returns the log-likelihood.

        :param params_values: dictionary of nuisance parameters
        :return: loglike

        """

        DA = self.provider.get_angular_diameter_distance(self.zlist) # angular diameter distances of the redshifts in zlist

        omega_k = self.provider.get_param('omk') # spatial curvature density

        H0 = self.provider.get_param('H0') # Hubble parameter in km/s/Mpc

        c = 299792 # speed of light in km/s

        K = omega_k*(c**2/H0**2) # dimensionless spatial curvature

        cosmo = CosmoInterp(ang_dist_list = DA, z_list = self.zlist, Ok0=omega_k, K=K) # get the cosmo object for hierarc

        # initialise the likelihood from hierarc for the lenses in lens_list
        self._likelihood = LensSampleLikelihood(self.lens_list)

        # nuisance parameters required to evaluate the likelihood in accordance with TDCOSMO IV Table 3
        lambda_mst = params_values['lambda_mst']              # mean in the internal MST distribution
        lambda_mst_sigma = params_values['lambda_mst_sigma']  # Gaussian sigma of the distribution of lambda_mst
        alpha_lambda = params_values['alpha_lambda']          # slope of lambda_mst with r_eff/theta_E
        a_ani = params_values['a_ani']                        # mean a_ani anisotropy parameter in the OM model
        a_ani_sigma = params_values['a_ani_sigma']            # sigma(a_ani)⟨a_ani⟩ is the 1-sigma Gaussian scatter in a_ani

        kwargs_lens_test = {'lambda_mst': lambda_mst, 'lambda_mst_sigma': lambda_mst_sigma, 'alpha_lambda': alpha_lambda}

        kwargs_kin_test = {'a_ani': a_ani,'a_ani_sigma': a_ani_sigma}

        # get the log-likelihood from hierarc
        loglike = self._likelihood.log_likelihood(cosmo=cosmo, kwargs_lens=kwargs_lens_test, kwargs_kin=kwargs_kin_test)

        return loglike