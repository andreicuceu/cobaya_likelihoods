# Cobaya Likelihoods
External likelihoods for [Cobaya](https://github.com/CobayaSampler/cobaya).

## Ly $\alpha$ full-shape likelihood from eBOSS DR16 $\xi_\rm{3D}$
To use the likelihood with the full-shape results from [insert citation], first clone this repository:
```console
$ git clone https://github.com/andreicuceu/cobaya_likelihoods.git
```

After that, you can use the likelihood (found in the **lya_fullshape_xi3d.py** file) when running Cobaya by adding this to the **likelihood** section in a Cobaya yaml file:
```yaml
likelihood:
  lya_fullshape_xi3d.lya_fullshape_xi3d:
    python_path: path_to/cobaya_likelihoods/likelihoods
    alpha: _
    sig_alpha: _
    phi: _
    sig_phi: _
    correlation: _
```
See Equations 5 and 6 of [insert citation] for the definitions of **alpha** and **phi**, and the [Cobaya documentation](https://cobaya.readthedocs.io/en/latest/) for instructions on installing and using Cobaya.

### If you use this likelihood please cite [insert citation].
