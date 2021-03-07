import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name="li_scraper",
                 version="0.0.1",
                 author="Hju Kneyck M. Flores",
                 author_email="hjucode@gmail.com",
                 description="A specific LinkedIn scraper",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/yue-fl/li-scraper",
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 keywords='python, python3, selenium, scraper, pandas',
                 python_requires='>=3.6',
                 install_requires=[
                     'numpy==1.19.3', 'pandas>=1.1.5', 'selenium>=3.141.0',
                     'requests>=2.25.0', 'msedge-selenium-tools>=3.141.3'
                 ])
