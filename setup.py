from setuptools import setup, find_packages
PACKAGES = find_packages()

opts = dict(name='laminar',
            maintainer='Dane Gellerup',
            maintainer_email='danegellerup@uwalumni.com',
            description='Simpler parallelization.',
            long_description=open('README.md').read(),
            url='your_repo_url_here',
            license='MIT',
            author='Dane Gellerup',
            author_email='danegellerup@uwalumni.com',
            version='1.0.0',
            packages=PACKAGES,
            install_requires=["pandas>=0.24.0",
                                "numpy>=1.12.1"]
           )

setup(**opts)
