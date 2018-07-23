#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Kilobot_scripts',
      version='1.0',
      description='To do',
      author='Amaury Camus',
      author_email='amaury.camus92@gmail.com',
      url='to do',
      packages=['analyze_scripts', 'conversion_scripts', 'tracking'],
      scripts=['analyze_scripts/analyze_comm_range.py',
               'conversion_scripts/convert_all_data.py',
               'tracking/tracking_scripts/kilobot_tracking.py']
      )
