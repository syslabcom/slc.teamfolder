from setuptools import setup, find_packages
import os

version = "0.1"

setup(
    name='slc.teamfolder',
    version=version,
    description="",
    long_description="\n".join((
        open(os.path.join("docs", "README.rst")).read(),
        open(os.path.join("docs", "CHANGES.rst")).read(),
    )),
    classifiers=[
      "Framework :: Plone",
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='osha plone syslab.com',
    author='Syslab.com GmbH',
    author_email='info@syslab.com',
    url='https://github.com/syslabcom/slc.teamfolder',
    license='GPL',
    packages=['slc', 'slc/teamfolder'],
    package_dir = {'' : 'src'},
    namespace_packages=['slc'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      'setuptools',
      ],
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
    """,
    )
