from setuptools import setup, find_packages

setup(
    name="pifan",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pifan-daemon = pifan.daemon:run"
        ]
    },
    include_package_data=True,
    data_files=[
        ("/etc/pifan", ["./default.toml"]),
        ("/etc/systemd/system", ["./pifand.service"])
    ],
    author="Emil Kelhälä",
    author_email="emil.kelhala@protonmail.com",
    license="GPL"
)