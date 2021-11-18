import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SrbAI",
    version="0.0.1",
    author="Serbian AI Society",
    author_email="nikola.milosevic86@gmail.com",
    description="Library for processing serbian language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "nltk"
    ],
    package_dir={"": "srbai"},
    packages=setuptools.find_packages(where="srbai"),
    python_requires=">=3.6",
)