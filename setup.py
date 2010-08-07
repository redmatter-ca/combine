# Copyright (c) 2010 John Reese
# Licensed under the MIT license

combine_metadata = dict(
  name = "combine",
  version = "0.1",
  description = "Asset installation and upgrade management",
  long_description =
"""Cross platform module for automating the process of installing or upgrading
binary assets from an HTTP server to a local machine, utilizing various
compression and differencing methods to reduce bandwidth usage.
""",

  author = "John Reese",
  author_email = "jreese@leetcode.net",
  url = "http://leetcode.net/projects/combine",

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
  license = "MIT license",

  packages = ['combine'],
  zip_safe = True,
)

import platform
from setuptools import setup

if platform.system() == "Windows":
  import py2exe
  combine_metadata["console"] = []

setup(**combine_metadata)

