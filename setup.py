from setuptools import setup
from setuptools import find_packages


with open("README.rst") as f:
    long_description = f.read()


setup(
    name="<PARAM: package-name>",
    version="<PARAM: api_version.major_version.revision_number>",
    license="MIT",
    description="<PARAM: Short description>",
    long_description=long_description,
    author="<PARAM: Author Surname>",
    author_email="<PARAM: author@email.here (optional)>",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["numpy", "scikit-learn"],  # Add additional requirements here
    extras_require={"test": ["pytest"], "dev": ["black", "pytest"]},  # Add additional requirements here
)
