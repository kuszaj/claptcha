from setuptools import setup
from claptcha import __version__ as version
from claptcha import __doc__ as long_description


setup(name='claptcha',
      version=version,
      author="Piotr Kuszaj",
      author_email="peterkuszaj@gmail.com",
      url="https://github.com/kuszaj/claptcha/",
      description="A simple CAPTCHA image generator",
      long_description=long_description,
      license='MIT',
      install_requires=[
          'Pillow'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ]
)
