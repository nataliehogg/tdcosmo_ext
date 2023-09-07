# TDCOSMO likelihood for Cobaya

This package provides the TDCOSMO likelihood as an external package for [Cobaya](https://cobaya.readthedocs.io/en/latest/index.html). The hierarchical computation of the likelihood uses the [hierArc](https://hierarc.readthedocs.io/en/latest/) package along with [lenstronomy](https://lenstronomy.readthedocs.io/en/latest/). An example notebook is included demonstrating how to use this likelihood package with Cobaya.

## Requirements
 * hierArc -- clone from [repo](https://github.com/sibirrer/hierArc)
 * lenstronomy >= 1.1.3 -- install with `pip` or clone from [repo](https://github.com/lenstronomy/lenstronomy/tree/main)

## References

[Birrer et al.](https://arxiv.org/abs/2007.02941), TDCOSMO IV: Hierarchical time-delay cosmography -- joint
inference of the Hubble constant and galaxy density profiles, A&A 2020.
