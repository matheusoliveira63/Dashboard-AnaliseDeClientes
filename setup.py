from setuptools import setup, find_packages

setup(
    name="analise_clientes",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'dash',
        'pandas',
        'plotly',
        'gunicorn'
    ],
)