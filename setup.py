from setuptools import setup, find_packages

setup(
    name='lingbuzz_scraper',
    version='0.1',
    author='Carlos Muñoz Pérez',
    author_email='cmunozperez@filo.uba.ar',
    description='This is a script to scrape data from lingbuzz.net',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.12.2',
        'pandas==1.4.2',
        'requests==2.27.1',
    ],
)