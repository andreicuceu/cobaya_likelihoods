from typing import Optional
from cobaya.likelihoods._base_classes import _bao_prototype
from cobaya.likelihood import Likelihood
import numpy as np
from scipy.interpolate import RectBivariateSpline
import scipy.constants

class lya_bao(Likelihood):

    path: str
    redshift: Optional[float]
    DA_over_rs_fid: Optional[float]
    c_over_Hz_rs_fid: Optional[float]

    def initialize(self):
        """
         Prepare any computation, importing any necessary code, files, etc.
        """
        data = np.loadtxt(self.path)

        at = np.array(sorted(set(data[:,0])))
        ap = np.array(sorted(set(data[:,1])))

        N_at = at.shape[0]
        N_ap = ap.shape[0]
        grid = np.zeros((N_at,N_ap))

        for i in range(N_ap):
            # Filter the data to only those corresponding to the ap value.
            indices = (data[:,1] == ap[i])
            scan_chunk = data[indices, :]

            # Ensure that they're sorted by at value.
            scan_chunk = scan_chunk[scan_chunk[:,0].argsort()]
            
            # Add the chi2 column to the grid.
            # Note that the grid is of shape (N_at,N_ap)
            grid[:,i] = scan_chunk[:,2]

        #Make the interpolator (x refers to at, y refers to ap).
        self.interpolator = RectBivariateSpline(at, ap, grid, kx=1, ky=1)

    def get_requirements(self):
        """
         return dictionary specifying quantities calculated by a theory code are needed
        """
        reqs = {"angular_diameter_distance": {"z": [self.redshift]},
                "rdrag": None,
                "Hubble": {"z": [self.redshift]}}
        
        return reqs

    def logp(self, **params_values):
        """
        Taking a dictionary of (sampled) nuisance parameter values params_values
        and return a log-likelihood.

        e.g. here we calculate chi^2  using cls['tt'], H0_theory, my_foreground_amp
        """
        rd = self.provider.get_param("rdrag")
        da = self.provider.get_angular_diameter_distance(self.redshift)
        hubble = self.provider.get_Hubble(self.redshift, units="km/s/Mpc")
        c = scipy.constants.c / 1000
        at = (da / rd) / self.DA_over_rs_fid
        ap = (c / (hubble * rd)) / self.c_over_Hz_rs_fid

        chi2 = float(self.interpolator(at, ap)[0])
        return -chi2 / 2