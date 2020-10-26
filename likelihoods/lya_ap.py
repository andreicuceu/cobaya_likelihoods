from typing import Optional
from cobaya.likelihoods._base_classes import _bao_prototype
from cobaya.likelihood import Likelihood
import scipy.constants

class lya_ap(Likelihood):

    redshift: Optional[float]
    F_AP: Optional[float]
    sig_F_AP: Optional[float]

    def get_requirements(self):
        """
         return dictionary specifying quantities calculated by a theory code are needed
        """
        reqs = {"angular_diameter_distance": {"z": [self.redshift]},
                "Hubble": {"z": [self.redshift]}}
        
        return reqs

    def logp(self, **params_values):
        """
        Taking a dictionary of (sampled) nuisance parameter values params_values
        and return a log-likelihood.
        """
        da = self.provider.get_angular_diameter_distance(self.redshift)[0]
        hubble = self.provider.get_Hubble(self.redshift, units="km/s/Mpc")[0]
        c = scipy.constants.c / 1000
        F_AP = (1 + self.redshift) * da * hubble / c

        chi2 = (F_AP - self.F_AP)**2 / self.sig_F_AP**2
        return -chi2 / 2