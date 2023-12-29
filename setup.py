import setuptools

__version__ = "1.1.0"

setuptools.setup(
    name="siblink",
    version=__version__,
    description="Sibling Link for trelbot's packages.",
    author="Trelta",
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
        'typer'
    ],
    package_data={"siblink": ["**/*.default.json"]}

)
