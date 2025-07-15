"""
Setup script for perforce-helix-core-python-tools.
"""

from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open(os.path.join('perforce_tools', '__init__.py'), 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '0.0.0'

# Read long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='perforce-helix-core-python-tools',
    version=version,
    description='A suite of command-line tools for interacting with Perforce Helix Core server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/perforce-helix-core-python-tools',
    packages=find_packages(),
    install_requires=[
        'p4python',
        'pyyaml',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'phc=perforce_tools.phc:cli',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
