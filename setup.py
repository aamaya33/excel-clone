from setuptools import setup, find_packages

setup(
    name="excel_clone",
    version="0.1.0",
    author="aamaya3",
    description="Google Sheets clone with Python, SQL/SQLAlchemy and pandas",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "openai>=0.27.0",
        "pandas>=1.5.0",
        "sqlalchemy>=2.0.0",
        "pytest>=7.0.0",
    ],
    packages=find_packages(),
    py_modules=["chat", "database", "main"],
    entry_points={
        "console_scripts": [
            "excel-clone=main:cli_main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)