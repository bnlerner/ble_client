from distutils.core import setup

setup(
    name="ble_client", 
    description="client for ble peripheral services on video ml device", 
    scripts=["bin/run_ble_client.py"], 
    version="0.0.1", 
    license="MIT",
    url="https://github.com/bnlerner/ble_client",
    packages=["ble_client"],
    requires=[],
    extras_require={
        "pybleno": ["pybleno"]
    }
    )
