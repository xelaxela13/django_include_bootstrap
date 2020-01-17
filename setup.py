from setuptools import setup, find_packages

setup(
    name="django-include-bootstrap",
    version="1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["requests", "subresource-integrity"],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst", "*.msg"],
    },
    # metadata to display on PyPI
    author="Alex Stepanenko",
    author_email="xelaxela13@gmail.com",
    description="Include twitter bootstrap to Django templates",
    keywords="django, bootstrap",
    url="https://github.com/xelaxela13/django_include_bootstrap",
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries"
    ],
    include_package_data=True
)
