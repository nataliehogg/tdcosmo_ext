from setuptools import setup

setup(
    name='tdcosmo',
    version='0.1',
    description='TDCOSMO likelihood',
    url="https://github.com/nataliehogg/tdcosmo_ext",
    author='Original likelihood by Simon Birrer; packaged for Cobaya by Natalie B. Hogg',
    python_requires='>=3',
    install_requires=['hierarc', 'lenstronomy'],
    packages=['tdcosmo'],
    include_package_data=True,
)
