import sys
from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = (3, 6)

if CURRENT_PYTHON < MIN_PYTHON:
    sys.stderr.write("""
        ============================
        Unsupported Python Version
        ============================
        
        Python {}.{} is unsupported. Please use a version newer than Python {}.{}.
    """.format(*CURRENT_PYTHON, *MIN_PYTHON))
    sys.exit(1)

with open('requirements.txt', 'r') as f:
    install_requires = f.readlines()

with open('VERSION') as f:
    VERSION = f.read().strip()

with open('README.md') as f:
    readme = f.readlines()

files = ["resources/*"]

setup(name='taggedtree',
      version=VERSION,
      description=readme,
      url='https://github.com/koheimiya/do-what-you-want',
      author='Kohei Miyaguchi',
      author_email='koheimiyaguchi@gmail.com',
      license='MIT',
      classifiers=[
          'Programming Language :: Python :: 3',
      ],
      packages=find_packages(),
      install_requires=install_requires,
      entry_points={
        'console_scripts': [
            'tt = app.tt:main',
            'itt = app.itt:main',
        ],
      },
      zip_safe=False)
