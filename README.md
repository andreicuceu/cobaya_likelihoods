# Cobaya Likelihoods
External likelihoods for [Cobaya](https://github.com/CobayaSampler/cobaya).

## Ly $\alpha$ full-shape likelihood from eBOSS DR16 $\xi_\rm{3D}$
To use the likelihood with the full-shape results from [Cuceu et al. 2022](https://arxiv.org/abs/2209.13942), first clone this repository:
```console
$ git clone https://github.com/andreicuceu/cobaya_likelihoods.git
```

After that, you can use the likelihood (found in the **lya_fullshape_xi3d.py** file) when running Cobaya by adding this to the **likelihood** section in a Cobaya yaml file:
```yaml
likelihood:
  lya_fullshape_xi3d.lya_fullshape_xi3d:
    python_path: path_to/cobaya_likelihoods/likelihoods
    alpha: 1.0167
    sig_alpha: 0.0135
    phi: 1.0206
    sig_phi: 0.0189
    correlation: 0.209
```
See Equations 5 and 6 of [Cuceu et al. 2022](https://arxiv.org/abs/2209.13942) for the definitions of **alpha** and **phi**, and the [Cobaya documentation](https://cobaya.readthedocs.io/en/latest/) for instructions on installing and using Cobaya.

### If you use this likelihood please cite [Cuceu et al. 2022](https://ui.adsabs.harvard.edu/abs/2022arXiv220913942C/abstract) (https://ui.adsabs.harvard.edu/abs/2022arXiv220913942C/exportcitation).
