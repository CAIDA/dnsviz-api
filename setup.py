import setuptools

with open('requirements.txt', 'r') as requirements_file:
    requirements = requirements_file.readlines()

setuptools.setup(
    name="dnsviz_api",
    version="0.0.1",
    author="Vinay Pillai",
    author_email="vspillai@ucsd.edu",
    packages=['dnsviz_api'],
    install_requires=requirements,
    python_requires=">=3.6",
)