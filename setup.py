from setuptools import setup, find_packages


tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'mock',
]


setup(
    name='cdk',
    version='0.0',
    description='cdk',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld>=9.2.2',
        'clldmpg>=4.3',
    ],
    tests_require=tests_require,
    test_suite="cdk",
    entry_points="""\
[paste.app_factory]
main = cdk:main
""")
