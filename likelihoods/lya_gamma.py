from typing import Optional
from cobaya.likelihoods._base_classes import _bao_prototype
from cobaya.likelihood import Likelihood
import scipy.constants
import numpy as np

class lya_gamma(Likelihood):

    redshift: Optional[float]
    gamma: Optional[float]
    sig_gamma: Optional[float]
    bao: Optional[bool]

    def get_requirements(self):
        """
         return dictionary specifying quantities calculated by a theory code are needed
        """
        reqs = {"angular_diameter_distance": {"z": [self.redshift]},
                "Hubble": {"z": [self.redshift]},
                "rdrag": None}
        
        return reqs

    def logp(self, **params_values):
        """
        Taking a dictionary of (sampled) nuisance parameter values params_values
        and return a log-likelihood.
        """
        da = self.provider.get_angular_diameter_distance(self.redshift)[0]
        hubble = self.provider.get_Hubble(self.redshift, units="km/s/Mpc")[0]
        c = scipy.constants.c / 1000
        
        dm = (1 + self.redshift) * da
        dh = c / hubble
        
        if self.bao:
            rd = self.provider.get_param("rdrag")
            gamma = np.sqrt(dm * dh / rd**2)
        else:
            gamma = np.sqrt(dm * dh)

        chi2 = (gamma - self.gamma)**2 / self.sig_gamma**2
        return -chi2 / 2