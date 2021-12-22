
# prefer setuptools over distutils
from setuptools import setup

# long description
with open(file='README.md', encoding='utf-8', mode='r') as text:
    long_description = text.read()

setup(
    # How you named your package folder (MyLib)
    name='ftkafinance',

    # Chose the same as "name"
    packages=['src.ftkafinance'],

    # Start with a small number and increase it with every change you make
    # Define the version of this library.
    # Read this as
    #   - MAJOR VERSION 1
    #   - MINOR VERSION 0
    #   - MAINTENANCE VERSION 0
    version='1.0.0',

    # Chose a license from here:
    # https://help.github.com/articles/licensing-a-repository
    license='MIT',

    # Give a short description about your library
    description='a finance Python package for easy \
      to use collecting and analyzing market data',

    # long description
    long_description=long_description,

    # long description type
    long_description_content_type='text/markdown',

    # Type in your name
    author='hamednikseresht',

    # Type in your E-Mail
    author_email='hamednikseresht@gmail.com',

    # Provide either the link to your github or to your website
    url='https://github.com/hamednikseresht/ftkafinance',

    # download package url
    download_url='',

    # Keywords that define your package best
    keywords=['FTKAFINANCE', 'CRYPTO', 'CRYPTOCURRENCY'],

    # I get to this in a second
    install_requires=[
      'requests',
      'pandas',
      'python-dotenv',
      'pymongo',
      'TA-Lib',
    ],

    # Here I can specify the python version necessary to run this library.
    python_requires='>=3.7',

    # Additional classifiers that give some characteristics about the package.
    # For a complete list go to https://pypi.org/classifiers/.
    classifiers=[
      # Specify which pyhton versions that you want to support
      "Programming Language :: Python :: 3",
      # Again, pick a license
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
)
