# TDCOSMO likelihood for Cobaya

This package provides the TDCOSMO likelihood as an external package for [Cobaya](https://cobaya.readthedocs.io/en/latest/index.html). The hierarchical computation of the likelihood uses the [hierArc](https://hierarc.readthedocs.io/en/latest/) package along with [lenstronomy](https://lenstronomy.readthedocs.io/en/latest/). An example notebook is included demonstrating how to use the package.

⚠️ The velocity dispersions of the SLACS lenses measured by SDSS using single-aperture spectroscopy have recently been shown to exhibit bias compared to IFU spectra obtained from Keck ([Knabel et al. 2024](https://arxiv.org/abs/2409.10631)). This bias will propagate to cosmological inference if these data are included in the analysis (`tdcosmo/data/slacs_sdss_likelihood_processed.pkl` in this repository). For this reason, I recommend **avoiding the use of this likelihood**. The likelihoods derived from the time delay data and from IFU-measured kinematics for nine of the SLACS lenses are safe to use (`tdcosmo/data/tdcosmo7_likelihood_processed.pkl` and `tdcosmo/data/slacs_ifu_likelihood_processed.pkl` respectively). This repository will be updated with any future likelihood for IFU-measured kinematics when so provided by the TDCOSMO collaboration.

## Requirements
 * hierArc: clone from [repo](https://github.com/sibirrer/hierArc)
 * lenstronomy >= 1.1.3: install with `pip` or clone from [repo](https://github.com/lenstronomy/lenstronomy/tree/main)

## References

[Birrer et al. (2020)](https://arxiv.org/abs/2007.02941). TDCOSMO IV: Hierarchical time-delay cosmography –
joint inference of the Hubble constant and galaxy density profiles, Astronomy & Astrophysics, 643, A165, November 2020.

```
@article{Birrer:2020tax,
    author = "Birrer, S. and others",
    title = "{TDCOSMO - IV. Hierarchical time-delay cosmography \textendash{} joint inference 
              of the Hubble constant and galaxy density profiles}",
    eprint = "2007.02941",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    doi = "10.1051/0004-6361/202038861",
    journal = "Astronomy \& Astrophysics",
    volume = "643",
    pages = "A165",
    year = "2020"
}
```

[Hogg (2024)](https://arxiv.org/abs/2310.11977). Constraints on dark energy from TDCOSMO & SLACS lenses, Monthly Notices of the Royal Astronomical Society: Letters, 528, 1, March 2024.

```
@article{Hogg:2023khs,
    author = "Hogg, Natalie B.",
    title = "{Constraints on dark energy from TDCOSMO~\& SLACS lenses}",
    eprint = "2310.11977",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    doi = "10.1093/mnrasl/slae005",
    journal = "Monthly Notices of the Royal Astronomical Society: Letters",
    volume = "528",
    number = "1",
    pages = "L95--L100",
    year = "2024"
}
```
