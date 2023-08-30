from setuptools import setup

setup(
    name='tdcosmo',
    version='0.1',
    description='TDCOSMO likelihood',
    url="https://github.com/nataliehogg/tdcosmo_ext",
    author='Cobaya extension by Natalie B. Hogg; original likelihood by Simon Birrer',
    python_requires='>=3',
    install_requires=['hierarc', 'pickle'],
    packages=['tdcosmo'],
    include_package_data=True,
)