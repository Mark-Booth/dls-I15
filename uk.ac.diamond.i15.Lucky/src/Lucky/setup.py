'''
Created on 26 Feb 2016

@author: wnm24546
'''
from distutils.core import setup

setup(name="Lucky",
      version="0.1",
      description="Visible light spectrum temperature calculator",
      long_description="Uses Black Body radiation models (Wien, Planck, Two Colour) to calculate temperature of a spot in a Laser Heating experiment.",
      author="Michael Wharmby",
      author_email="michael.wharmby@diamond.ac.uk",
      packages=["Lucky", "Lucky.ui"],
      license=""#BSD or EPL
      )