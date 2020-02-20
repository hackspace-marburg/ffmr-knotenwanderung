from setuptools import setup, find_packages

setup(
    name="knotenwanderung",
    description="Check FFMR nodes for renaming",
    url="https://github.com/hackspace-marburg/ffmr-knotenwanderung",
    packages=find_packages(),
    install_requires=["bjoern", "bottle", "cachetools", "influxdb"],
    include_package_data=True,
    entry_points={
      "console_scripts": ["knotenwanderung=knotenwanderung.knotenserv:main"]
    }
)
