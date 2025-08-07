from setuptools import setup, find_packages

__version__ = "1.2.2"

__longdescription = open("README.md", 'r').read()

setup(
    name="siblink",
    version=__version__,
    description="Sibling Link for python packages.",
    long_description=__longdescription,
    long_description_content_type="text/markdown",
    author="Trelta",
    author_email="treltasev@gmail.com",
    url="https://github.com/treltasev/siblink",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "siblink = siblink.cli:main"
        ]
    },
    install_requires=[
        'pyucc',
        'click'
    ],
    package_data={"siblink": ["**/*.json"]}

)
