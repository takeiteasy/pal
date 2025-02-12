from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read().splitlines()

setup(
    name="pal",
    version="0.0.1",
    author="George Watson",
    author_email="gigolo@hotmail.co.uk",
    description="Python Abstraction Layer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takeiteasy/pal",
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"])
