from setuptools import setup, find_packages
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))
# Get the long description from the README.md file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ctyun_hybrid_sdk',
    version="0.0.12",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='CTYUN Hybrid API Gateway Team',
    url='https://work.ctyun.cn/git/hybrid-gateway/ctyun-hybrid-python-sdk',
    scripts=[],
    packages=find_packages(),
    install_requires=['requests', 'urllib3'],
    license="Apache License V2.0"
)
