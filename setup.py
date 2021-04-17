from pathlib import Path
from setuptools import setup, find_packages

README = Path(__file__).parent.joinpath("README.md").read_text()

setup(
    author="Armani Tallam",
    author_email="armanitallam@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
    ],
    description="A simple way to evaluate Boolean Algebra.",
    license="BSD License",
    long_description=README,
    long_description_content_type="text/markdown",
    name="caesium-lang",
    packages=find_packages(),
    scripts=["caesium"],
    url="https://github.com/Armani-T/Caesium",
    version="1.4.0",
)
