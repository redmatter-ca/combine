# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from setuptools import setup, find_packages

setup(
  name = "combine",
  version = "0.1",
  description = "Asset installation and upgrade management library for cross platform releases",
  author = "John Reese",
  author_email = "jreese@leetcode.net",

  classifiers = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Build Tools",
    "Topic :: System :: Archiving :: Packaging",
    "Topic :: System :: Installation/Setup",
    "Topic :: System :: Software Distribution",
  ],

  packages = find_packages(),
  zip_safe = True,
)

