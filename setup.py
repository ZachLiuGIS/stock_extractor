from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='stock_extractor',
      version='0.2',
      description='a general purpose stock data extractor',
      long_description=readme(),
      url='https://github.com/ZachLiuGIS/stock_extractor',
      author='Zach Liu',
      author_email='zachliugis@gmail.com',
      license='MIT',
      packages=['stock_extractor'],
      keywords='stock, finance, market',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Topic :: Office/Business :: Financial'
      ],
      install_requires=[
          'requests',
          'pandas',
          'beautifulsoup4',
          'dateutils',
      ],
      include_package_data=True,
      zip_safe=False)
