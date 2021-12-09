
# prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
root = path.dirname(here)

readme = path.join(here, 'README.md')

# long description from README file
with open(readme, encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'ftkafinance',         # How you named your package folder (MyLib)
  packages = ['ftkafinance'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license ='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'a finance Python package for easy to use collecting and analyzing market data',   # Give a short description about your library
  long_description = long_description,
  author = 'hamednikseresht',                   # Type in your name
  author_email = 'hamednikseresht@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/hamednikseresht/ftkafinance',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hamednikseresht/ftkafinance/archive/refs/tags/v1.0.tar.gz',    # I explain this later on
  keywords = ['FTKAFINANCE', 'CRYPTO', 'CRYPTOCURRENCY'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'pandas',
          'python-dotenv',
          'pymongo',
          'json',
      ],
  classifiers=[
    "Programming Language :: Python :: 3",      #Specify which pyhton versions that you want to support
    "License :: OSI Approved :: MIT License",   # Again, pick a license
    "Operating System :: OS Independent",
  ],
)