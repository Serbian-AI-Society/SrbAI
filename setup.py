import setuptools
import os
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.abspath(os.path.join('', path, filename)))
    return paths

extra_files = package_files('src/srbai/Resursi')

setuptools.setup(
    name="SrbAI",
    version="0.0.12",
    author="Serbian AI Society",
    author_email="nikola.milosevic86@gmail.com",
    description="Library for processing serbian language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Serbian-AI-Society/SrbAI",
    project_urls={
        "Bug Tracker": "https://github.com/Serbian-AI-Society/SrbAI/issues",
        "Road Map":"https://github.com/Serbian-AI-Society/SrbAI/projects/1"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "nltk",
        "torch>=1.10.2",
        "classla==1.1.0",
        "nlu"

    ],
    package_dir={"": "src"},
    package_data={'': extra_files},
    include_package_data=True,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)