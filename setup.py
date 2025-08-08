"""
This is a `setup.py` file used for packaging a Python project.

📌 Purpose:
- Makes your project installable via `pip install .`
- Allows you to share/distribute your code as a package.
- Helps tools like `pip`, `build`, and `setuptools` understand your project structure.

📌 Key Points:
- `setuptools` is a Python library that simplifies packaging Python projects.
- `find_packages()` automatically finds all Python packages (folders with `__init__.py` files) in your project.
- The arguments inside `setup()` describe your package metadata.

Once created, you can install your package locally by running:
    pip install -e .

This lets you import your modules anywhere on your system without needing relative paths.
"""

# Import the necessary functions from setuptools

from setuptools import setup, find_packages

# Call the setup function to provide package metadata and configuration
setup(
    name="src",  # Name of your package (this will be the name users install with pip)
    version="0.0.1",  # Version of your package (follow semantic versioning: major.minor.patch)
    author="Vijayraj singh",  # Author name
    author_email="vijayrajsinghsisodi@gmail.com",  # Author email
    packages=find_packages()  # Automatically find all packages (folders with __init__.py)
)

