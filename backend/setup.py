from setuptools import find_packages, setup

setup(
    name='sales_robo_backend',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-cors',
        'requests',
        'trading_calendars',
        'numpy',
        'pandas',
        'pystan',
        'fbprophet',
        'transformers',
        'torch',
        'scikit-learn',
        'statsmodels',
    ],
)