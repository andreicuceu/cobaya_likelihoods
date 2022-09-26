from cobaya.likelihood import Likelihood
import scipy.constants
import numpy as np


class lya_fullshape_xi3d(Likelihood):
    """Lyman-alpha analysis for Xi3D compressed full-shape parameters
    alpha = sqrt(D_M * D_H / r_d^2) / sqrt(D_M * D_H / r_d^2)_fiducial
    phi = D_M * D_H / [D_M * D_H]_fiducial
    See equations 6 and 7 of Cuceu et al. 2021 (https://arxiv.org/pdf/2103.14075.pdf)
    """

    redshift: float = 2.334
    alpha: float = 1.
    sig_alpha: float = 0.01
    phi: float = 1.
    sig_phi: float = 0.02
    correlation: float = 0.209

    DM_fid: float = 5776.02  # In Mpc
    DH_fid: float = 1267.23  # In Mpc
    rd_fid: float = 147.334  # In Mpc

    speed: float = 500

    def initialize(self):
        # Initizalize the data vector
        self.data = np.array([self.alpha, self.phi])

        # Compute the correlation term
        cross_term = self.correlation * self.sig_alpha * self.sig_phi

        # Initialize the covariance matrix and compute its inverse
        self.cov = np.array([[self.sig_alpha**2, cross_term], [cross_term, self.sig_phi**2]])
        self.inv_cov = np.linalg.inv(self.cov)

    def get_requirements(self):
        """Return dictionary specifying quantities calculated by a theory code are needed
        """
        reqs = {"angular_diameter_distance": {"z": [self.redshift]},
                "Hubble": {"z": [self.redshift]},
                "rdrag": None}

        return reqs

    def logp(self, **params_values):
        """Taking a dictionary of (sampled) nuisance parameter values params_values
        and return a log-likelihood.
        """
        # Get distances from Cobaya
        rd = self.provider.get_param("rdrag")
        DA = self.provider.get_angular_diameter_distance(self.redshift)[0]
        hubble = self.provider.get_Hubble(self.redshift, units="km/s/Mpc")[0]
        c = scipy.constants.c / 1000

        # Compute DM and DH
        DM = (1 + self.redshift) * DA
        DH = c / hubble

        # Compute alpha and phi (Eq 6 and 7 of 2103.14075)
        alpha = np.sqrt(DM * DH / rd**2) / np.sqrt(self.DM_fid * self.DH_fid / self.rd_fid**2)
        phi = DM / DH / (self.DM_fid / self.DH_fid)

        # Compute the chi^2
        theory = np.array([alpha, phi])
        diff = theory - self.data
        chi2 = diff.T.dot(self.inv_cov.dot(diff))

        return -chi2 / 2
