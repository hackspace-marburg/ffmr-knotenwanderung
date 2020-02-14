from setuptools import setup, find_packages

setup(
    name="knotenwanderung",
    version="0.1.0",
    description="Check FFMR nodes for renaming",
    url="https://github.com/hackspace-marburg/ffmr-knotenwanderung",
    packages=find_packages(),
    install_requires=["bottle", "influxdb"],
    include_package_data=True,
    entry_points={
      "console_scripts": ["knotenwanderung=knotenwanderung.knotenserv:main"]
    }
)
